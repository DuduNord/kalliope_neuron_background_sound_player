# for some reason, launching a new process through subprocess.Popen can't launch all files in a folder but can launch a TXT playlist
# Mplayer does not take more than one TXT playlist and play the first one in the list (seems that -shuffle option has then no effect)
# manage different song input, mix of TXT playlist or other songs in _check_sounds function
# 1/ if a mix is none between TXT playlist and songs, an error is reported
# 2/ in case of no random, the first TXT playlist is sent to MPLAY
# 3/ in case of one selected randomly, only one TXT playlist is passed, with -playlist arg, but with no shuffle
# need to arrange the returned song title when many songs are passed.
import logging
import subprocess
import os
import sys
import psutil
import threading
import random
from time import sleep
from kalliope.core.Utils import Utils
from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException
from kalliope.core.Cortex import Cortex

logging.basicConfig()
logger = logging.getLogger("kalliope")

pid_file_path = "pid.txt"
NAME = 0
LINK = 1
# Default volume numbers
VOLUME_MIN = "-40"
VOLUME_MAX = "-10"
VOLUME_DEFAULT = "-17"
VOLUME_LISTEN = "-35"

class Background_sound_player(NeuronModule):
    """
    Background sound player neuron
    Play the stream from a file or an url
    (for example: ./musics/zelda/fullOst.wav, or Radio Néo url like: http://stream.radioneo.org:8000/;stream/1)
    """
    def __init__(self, **kwargs):
        super(Background_sound_player, self).__init__(**kwargs)

        self.state = kwargs.get('state', None)                                  # "on" / "off"
        self.sounds = kwargs.get('sounds', None)                                # "[{'title1': 'link1'}, {'title2': 'link2'}, ...]"
        self.random_option = kwargs.get('random_option', "no-random")           # "random-order-play" / "random-select-one" / "no-random"
        self.loop_option = kwargs.get('loop_option', 'no-loop')                 # "loop" / "no-loop"
        self.mplayer_path = kwargs.get('mplayer_path', "/usr/bin/mplayer")      
        self.auto_stop_minutes = kwargs.get('auto_stop_minutes', None)
        self.volume = kwargs.get('volume', VOLUME_DEFAULT)

        # a dict of parameters the user ask to save in short term memory
        self.kalliope_memory = kwargs.get('kalliope_memory', None)
        # parameters loaded from the order can be save now
        Cortex.save_parameter_from_order_in_memory(self.kalliope_memory)
        Cortex.save("current_playing_background_sound", "Aucun fond sonore lancé actuellement")

        # message dict that will be passed to the neuron template
        self.message = dict()

        # check if sent parameters are in good state
        if self._is_parameters_ok():
            if self.state == "off":
                self.stop_last_process()
                self.clean_pid_file()
                Cortex.save("current_playing_background_sound", "Aucun fond sonore lancé actuellement")
            else:
                # we stop the last process if exist
                self.stop_last_process()

                # then we can start a new process
                self.start_new_process(self.sounds)
                Cortex.save("Mplayer_current_volume", self.volume)
                
                # run auto stop thread
                if self.auto_stop_minutes:
                    thread_auto_stop = threading.Thread(target=self.wait_before_stop)
                    thread_auto_stop.start()

            # give the message dict to the neuron template
            self.say(self.message)

    def start_new_process(self, sound_arg):         #Start mplayer process
        """
        Start mplayer process with the given sounds to play
        :param sound_arg:
        :type sound_arg: list of dicts [{name: link}, {name: link}, {name: link}]
        :return:
        """

        currently_playing_sound = None

        mplayer_exec_path = [self.mplayer_path]
        mplayer_options = ['-slave', '-quiet', '-af'] 
        mplayer_volume = ['volume']
        mplayer_volume[0] = "volume="+self.volume
        mplayer_loop = ['-loop']
        mplayer_loop.append("0" if self.loop_option == "loop" else "1")
        # mplayer { 1.avi - loop 2 2.avi } -loop 3 > La commande  jouera les fichiers dans cet ordre: 1, 1, 2, 1, 1, 2, 1, 1, 2. "-loop 0" tournera a l'infini
        
        first_sound_name, first_sound_link = list(sound_arg[0].items())[0]
        first_sound_link = str(first_sound_link)
        # Pick one sound randomly in all sounds entered. currently_playing_sound will have only one entry
        # Need anyway to add "-playlist" if the link is a TXT playlist. But this playlist will be read with no shuffle option
        if self.random_option == "random-select-one":
            currently_playing_sound = [random.choice(sound_arg)]
            if (first_sound_link)[-4:] == ".txt":
                mplayer_loop.append("-playlist")
        # play all sounds in random order if there is no TXT playlist
        # at this stage, the list either only TXT or playable files (if not it should has raised an error in _check_sounds function
        # if the links are then TXT playlist, one will be selected. Otherwise, shuffle parameter is added to MPLAYER commands > need "-playlist" for TXT playlist
        elif self.random_option == "random-order-play":
            mplayer_loop.append("-shuffle")
            if str(first_sound_link)[-4:] == ".txt":                          # if it is a TXT (then like all others), need to randomly select one
                currently_playing_sound = [random.choice(sound_arg)]
                mplayer_loop.append("-playlist")
            else:
                currently_playing_sound = sound_arg
        # play all sounds the specified order
        else:
            if str(first_sound_link)[-4:] == ".txt":                          # if it is a TXT (then like all others)
                mplayer_loop.append("-playlist")                        # then indicate that this is a playlist
                currently_playing_sound = sound_arg[0]                  # and select the first playlist
            else:
                currently_playing_sound = sound_arg                     # else the list is simply copied

        mplayer_command = list()
        mplayer_command.extend(mplayer_exec_path)
        mplayer_command.extend(mplayer_options)
        mplayer_command.extend(mplayer_volume)
        mplayer_command.extend(mplayer_loop)
        for sound in currently_playing_sound:
            for sound_name, sound_link in sound.items():
                mplayer_command.append(sound_link)

        logger.debug("[Background_sound_player] Mplayer cmd: %s" % str(mplayer_command))
        Cortex.save("current_playing_background_sound", sound_name)

        # give the current file name played to the neuron template
        self.message['sound_name'] = sound_name
        self.message["sound_link"] = sound_link

        # run mplayer in background inside a new process
        fnull = open(os.devnull, 'w')
        # mplayer_command = "mplayer -slave -quiet -af volume=-20 -loop 0 -shuffle -playlist /home/pi/kalliope_starter_fr/resources/sounds/MP3/Florian/*.*"
        pid = subprocess.Popen(mplayer_command, stdout=fnull, stderr=fnull).pid

        # store the pid in a file to be killed later
        self.store_pid(pid)
        logger.debug("[Background_sound_player] Mplayer started, pid: %s" % pid)


    def _is_playable_link(self, link):
        """
        Checks if the link is playable in mplayer.
        Not done yet.
        return: True if playable, False if it isn't
        """
        return True

    def _check_sounds(self, sounds):
        NbTXTplaylist = 0

        if (type(sounds) != type([]) or len(sounds) == 0):
            raise InvalidParameterException("[Background_sound_player] The sounds parameter is not set properly. Please use the representation specified in the documentation.")

        for sound in sounds:
            sound_name, sound_link = list(sound.items())[0]
            sound_name, sound_link = str(sound_name), str(sound_link)

            if sound_name == "":
                raise InvalidParameterException("[Background_sound_player] The name parameter is not set properly. Please set the name as specified in the documentation.")
            if sound_link == "":
                raise InvalidParameterException("[Background_sound_player] The link parameter is not set properly. Please set the link as specified in the documentation.")
            if sound_link[-4:] == ".txt":
                NbTXTplaylist += 1
            if self._is_playable_link(sound_link) is not True:
                raise InvalidParameterException("[Background_sound_player] The link " + sound_link + " is not a playble stream.")
        if (NbTXTplaylist > 0 and NbTXTplaylist is not len(sounds)):
            if NbTXTplaylist == 1:
                raise InvalidParameterException("[Background_sound_player] One of the link is a TXT playlist and mixed with " + str(len(sounds)-NbTXTplaylist) + " classic sound(s).")
            else:
                raise InvalidParameterException("[Background_sound_player] " + str(NbTXTplaylist) + " links are a TXT playlist and mixed with " + str(len(sounds)-NbTXTplaylist) + " classic sound(s).")
        else:
            if NbTXTplaylist == 0:
                logger.debug("[Background_sound_player] Get only song(s)")
            else:
                logger.debug("[Background_sound_player] Get only TXT playlist(s)")
        return True

    def wait_before_stop(self):
        logger.debug("[Background_sound_player] Wait %s minutes before checking if the thread is alive" % self.auto_stop_minutes)
        Utils.print_info("[Background_sound_player] Wait %s minutes before stopping the ambient sound" % self.auto_stop_minutes)
        sleep(self.auto_stop_minutes*60)  # *60 to convert received minutes into seconds
        logger.debug("[Background_sound_player] Time is over, Stop player")
        Utils.print_info("[Background_sound_player] Time is over, stopping the ambient sound")
        self.stop_last_process()

    def _is_parameters_ok(self):
        """
        Check that all given parameter are valid
        :return: True if all given parameter are ok
        """

        if self.state not in ["on", "off"]:
            raise InvalidParameterException("[Background_sound_player] State must be 'on' or 'off'")

        if self.state == "on":
            if self.sounds is None:
                raise InvalidParameterException("[Background_sound_player] You have to specify a sound parameter")
            elif type(self.sounds) != type([]):
                raise InvalidParameterException("[Background_sound_player] You have to specify the sound parameter as shown in the documentation.")
            if self._check_sounds(self.sounds) is not True:
                raise InvalidParameterException("[Background_sound_player] A sound parameter you specified in the list is not a valid playable link")
            if self.random_option not in ["random-select-one", "random-order-play", "no-random"]:
                raise ValueError("[Background_sound_player] random_option parameter must be \"random-select-one\" OR \"random-order-play\" OR \"no-random\" if specified")
            if self.loop_option not in ["loop", "no-loop"]:
                raise ValueError("[Background_sound_player] loop_option parameter must be \"loop\" OR \"no-loop\" if specified")
            # check if the volume parameter is in the correct range. otherwise, report a debug message and change volume to min or max
            if self.volume is not None:
                if int(self.volume) > int(VOLUME_MAX):
                    #raise ValueError("[Background_sound_player] Volume parameter ("+self.volume+") must be between " + VOLUME_MIN +" and " + VOLUME_MAX)
                    logger.debug("[Background_sound_player] Volume parameter ("+self.volume+") must be between " + VOLUME_MIN +" and " + VOLUME_MAX + ". Set volume to "+ VOLUME_MAX)
                    self.volume = VOLUME_MAX
                elif int(self.volume) < int(VOLUME_MIN):
                    logger.debug("[Background_sound_player] Volume parameter ("+self.volume+") must be between " + VOLUME_MIN +" and " + VOLUME_MAX + ". Set volume to "+ VOLUME_MIN)
                    self.volume = VOLUME_MIN
        # if wait auto_stop_minutes is set, must be an integer or string convertible to integer
        if self.auto_stop_minutes is not None:
            if not isinstance(self.auto_stop_minutes, int):
                try:
                    self.auto_stop_minutes = int(self.auto_stop_minutes)
                except ValueError:
                    raise InvalidParameterException("[Background_sound_player] auto_stop_minutes must be an integer")
            # check auto_stop_minutes is positive
            if self.auto_stop_minutes < 1:
                raise InvalidParameterException("[Background_sound_player] auto_stop_minutes must be set at least to 1 minute")
        return True

    @classmethod
    def get_scriptdir_absolute_path(cls):
        return os.path.dirname(os.path.abspath( __file__ ))

    @staticmethod
    def store_pid(pid):             # Store a PID number into a file
        """
        Store a PID number into a file
        :param pid: pid number to save
        :return:
        """

        content = str(pid)
        absolute_pid_file_path = os.path.dirname(os.path.abspath( __file__ )) + os.sep + pid_file_path
        try:
            with open(absolute_pid_file_path, "wb") as file_open:
                if sys.version_info[0] == 2:
                    file_open.write(content)
                else:
                    file_open.write(content.encode())
                file_open.close()

        except IOError as e:
            logger.error("[Background_sound_player] I/O error(%s): %s", e.errno, e.strerror)
            return False

    @staticmethod
    def load_pid():                     # Load a PID number from the pid.txt file
        """
        Load a PID number from the pid.txt file
        :return:
        """
        absolute_pid_file_path = Background_sound_player.get_scriptdir_absolute_path() + os.sep + pid_file_path

        if os.path.isfile(absolute_pid_file_path):
            try:
                with open(absolute_pid_file_path, "r") as file_open:
                    pid_str = file_open.readline()
                    if pid_str:
                        return int(pid_str)

            except IOError as e:
                logger.debug("[Background_sound_player] I/O error(%s): %s", e.errno, e.strerror)
                return False
        return False

    def stop_last_process(self):            # stop the last mplayer from PID file info
        """
        stop the last mplayer process launched by this neuron
        :return:
        """
        pid = self.load_pid()

        if pid is not None:
            logger.debug("[Background_sound_player] loaded pid: %s" % pid)
            try:
                p = psutil.Process(pid)
                p.kill()
                logger.debug("[Background_sound_player] mplayer process with pid %s killed" % pid)
            except psutil.NoSuchProcess:
                logger.debug("[Background_sound_player] the process PID %s does not exist" % pid)
        else:
            logger.debug("[Background_sound_player] pid is null. Process already stopped")

    @staticmethod
    def clean_pid_file():           #Clean up all data stored in the pid.txt file
        """
        Clean up all data stored in the pid.txt file
        """

        absolute_pid_file_path = Background_sound_player.get_scriptdir_absolute_path() + os.sep + pid_file_path
        try:
            with open(absolute_pid_file_path, "w") as file_open:
                file_open.close()
                logger.debug("[Background_sound_player] pid file cleaned")

        except IOError as e:
            logger.error("I/O error(%s): %s", e.errno, e.strerror)
            return False
