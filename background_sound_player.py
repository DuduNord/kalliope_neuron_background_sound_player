import logging
import subprocess
import os
import sys
import psutil
import threading
from time import sleep
from kalliope.core.Utils import Utils
from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException
from kalliope.core.Cortex import Cortex

logging.basicConfig()
logger = logging.getLogger("kalliope")

pid_file_path = "pid.txt"

class Background_sound_player(NeuronModule):
    """
    Background sound player neuron
    Play the stream from a file or an url
    (for example: ./musics/zelda/fullOst.wav, or Radio Néo url like: http://stream.radioneo.org:8000/;stream/1)
    """
    def __init__(self, **kwargs):
        super(Background_sound_player, self).__init__(**kwargs)

        self.state = kwargs.get('state', None)
        self.sound_link = kwargs.get('sound_link', None)
        self.sound_name = kwargs.get('sound_name', None)
        self.mplayer_path = kwargs.get('mplayer_path', "/usr/bin/mplayer")
        self.auto_stop_minutes = kwargs.get('auto_stop_minutes', None)

        # a dict of parameters the user ask to save in short term memory
        self.kalliope_memory = kwargs.get('kalliope_memory', None)
        # parameters loaded from the order can be save now
        Cortex.save_parameter_from_order_in_memory(self.kalliope_memory)

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
                self.start_new_process(self.sound_link)

                # give the current file name played to the neuron template
                self.message["sound_link"] = self.sound_link
                self.message["sound_name"] = self.sound_name

                # we save the sound's name to Kalliope be able to answer if we ask
                Cortex.save("current_playing_background_sound", self.sound_name)

                # run auto stop thread
                if self.auto_stop_minutes:
                    thread_auto_stop = threading.Thread(target=self.wait_before_stop)
                    thread_auto_stop.start()

            # give the message dict to the neuron template
            self.say(self.message)

    def is_playable_link(self, sound_link):
        """
        Checks if the link is playable in mplayer.
        Not done yet.
        return: True if playable, False if it isn't
        """
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
            if self.sound_link is None:
                raise InvalidParameterException("[Background_sound_player] You have to specify a sound_link parameter")
            if self.is_playable_link(self.sound_link) is not True:
                raise InvalidParameterException("[Background_sound_player] The sound_link parameter you specified is not a valid playable link")
            if self.sound_name is None:
                raise InvalidParameterException("[Background_sound_player] You have to specify a sound_name parameter")

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

    @staticmethod
    def store_pid(pid):
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

    @classmethod
    def get_scriptdir_absolute_path(cls):
        return os.path.dirname(os.path.abspath( __file__ ))

    @staticmethod
    def load_pid():
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

    def stop_last_process(self):
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

    def start_new_process(self, radio_url):
        """
        Start mplayer process with the given radio_url
        :param radio_url:
        :type radio_url: str
        :return:
        """
        mplayer_exec_path = [self.mplayer_path]
        mplayer_options = ['-slave', '-quiet', '-loop', '0', '-af', 'volume=-15']
        mplayer_command = list()
        mplayer_command.extend(mplayer_exec_path)
        mplayer_command.extend(mplayer_options)

        mplayer_command.append(radio_url)
        logger.debug("[Background_sound_player] Mplayer cmd: %s" % str(mplayer_command))

        # run mplayer in background inside a new process
        fnull = open(os.devnull, 'w')
        pid = subprocess.Popen(mplayer_command, stdout=fnull, stderr=fnull).pid

        # store the pid in a file to be killed later
        self.store_pid(pid)

        logger.debug("[Background_sound_player] Mplayer started, pid: %s" % pid)

    @staticmethod
    def clean_pid_file():
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
