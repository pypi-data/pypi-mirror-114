# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asrecognition']

package_data = \
{'': ['*']}

install_requires = \
['datasets>=1.10.2,<2.0.0',
 'librosa>=0.8.1,<0.9.0',
 'llvmlite>=0.36.0,<0.37.0',
 'numba>=0.53.1,<0.54.0',
 'torch>=1.9.0,<2.0.0',
 'transformers>=4.9.1,<5.0.0']

setup_kwargs = {
    'name': 'asrecognition',
    'version': '0.0.4',
    'description': 'ASRecognition: just an easy-to-use library for Automatic Speech Recognition.',
    'long_description': '# ASRecognition\n\nASRecognition: just an easy-to-use library for Automatic Speech Recognition.\n\nI have no intention of building a very complex toolkit for speech recognition here. \nIn fact, this library uses a lot of things already built by the [Hugging Face](https://huggingface.co/) (Thank you guys!). \nI just wanna have an easy-to-use interface to add speech recognition features to my apps.\nI hope this library could be useful for someone else too :)\n\nThe currently supported languages are Arabic (ar), German (de), Greek (el), English (en), Spanish (es), Persian (fa), Finnish (fi), French (fr), Hungarian (hu), Italian (it), Japanese (ja), Dutch (nl), Polish (pl), Portuguese (pt), Russian (ru), Chinese (zh-CN).\n\n# Requirements\n\n- Python 3.7+\n\n# Installation\n\n```console\n$ pip install asrecognition\n```\n\n# How to use it?\n\n```python\nfrom asrecognition import ASREngine\n\n# 1 - Load the ASR engine for a given language (on the first run it may take a while)\nasr = ASREngine("en")\n\n# 2 - Use the loaded ASR engine to transcribe a list of audio files\naudio_paths = ["/path/to/sagan.mp3", "/path/to/asimov.wav"]\ntranscriptions = asr.transcribe(audio_paths)\n\n# 3 - Voilà!\nprint(transcriptions)\n\n# [\n#  {"path": "/path/to/sagan.mp3", "transcription": "EXTRAORDINARY CLAIMS REQUIRE EXTRAORDINARY EVIDENCE"},\n#  {"path": "/path/to/asimov.wav", "transcription": "VIOLENCE IS THE LAST REFUGE OF THE INCOMPETENT"}\n# ]\n```\n# Want to help?\n\nSee the [contribution guidelines](https://github.com/jonatasgrosman/asrecognition/blob/master/CONTRIBUTING.md)\nif you\'d like to contribute to ASRecognition project.\n\nYou don\'t even need to know how to code to contribute to the project. Even the improvement of our documentation is an outstanding contribution.\n\nIf this project has been useful for you, please share it with your friends. This project could be helpful for them too.\n\nIf you like this project and want to motivate the maintainers, give us a :star:. This kind of recognition will make us very happy with the work that we\'ve done with :heart:\n\n# Citation\nIf you want to cite the tool you can use this:\n\n```bibtex\n@misc{grosman2021asrecognition,\n  title={ASRecognition},\n  author={Grosman, Jonatas},\n  publisher={GitHub},\n  journal={GitHub repository},\n  howpublished={\\url{https://github.com/jonatasgrosman/asrecognition}},\n  year={2021}\n}\n```',
    'author': 'Jonatas Grosman',
    'author_email': 'jonatasgrosman@gmail.com',
    'maintainer': 'Jonatas Grosman',
    'maintainer_email': 'jonatasgrosman@gmail.com',
    'url': 'https://github.com/jonatasgrosman/asrecognition',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
