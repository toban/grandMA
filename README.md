# grandMA
GrandMA - Sample &amp; Preset Manager for Bastl Instruments GrandPA

- automagically names samples added correctly
- converts anything using ffmpeg to 16bit mono 22Khz
- audio playback and waveform preview
- freesound.org search and browse (requires your own api key)

# installation
- install ffmpeg make sure it's runnable from shell
- pip install requirements.txt
- sudo apt-get install python3-pil.imagetk
- for using the freesound integration you need an .env file with the following set
```
FREESOUND_API_KEY=<get from freesound.org>
FREESOUND_ACCESS_TOKEN=<oauth from freesound.org>
FREESOUND_CLIENT_ID=
FREESOUND_AUTH_CODE=
```

# usage
- python main.py (might wanna run with sudo)
- select SD-card path

# todo
- preset editor does not work yet
- sample editing / offsets
- why not add support for all ffmpeg filters

