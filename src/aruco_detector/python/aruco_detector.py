#!/usr/bin/env python

# Not finished

import numpy as np
import cv2
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from markerlocator.msg import markerpose

class ArUcoDetector():
    def __init__(
            self,
            subscribe_topic="/image_raw",
            publish_topic="/aruco_detector/marker_pose",
            marker_id=0,
            camera_matrix=np.array([
                [448.1, 0, 376],
                [0, 448.1, 240],
                [0, 0, 1]
            ]),
            aruco_length=0.05
    ):
        self.parameters = cv2.aruco.DetectorParameters_create()
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
        self.marker_id = marker_id
        self.camera_matrix = camera_matrix
        self.aruco_length = aruco_length

        self.sub = rospy.Subscriber(
                subscribe_topic,
                Image,
                callback=self.on_new_image,
                queue_size=1
        )

        self.pub = rospy.Publisher(
                publish_topic,
                markerpose,
                queue_size=1
        )

    def on_new_image(
            self,
            frame
    ):
        corners, ids, rejected_pts = cv2.aruco.detectMarkers(
                frame, 
                self.dictionary, 
                parameters=self.parameters
        )

        if self.marker_id in ids:
            index = list(ids).index(self.marker_id)
            corners = np.array(list(corners[0][index])).astype(np.int32)

            rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(
                    corners,
                    aruco_length,
                    self.camera_matrix,
                    np.zeros(4)
            )

	    # Publish estimated pose


    



if __name__ == '__main__':
    pass
