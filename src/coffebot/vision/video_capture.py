#!/usr/bin/env python3
import sys
sys.path.insert(1,'/usr/local/lib/python3.5/dist-packages')

import cv2
import numpy
from typing import List
import ffmpy

import time

import logging
import os
LOG_FOLDER = 'logs'
if os.path.exists(LOG_FOLDER) is False:
    os.mkdir(LOG_FOLDER)

logging.basicConfig(filename=LOG_FOLDER + '/' + __name__ + '.log', format='[%(asctime)s] %(message)s\n\n',
                    level=logging.DEBUG)


def create_video(frames: List[numpy.ndarray], video_name_with_extension: str) -> str or None:
    '''
    1. takes frames list and video file name
    2. saves frames in avi file
    '''

    try:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(video_name_with_extension, fourcc, 8.0, (640,480))

        for frame in frames:
            out.write(frame)
        out.release()
        return video_name_with_extension
    except Exception as e:
        logging.error(str(e))
        return None


def merge_audio_video(wav_file_name: str, avi_file_name: str, audio_video_file_name: str) -> str or None:
    '''
    1. takes names of .wav and .avi file
    2. merges them into one file
    '''

    try:
        ffmpy.FFmpeg(inputs={wav_file_name: None, avi_file_name: None}, outputs={audio_video_file_name: None}).run()
        return audio_video_file_name
    except Exception as e:
        logging.error(str(e))
        return None
