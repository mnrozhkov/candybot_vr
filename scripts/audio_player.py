#!/usr/bin/env python3

'''
play audio node
'''

import rospy
import std_msgs
from coffebot.msg import Audio

from coffebot.audio.player import Player
from coffebot.audio.utils import audio_format_converter
import io

from coffebot.topic_controller import Lock

import time


if __name__ == '__main__':

    rospy.init_node('audio_player')

    player = Player()

    lock_speech = Lock()
    rospy.Subscriber('speech_audio', Audio, lock_speech.callback)
    print('play audio start')

    def callback_audio(data):
        pass

    rospy.Subscriber('play_audio', std_msgs.msg.String, callback_audio)

    while True:
        try:
            rospy.get_master().getPid()
        except:
            break

        msg = lock_speech.message
        if msg is not None:
            wav_bytes = msg.content
            wav_source = io.BytesIO(wav_bytes)
            wav_source.seek(0)
            player.play_audio(wav_source)

        if lock_speech.message == msg:
            lock_speech.message = None
        time.sleep(0.5)
