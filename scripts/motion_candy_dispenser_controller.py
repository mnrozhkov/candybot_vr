#!/usr/bin/env python3

import rospy
from motion.candy_dispenser.candy_dispenser_controller import Dispenser
import serial
from candybot_v2.msg import SmileDetected, FaceFeatures
from std_msgs.msg import Bool

import time


from pathlib import Path
TOP = Path(__file__).resolve().parents[1].as_posix()
import os

from utils import app_logger
log_folder  = TOP + '/logs'
if os.path.exists(log_folder) is False:
    os.mkdir(log_folder)

log_file = log_folder + '/' + __file__.split('/')[-1] + '.info'
logger = app_logger.setup_logger('candybot', filename=log_file)

TIMEOUT = 0.4
DISPENSER_ROTATES = False

#ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=TIMEOUT)
dispenser = Dispenser(SERVO_CHANNEL=4)


def rotate_dispenser() -> bool:
    '''
    rotate dispenser until candy is gave
    '''

    DISPENSER_ROTATES = True

    start = time.time()
    candy_is_gave = False
    dispenser.run()

    while time.time() - start < TIMEOUT: #rotate until timeout
        # if ser.read(4) == b'true': #if candy sensor sent true break cycle
        #     candy_is_gave = True
        #     break
        pass

    dispenser.stop()
    DISPENSER_ROTATES = False
    logger.info('give_candy')
    return candy_is_gave #return candy dispensing result


def callback_smile_detected(data: SmileDetected):
    if DISPENSER_ROTATES is False and data.detected is True:
        rotate_dispenser()


def callback_positive_emotions_detected(data: FaceFeatures):
    print('emotions!')
    if 'happy' in data.emotions or 'surprise' in data.emotions:
        print('positive emotion!')
        if DISPENSER_ROTATES is False:
            print('rotate!')
            give_candy_result = rotate_dispenser()
            print(give_candy_result)


def callback_vk_topic_published(data: Bool):
    if DISPENSER_ROTATES is False and data.data is True:
        rotate_dispenser()


def callback_twitter_topic_published(data: Bool):
    if DISPENSER_ROTATES is False and data.data is True:
        rotate_dispenser()


def callback_action_give_candy(data: Bool):
    if DISPENSER_ROTATES is False and data.data is True:
        rotate_dispenser()


if __name__ == '__main__':
    rospy.init_node('motion_candy_dispenser_controller')

    #subscribers for smile detected and social give candy topic
    smile_detected_subscriber = rospy.Subscriber('/vision_face_tracking/smile_detected', SmileDetected, callback_smile_detected)
    #face_features_subscriber = rospy.Subscriber('/vision_face_recognition/face_info', FaceFeatures, callback_positive_emotions_detected)
    vk_topic_published_sub = rospy.Subscriber('/social/vk/newsfeed_scanner/give_candy', Bool, callback_vk_topic_published)
    twitter_topic_published_sub = rospy.Subscriber('/social/twitter/code_scanner/give_candy', Bool, callback_twitter_topic_published)
    action_give_candy_sub = rospy.Subscriber('/action_manager/give_candy', Bool, callback_action_give_candy)

    last_give_candy_time = time.time()

    while True:
        try:
            rospy.get_master().getPid()
        except:
            break
        if time.time() - last_give_candy_time >= 60:
            if DISPENSER_ROTATES is False:
                rotate_dispenser()
                last_give_candy_time = time.time()
        time.sleep(0.1)
