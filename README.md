# kalliope_neuron_background_sound_player
a Kalliope Neuron that launch and stop background sound (ambient, radio, wav files, anything you want). Based on Ambient Neuron and is suppose to manage all "Ambient Neuron" and "Launch Radio Neuron" problematicals in the near future.

## Documentation:
At that time it is just a 0.1 version. The full documentation is comming quickly wonce we've solve the following features:
- manage the random files launching from a directory --> useful for the ambient feature
- manage the playlist launching --> be able to launch a list of links instead of only one

## Examples Synapses:

###
```yaml
- name: "wich-music-is-playing-synapse"
  signals:
    - order: "musique jouée"
    - order: "musique maintenant"
    - order: "musique en ce moment"
    - order: "musique entend"
    - order: "musique écoute"
  neurons:
    - say:
        message: "{{kalliope_memory['current_playing_background_sound']}}."

- name: "stop-music-synapse"
  signals:
    - order: "coupe la musique"
    - order: "couper la musique"
    - order: "stoppe la musique"
  neurons:
    - background_sound_player:
        state: "off"

- name: "launch-zelda-Musique-synapse"
  signals:
    - order: "musique de Zelda"
  neurons:
    - background_sound_player:
        state: "on"
        sounds:
          - "theme général": "./resources/sounds/Music/Zelda/awakening.mp3"
        say_template:
          - "{{sound_name}} lancée."

- name: "launch-zelda-Musique-synapse2"
  signals:
    - order: "musique de Zelda"
  neurons:
    - background_sound_player:
        state: "on"
        random_option: "no_random"
        sounds:
          - "theme général": "./resources/sounds/Music/Zelda/awakening.mp3"
          - "choisir sa partie": "./resources/sounds/Music/Zelda/choose_player.mp3"
          - "intro": "./resources/sounds/Music/Zelda/intro.mp3"
        say_template:
          - "playliste lancée."
```

### Radio Launcher:
```yaml
- name: "wich-radio-is-playing-synapse"
  signals:
    - order: "radio jouée"
    - order: "radio maintenant"
    - order: "radio en ce moment"
    - order: "radio entend"
    - order: "radio écoute"
  neurons:
    - say:
        message: "{{kalliope_memory['current_playing_background_sound']}}."

- name: "stop-radio-synapse"
  signals:
    - order: "coupe la radio"
    - order: "couper la radio"
    - order: "stoppe la radio"
  neurons:
    - background_sound_player:
        state: "off"

- name: "Launch-radio-choice-synapse"
  signals:
    - order:
        text: "passe en mode radio"
        matching-type: "ordered-strict"
  neurons:
    - say:
        message: "Quelle radio voulez-vous lancer ?"
    - neurotransmitter:
        from_answer_link:
        - synapse: "launch-radio-Neo-synapse"
          answers:
            - "Radio Néo"
        - synapse: "launch-radio-RTL-synapse"
          answers:
            - "RTL"
        - synapse: "launch-radio-classique-synapse"
          answers:
            - "Radio Classique"
        - synapse: "launch-radio-FIP-synapse"
          answers:
            - "FIP"
        - synapse: "launch-radio-Nova-synapse"
          answers:
            - "Radio Nova"
        - synapse: "launch-radio-TSF-Jazz-synapse"
          answers:
            - "TSF Jazz"
        - synapse: "launch-radio-France-Inter-synapse"
          answers:
            - "France Inter"
        - synapse: "launch-radio-France-Culture-synapse"
          answers:
            - "France Culture"
        - synapse: "launch-radio-France-Musique-synapse"
          answers:
            - "France Musique"
        default: "launch-radio-Neo-synapse"


- name: "launch-radio-Neo-synapse"
  signals:
    - order: "mets-nous Radio Néo"
    - order: "lance Radio Néo"
    - order: "lancer Radio Néo"
    - order: "mettre Radio Néo"
    - order: "lance-moi Radio Néo"
    - order: "mets-moi Radio Néo"
    - order: "mets Radio Néo"
    - order: "tu peux mettre Radio Néo"
    - order: "tu peux lancer Radio Néo"
  neurons:
    - background_sound_player:
        state: "on"
        sounds:
          - "Radio Néo": "http://stream.radioneo.org:8000/;stream/1"
        say_template:
          - "{{sound_name}} lancée."

- name: "launch-radio-RTL-synapse"
  signals:
    - order: "mets-nous RTL"
    - order: "lance RTL"
    - order: "lancer RTL"
    - order: "mettre RTL"
    - order: "lance-moi RTL"
    - order: "mets-moi RTL"
    - order: "mets RTL"
    - order: "tu peux mettre RTL"
    - order: "tu peux lancer RTL"
  neurons:
    - background_sound_player:
        sounds:
        - "RTL": "http://streaming.radio.rtl.fr/rtl-1-48-192"
        say_template:
          - "{{sound_name}} lancée."

- name: "launch-radio-classique-synapse"
  signals:
    - order: "mets-nous Radio Classique"
    - order: "lance Radio Classique"
    - order: "lancer Radio Classique"
    - order: "mettre Radio Classique"
    - order: "lance-moi Classique"
    - order: "mets-moi Classique"
    - order: "mets Radio Classique"
    - order: "tu peux mettre Radio Classique"
    - order: "tu peux lancer Radio Classique"
  neurons:
    - background_sound_player:
        state: "on"
        sounds:
          - "Radio Classique": "http://radioclassique.ice.infomaniak.ch/radioclassique-high.mp3"
        say_template:
          - "{{sound_name}} lancée."

- name: "launch-radio-FIP-synapse"
  signals:
    - order: "mets-nous Radio FIP"
    - order: "lance Radio FIP"
    - order: "lancer Radio FIP"
    - order: "mettre Radio FIP"
    - order: "lance-moi Radio FIP"
    - order: "mets-moi Radio FIP"
    - order: "mets Radio FIP"
    - order: "tu peux mettre Radio FIP"
    - order: "tu peux lancer Radio FIP"
  neurons:
    - background_sound_player:
        state: "on"
        sounds:
          - "Radio FIP": "http://direct.fipradio.fr/live/fip-midfi.mp3"
        say_template:
          - "{{sound_name}} lancée."

- name: "launch-radio-Nova-synapse"
  signals:
    - order: "mets-nous Radio Nova"
    - order: "lance Radio Nova"
    - order: "lancer Radio Nova"
    - order: "mettre Radio Nova"
    - order: "lance-moi Radio Nova"
    - order: "mets-moi Radio Nova"
    - order: "mets Radio Nova"
    - order: "tu peux mettre Radio Nova"
    - order: "tu peux lancer Radio Nova"
  neurons:
    - background_sound_player:
        state: "on"
        sounds:
          - "Radio Nova": "http://novazz.ice.infomaniak.ch/novazz-128.mp3"
        say_template:
          - "{{sound_name}} lancée."

- name: "launch-radio-TSF-Jazz-synapse"
  signals:
    - order: "mets-nous TSF Jazz"
    - order: "lance TSF Jazz"
    - order: "lancer TSF Jazz"
    - order: "mettre TSF Jazz"
    - order: "lance-moi TSF Jazz"
    - order: "mets-moi TSF Jazz"
    - order: "mets TSF Jazz"
    - order: "tu peux mettre TSF Jazz"
    - order: "tu peux lancer TSF Jazz"
  neurons:
    - background_sound_player:
        state: "on"
        sounds:
          - "TSF Jazz": "http://direct.fipradio.fr/live/fip-midfi.mp3"
        say_template:
          - "Radio {{sound_name}} lancée."

- name: "launch-radio-France-Inter-synapse"
  signals:
    - order: "mets-nous France Inter"
    - order: "lance France Inter"
    - order: "lancer France Inter"
    - order: "mettre France Inter"
    - order: "lance-moi France Inter"
    - order: "mets-moi France Inter"
    - order: "mets France Inter"
    - order: "tu peux mettre France Inter"
    - order: "tu peux lancer France Inter"
  neurons:
    - background_sound_player:
        state: "on"
        sounds:
          - "France Inter": "http://direct.franceinter.fr/live/franceinter-midfi.mp3"
        say_template:
          - "Radio {{sound_name}} lancée."

- name: "launch-radio-France-Culture-synapse"
  signals:
    - order: "mets-nous France Culture"
    - order: "lance France Culture"
    - order: "lancer France Culture"
    - order: "mettre France Culture"
    - order: "lance-moi France Culture"
    - order: "mets-moi France Culture"
    - order: "mets France Culture"
    - order: "tu peux mettre France Culture"
    - order: "tu peux lancer France Culture"
  neurons:
    - background_sound_player:
        state: "on"
        sounds:
          - "France Culture": "http://direct.franceculture.fr/live/franceculture-midfi.mp3"
        say_template:
          - "Radio {{sound_name}} lancée."

- name: "launch-radio-France-Musique-synapse"
  signals:
    - order: "mets-nous France Musique"
    - order: "lance France Musique"
    - order: "lancer France Musique"
    - order: "mettre France Musique"
    - order: "lance-moi France Musique"
    - order: "mets-moi France Musique"
    - order: "mets France Musique"
    - order: "tu peux mettre France Musique"
    - order: "tu peux lancer France Musique"
  neurons:
    - background_sound_player:
        state: "on"
        sounds:
          - "France Musique": "http://direct.francemusique.fr/live/francemusique-midfi.mp3"
        say_template:
          - "Radio {{sound_name}} lancée."
```

### Ambient sound launcher:
```yaml
- name: "wich-ambient-is-playing-synapse"
  signals:
    - order: "ambiance jouée"
    - order: "ambiance maintenant"
    - order: "ambiance en ce moment"
    - order: "ambiance entend"
    - order: "ambiance écoute"
  neurons:
    - say:
        message: "Ambiance {{kalliope_memory['current_playing_background_sound']}}."

- name: "stop-ambient-synapse"
  signals:
    - order: "stoppe l'ambiance"
  neurons:
    - say:
        message: "Entendu."
    - background_sound_player:
        state: "off"

- name: "launch-random-ambient-synapse"
  signals:
    - order: "mets-nous ambiance au pif"
    - order: "mets-moi ambiance au pif"
    - order: "mets ambiance au pif"
    - order: "autre ambiance"
    - order: "change l'ambiance"
    - order: "change d'ambiance"
  neurons:
    - say:
        message:
        - "celle-ci devrait convenir"
        - "que pensez-vous de celle-ci ?"
        - "celle-ci me semble appropriée"
        - "si vous me le permettez, ma préférence va à celle-ci"
        - "Bien Monsieur"
    - background_sound_player:
        state: "on"
        loop_option: "loop"
        sounds:
          - "Oiseaux": "./resources/sounds/ambientSounds/birds.mp3"
          - "Feu de camp": "./resources/sounds/ambientSounds/fireplace.ogg"
          - "Forêt": "./resources/sounds/ambientSounds/forest.mp3"
          - "Source": "./resources/sounds/ambientSounds/stream.mp3"
          - "Vent": "./resources/sounds/ambientSounds/wind.mp3"
          - "Ruisseau": "./resources/sounds/ambientSounds/forest-stream.mp3"
          - "Montagne": "./resources/sounds/ambientSounds/mountain-stream.mp3"
          - "Océan": "./resources/sounds/ambientSounds/ocean-waves.mp3"
          - "Lac": "./resources/sounds/ambientSounds/seaside.mp3"
          - "Eau": "./resources/sounds/ambientSounds/stream.ogg"
          - "Tropical": "./resources/sounds/ambientSounds/tropical-beach.mp3"
          - "Vent": "./resources/sounds/ambientSounds/wind.ogg"
          - "Bateau mouillé": "./resources/sounds/ambientSounds/wood-sailboat.mp3"

- name: "launch-ambient-synapse"
  signals:
    - order: "mets-nous une ambiance sonore"
    - order: "mets-moi une ambiance sonore"
    - order: "j'ai besoin d'une ambiance"
    - order: "j'aurais besoin d'une ambiance"
  neurons:
    - say:
        message: "Vous avez une préférence ?"
    - neurotransmitter:
        from_answer_link:
          - synapse: "launch-birds-ambient-synapse"
            answers:
              - "oiseaux"
          - synapse: "launch-fireplace-ambient-synapse"
            answers:
              - "feu"
              - "cheminée"
          - synapse: "launch-forest-ambient-synapse"
            answers:
              - "forêt"
          - synapse: "launch-rain-ambient-synapse"
            answers:
              - "pluie"
          - synapse: "launch-stream-ambient-synapse"
            answers:
              - "ruisseau"
          - synapse: "launch-mountain-ambient-synapse"
            answers:
              - "montagne"
          - synapse: "launch-ocean-ambient-synapse"
            answers:
              - "océan"
              - "mer"
              - "plage"
          - synapse: "launch-lake-ambient-synapse"
            answers:
              - "lac"
          - synapse: "launch-water-ambient-synapse"
            answers:
              - "l'eau"
          - synapse: "launch-storm-ambient-synapse"
            answers:
              - "orage"
              - "tempête"
              - "tonnerre"
          - synapse: "launch-tropical-ambient-synapse"
            answers:
              - "tropical"
          - synapse: "launch-wind-ambient-synapse"
            answers:
              - "vent"
              - "venteux"
              - "souffle"
              - "soufflante"
          - synapse: "launch-boat-ambient-synapse"
            answers:
              - "bateau"
              - "pirate"
              - "piraterie"
              - "navire"
              - "corsaire"
              - "mouillage"
        default: "launch-random-ambient-synapse"

- name: "launch-birds-ambient-synapse"
  signals: {}
  neurons:
    - background_sound_player:
        state: "on"
        sounds:
          - "Oiseaux": "./resources/sounds/ambientSounds/birds.mp3"

- name: "launch-fireplace-ambient-synapse"
  signals: {}
  neurons:
    - background_sound_player:
        state: "on"
        loop_option: "loop"
        sounds:
          - "Feu de bois": "./resources/sounds/ambientSounds/fireplace.ogg"

- name: "launch-forest-ambient-synapse"
  signals: {}
  neurons:
    - background_sound_player:
        state: "on"
        loop_option: "loop"
        sounds:
          - "Forêt": "./resources/sounds/ambientSounds/forest.mp3"

- name: "launch-rain-ambient-synapse"
  signals: {}
  neurons:
    - background_sound_player:
        state: "on"
        loop_option: "loop"
        sounds:
          - "Pluie": "./resources/sounds/ambientSounds/heavy-rain.ogg"

- name: "launch-stream-ambient-synapse"
  signals: {}
  neurons:
    - background_sound_player:
        state: "on"
        loop_option: "loop"
        sounds:
          - "Ruisseau": "./resources/sounds/ambientSounds/forest-stream.mp3"

- name: "launch-mountain-ambient-synapse"
  signals: {}
  neurons:
    - background_sound_player:
        state: "on"
        loop_option: "loop"
        sounds:
          - "Montagne": "./resources/sounds/ambientSounds/mountain-stream.mp3"

- name: "launch-ocean-ambient-synapse"
  signals: {}
  neurons:
    - background_sound_player:
        state: "on"
        loop_option: "loop"
        sounds:
          - "Océan": "./resources/sounds/ambientSounds/ocean-waves.mp3"

- name: "launch-lake-ambient-synapse"
  signals: {}
  neurons:
    - background_sound_player:
        state: "on"
        loop_option: "loop"
        sounds:
          - "Lac": "./resources/sounds/ambientSounds/seaside.mp3"

- name: "launch-water-ambient-synapse"
  signals: {}
  neurons:
    - background_sound_player:
        state: "on"
        loop_option: "loop"
        sounds:
          - "Eau": "./resources/sounds/ambientSounds/stream.ogg"

- name: "launch-storm-ambient-synapse"
  signals: {}
  neurons:
    - background_sound_player:
        state: "on"
        loop_option: "loop"
        sounds:
          - "Orage": "./resources/sounds/ambientSounds/thunderstorm.ogg"

- name: "launch-tropical-ambient-synapse"
  signals: {}
  neurons:
    - background_sound_player:
        state: "on"
        loop_option: "loop"
        sounds:
          - "Tropical": "./resources/sounds/ambientSounds/tropical-beach.mp3"

- name: "launch-wind-ambient-synapse"
  signals: {}
  neurons:
    - background_sound_player:
        state: "on"
        loop_option: "loop"
        sounds:
          - Vent: "./resources/sounds/ambientSounds/wind.ogg"

- name: "launch-boat-ambient-synapse"
  signals: {}
  neurons:
    - background_sound_player:
        state: "on"
        loop_option: "loop"
        sounds:
          - "Bateau mouillé": "./resources/sounds/ambientSounds/wood-sailboat.mp3"
```
