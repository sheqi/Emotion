#!/usr/bin/env python
from __future__ import print_function

import sys
import cv2
import socket
import numpy
from time import sleep

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65436        # The port used by the server
emotion_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def pub_file(resource, fps, loop_count):

# If we are given just a number, interpret it as a video device
    if len(resource) < 3:
        resource_name = "/dev/video" + resource
        resource = int(resource)
    else:
        resource_name = resource

    forever = (loop_count < 0)
    current_loop = 0
    while (forever or current_loop < loop_count):
        print("Trying to open resource: " + resource_name)
        cap = cv2.VideoCapture(resource)
        if not cap.isOpened():
            print("Error opening resource: " + str(resource))
            print( "Maybe opencv VideoCapture can't open it")
            exit(0)

        print("Correctly opened resource, starting to show feed.")
        rval, frame = cap.read()

        frame_num = 0
        while rval :
            #cv2.imshow("Stream: " + resource_name, frame)
            #frame = cv2.resize(frame, (960,540))
	        #cv2.Flip(frame, frame, 0);
            frame = cv2.resize(frame, (640,480))

            encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
            result, imgencode = cv2.imencode('.jpg', frame, encode_param)
            data = numpy.array(imgencode)
            stringData = data.tostring()
            emotion_sock.send( str(len(stringData)).ljust(16).encode())
            emotion_sock.send( stringData )

            rval, frame = cap.read()
            sleep(1.0/fps)
            print("publishing loop {}\t in frame{}@{}fps".format(current_loop, frame_num, fps))
            frame_num += 1
        current_loop+=1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("You must give an argument to open a video stream.")
        print("  It can be a number as video device, e.g.: 0 would be /dev/video0")
        print("  It can be a url of a stream,        e.g.: rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov")
        print("  It can be a video file,             e.g.: myvideo.mkv")
        print("Usage: python image_src.py [filename] (fps=10) (loop_count=forever)")
        exit(0)
    resource = sys.argv[1]
    fps = 10.0
    loop_count = -1
    if len(sys.argv) > 2:
        fps = float(sys.argv[2])
    if len(sys.argv) > 3:
        loop_count = int(sys.argv[3])

    emotion_sock.connect((HOST, PORT))
    pub_file(resource, fps, loop_count)
    emotion_sock.close()
