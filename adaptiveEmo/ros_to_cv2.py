#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Start the emotion server first, and then start this file

import rospy
import cv2
import socket
from sensor_msgs.msg import Image
import cv_bridge
import numpy
display = False

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65436        # The port used by the server
emotion_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def callback(msg):
    img = cv_bridge.CvBridge().imgmsg_to_cv2(msg, "bgr8")

    if display:
        cv2.imshow("emotion", img)
        cv2.waitKey(1)

    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    result, imgencode = cv2.imencode('.jpg', img, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()
    emotion_sock.send( str(len(stringData)).ljust(16))
    emotion_sock.send( stringData )
    #emotion_sock.sendall(encoded_img)
            

def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('emotion_detection', anonymous=True)

    rospy.Subscriber('usb_cam/image_raw', Image, callback, queue_size=1)

    emotion_sock.connect((HOST, PORT))
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
    cv2.destroyAllWindows()
    emotion_sock.close()

if __name__ == '__main__':
    listener()
