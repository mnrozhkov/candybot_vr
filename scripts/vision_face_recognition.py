#!/usr/bin/env python3

'''
face recognition node
'''

import rospy
from candybot_v2.msg import FaceFeatures, SmileDetected
import ros_numpy
from sensor_msgs.msg import Image

from vision.utils import image_format_converter
#from vision.utils import algorithmia
from vision.utils import findface

import time

from utils.topic_controller import Lock

import sys
sys.path.insert(1, '/usr/local/lib/python3.5/dist-packages')
import cv2

import os
PHOTO_SAVE_PATH = 'photos'
if os.path.exists(PHOTO_SAVE_PATH) is False:
    os.mkdir(PHOTO_SAVE_PATH)


if __name__ == '__main__':

    rospy.init_node('vision_face_recognition')

    if rospy.has_param('findface_token'):
        findface.token=rospy.get_param('findface_token')
        face_info_publisher = rospy.Publisher('/vision_face_recognition/face_info', FaceFeatures, queue_size=1)
        smile_detected_publisher = rospy.Publisher('/vision_face_tracking/smile_detected', SmileDetected, queue_size=1)

        lock_recognize = Lock()
        rospy.Subscriber('/vision_face_tracking/face_image', Image, lock_recognize.callback)
        print('vision face recognition start')

        while True:
            try:
                rospy.get_master().getPid()
            except:
                break

            face_image_msg = lock_recognize.message
            #print('face_image for recognition recieved, type = ', type(face_image_msg))
            if isinstance(face_image_msg, Image):
                face_image = ros_numpy.numpify(face_image_msg)
                if face_image is not None:

                    #search other features: emotions, gender, age
                    binary_face_image = image_format_converter.ndarray2format(face_image)
                    face_features = findface.detect_closest_face(binary_face_image)
                    #print(face_features_msg)
                    print('face features request result: ', face_features)
                    if face_features is not None:
                        cv2.imwrite(PHOTO_SAVE_PATH + '/' + time.ctime() + '.png', face_image)
                        face_features_msg = FaceFeatures()
                        face_features_msg.emotions = face_features['emotions']
                        face_features_msg.gender = face_features['gender']
                        face_features_msg.age = face_features['age']

                        if 'happy' in face_features['emotions'] or 'surprise' in face_features['emotions']:
                            smile_detected_msg = SmileDetected(detected=True)
                            smile_detected_publisher.publish(smile_detected_msg)

                        face_info_publisher.publish(face_features_msg)
                    else:
                        cv2.imwrite(PHOTO_SAVE_PATH + '/' + time.ctime() + 'nonemotions.png', face_image)

            if lock_recognize.message == face_image_msg:
                lock_recognize.message = None
            time.sleep(0.5)
