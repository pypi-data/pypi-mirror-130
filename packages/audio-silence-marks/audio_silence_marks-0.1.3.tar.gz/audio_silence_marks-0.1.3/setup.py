# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['audio_silence_marks', 'audio_silence_marks.targets']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['audio_silence_marks = audio_silence_marks.cli:main']}

setup_kwargs = {
    'name': 'audio-silence-marks',
    'version': '0.1.3',
    'description': 'Tool for creating silence marks for audio files',
    'long_description': '# Create silence marks for your audio files\n\nCreates a list of "silences" timecodes in audio files using **FFmpeg** and its filter \n[silencedetect](https://ffmpeg.org/ffmpeg-filters.html#silencedetect).\n\nCurrently, only [Audipo](https://play.google.com/store/apps/details?id=jp.ne.sakura.ccice.audipo&hl=en_US&gl=US)\nplayer marks format is supported.\n\n## Prerequisites\n\n- [Python 3.8+](https://www.python.org/)\n- [FFmpeg](https://ffmpeg.org/)\n- Linux (haven\'t tested on Windows/Mac yet)\n\n## Installation\n\n```\n$ pip install audio_silence_marks\n```\n\n## Usage\n\nRun the tool against one file or a directory tree:\n\n```\n$ audio_silence_marks . file.mp3 > marks.audipomark\n$ audio_silence_marks . \'**/*.mp3\' > marks.audipomark\n```\n\nThen upload this file to your phone\'s directory `Interal Storage/Audipo/Mark`, e.g.: \n```\n$ adb push marks.audipomark /storage/emulated/0/Audipo/Mark/\n```\n\nOpen your Audipo player, go to `Menu > Preferences` and click on `Import all marks` item.\nRestart the player.\n\n## Result\n\nExample:\n\n|                                                   Unit 23                                                    |                         Unit 24                                                                              |\n|:------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------------------------:|\n| ![image](https://user-images.githubusercontent.com/114060/99715000-5cd86780-2ab7-11eb-8707-b7235bebebf3.png) | ![image](https://user-images.githubusercontent.com/114060/99714622-dc196b80-2ab6-11eb-977d-cd3d58ff1786.png) | \n\n## Processing audiobooks\n\nThe script accepts two parameters which highly affect the output, i.e. the amount and the positions of the marks.\nThey are: \n\n- `--noise`, `-n` - noise tolerance in decibels (negated for convenience).\n\n  Acts like a reverse noise gate, passing through parts with the volume below defined. The default value is `50` (which makes `-50dB`).\n\n- `--duration`, `-d` - duration of silence in milliseconds. \n\n  Sets the minimum duration of silence. The default value is `1000` (ms).\n\nThus, even a book with some background music which level is less than of the speech, can be successfully marked by `--noise` parameter tuning.\n\nAn example profile for a regular book:\n\n```\naudio_silence_marks -d 400 -n 30 . book.mp3 > marks.audipomark \n```\n\nThis sets `-30dB` noise level and `400` millisecond minimum silence duration.\n\n## Docs\n\n```\n$ audio_silence_marks --help\n\nUsage: audio_silence_marks [OPTIONS] PATH GLOB\n\n  Processes audio files using FFmpeg filter silencedetect and outputs Audipo\n  markers JSON with the list of spots placed in the middle of silence\n  intervals.\n\n  More info on using GLOBS: https://docs.python.org/3.8/library/glob.html\n\nArguments:\n  PATH  is a path to files. E.g: "."  [required]\n  GLOB  argument is a pattern for selecting files. E.g.: \'**/*.mp3\'\n        [required]\n\n\nOptions:\n  -t, --target [audipo]           Target format for marks.  [default: audipo]\n  -n, --noise INTEGER             Maximum volume of the noise treated as\n                                  silence in -dB  [default: 50]\n\n  -d, --duration INTEGER          Minimum length of the silent interval in\n                                  milliseconds [default: 1000]\n\n  -l, --list                      Simply lists matched files. Useful for GLOB\n                                  debugging.  [default: False]\n\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n\n  --help                          Show this message and exit.\n```\n',
    'author': 'OnkelTem',
    'author_email': 'aneganov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/OnkelTem/audio_silence_marks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
