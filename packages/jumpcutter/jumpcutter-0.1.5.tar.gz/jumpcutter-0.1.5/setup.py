# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jumpcutter']

package_data = \
{'': ['*']}

install_requires = \
['moviepy>=1.0.3,<1.1.0', 'tqdm>=4.60.0,<4.61.0']

entry_points = \
{'console_scripts': ['jumpcutter = jumpcutter.__main__:main']}

setup_kwargs = {
    'name': 'jumpcutter',
    'version': '0.1.5',
    'description': 'Jumpcut silent parts of your videos automagically',
    'long_description': '## What is jumpcutter?\n\nJumpcutter is a program that is written in Python to automatically jump-cut silent parts of your videos.\nThe purpose here is to ease your post recording work.\n\nCheck out [the medium post](https://medium.com/@emkademy/how-to-jump-cut-silent-parts-of-your-videos-automatically-with-python-2e4b96320dc1)\nfor more information.\n\n## Installation\nYou can install jumpcutter by simply:\n\n```bash\npip install jumpcutter \n```\n\n## Demo\n\n[![Watch the video](https://img.youtube.com/vi/UDjzm_lzWOA/hqdefault.jpg)](https://youtu.be/UDjzm_lzWOA)\n\n## How to run it?\nThere are 11 command line arguments you can run the program with. \nBefore explaining them, I would like to say that most of these parameters \nhave a default value that “just works”. So, if you don’t want you don’t need to specify \n(or know) almost any of these parameters. You will be just fine with the default values.\n\n1. `--input`, `-i`: Path to the video that you want to jump-cut.\n2. `--output`, `-o`: Path to where you want to save the output video.\n3. `--magnitude-threshold-ratio`, `-m`: The percentage of the maximum value of your audio signal that you would like to \n     consider as silent a signal (default: 0.02).\n4. `--duration-threshold`, `-d`: Minimum number of required seconds in silence to cut it out. For example if this parameter \n     is 0.5, it means that the silence parts have to last minimum 0.5 seconds, otherwise they won\'t be jump-cut (default: 0.5).\n5. `--failure-tolerance-ratio`, `-f`: Most of the times, there are 44100 audio signal values in 1 second of a video. \n     Let\'s say the "--duration-threshold" was set to 0.5. This means that, we need to check minimum 22050 signal \n     values to see if there is a silent part of not. What happens if we found 22049 values that we consider as silent, \n     but there is 1 value that is above our threshold. Should we just throw this part of the video and consider it as a \n     loud signal? I think we shouldn\'t. This parameter leaves some room for failure, it tolerates high signal values until \n     some point. Let\'s say it is set to 0.1, it means that 10% of the signal that is currently being investigated can \n     have values that are higher than our threshold, but they are still going to be considered as a silent part (default: 0.1).\n6. `--spaces-on-edges`, `-s`: Leaves some space on the edges of silence cut. E.g. if it is found that there is \n     silence between 10th and 20th second of the video, then instead of cutting it out directly, we cut out \n     (10+space_on_edges)th and (20-space_on_edges)th seconds of the clip (default: 0.1).\n7. `--silence-part-speed`, `-x`: If this parameter is given, instead of cutting the silent parts out, the script will \n     speed them up "x" times.\n8. `--min-loud-part-duration`, `-l`: If this parameter is given, loud parts of the video that are shorter then this \n     parameter will also be cut.\n9. `--cut`, `-c`: If you want, you can also cut voiced parts of the video (to have some fun :)). There are 3 choices \n     you can make for this parameter: `silent`, `voiced`, `both`. If you choose `silent`, silent parts of the video will\n     be cutted; if you choose `voiced`, voiced parts of the video will be cutted; if you choose `both` 2 videos will be\n     saved: 1 for the silent parts, 1 for the voiced parts (default: silent).\n10. `--codec`: Codec to use for image encoding. Can be any codec supported by ffmpeg. If the filename \n     has extension ‘.mp4’, ‘.ogv’, ‘.webm’, the codec will be set accordingly, but you can still set\n     it if you don’t like the default. For other extensions, the output filename must be set accordingly. \n     Check [here](https://zulko.github.io/moviepy/ref/VideoClip/VideoClip.html#moviepy.video.compositing.CompositeVideoClip.CompositeVideoClip.write_videofile)\n11. `bitrate`: Desired bitrate of the output video. Leave blank if you don\'t know what this is.\n     \n## Examples of running the program\n\n```bash\n# The simplest way you can run the program\njumpcutter -i input_video.mp4 -o output_video.mp4\n# If you want, you can also set the other parameters that was mentioned\njumpcutter -i input_video.mp4 -o output_video.mp4 -m 0.05 -d 1.0 -f 0.2 -s 0.2 -x 2000 -l 1.0 -c both\n```\n',
    'author': 'Kivanc Yuksel',
    'author_email': 'emkademy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kivancyuksel/jumpcutter.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
