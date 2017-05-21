#!/usr/bin/env python3
'''
1. listen command to generate_hashtag
2. scan newsfeed (vk) for posts with the hashtag
'''

import rospy
from coffebot.social.vk import VkNeewsfeedScanner
from std_msgs.msg import Bool, String
import time

if __name__ == '__main__':
    rospy.init_node('social_vk')

    if rospy.has_param('vk_api_access_key'):
        newsfeed_scanner = VkNeewsfeedScanner(access_token=rospy.get_param('vk_api_access_key'), required_hashtag='#funrobots')

        hashtag_publisher = rospy.Publisher('/social/vk/newsfeed_scanner/hashtag', String, queue_size=1)
        give_candy_publisher = rospy.Publisher('/social/vk/newsfeed_scanner/give_candy', Bool, queue_size=1)

        def callback_scan_command(data: Bool):
            if data.data is True:
                hashtag = newsfeed_scanner.generate_hashtag()
                hashtag_publisher.publish(hashtag)
                hashtag_posted_in_vk = newsfeed_scanner.listen(hashtag, 120)
                if hashtag_posted_in_vk is True:
                    give_candy_publisher.publish(True)

        rospy.Subscriber('/social/vk/newsfeed_scanner/scan_command', Bool, callback_scan_command)

        while True:
            try:
                rospy.get_master().getPid()
            except:
                break

            time.sleep(0.1)