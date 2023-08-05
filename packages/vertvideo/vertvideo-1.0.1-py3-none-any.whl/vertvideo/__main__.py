import sys
import argparse
import os
from moviepy.editor import *
import re

import shutil


def clean_string(string):
    return re.sub('[^a-z0-9]', '', str(string.lower()))


def get_index_or_default(array, index, default=None):
    try:
        val = array[index]
        if not val:
            return default
    except IndexError:
        return default


def main():

    assert len(
        sys.argv) < 3, f'{__file__} arguments must not exceed 2 arguments, received {len(sys.argv)}'
    assert len(
        sys.argv) > 0, f'{__file__} must be called with atleast 1 argument (input), received {len(sys.argv)}'

    # FOR SOME REASON THE PATH OF THE SCRIPT IS PASSED IN SYSARGV
    if 'vertvideo' in sys.argv[0]:
        del sys.argv[0]

    input = sys.argv[0]
    if not os.path.isdir(input):
        raise NotADirectoryError(f'{input} is not a directory.')

    format = clean_string(
        string=get_index_or_default(
            array=sys.argv,
            index=1,
            default='mp3'
        )
    )

    failed = []

    files = os.listdir(input)
    for file in files:
        filename = file.replace(' ', '_').split('.')[0]
        try:
            video = VideoFileClip(input + '/' + file)
            video.audio.write_audiofile(input + f'/{filename}.{format}')

        except OSError as e:
            failed.append(file)
            print(f'{file} has failed.')
            continue

        except KeyError:
            print(f'{file} is not a video.')
            continue

    else:
        if len(files) > 0:
            print(f'Conversion has ended with {len(failed)} attempts.')
            return

        print('Empty folder detected.')


if __name__ == "__main__":
    main()
