#!/usr/bin/env python

import rospy                                    #rospy needs to be imported in all nodes.
import struct
from stereo_msgs.msg import DisparityImage
from std_msgs.msg import Header                 #This allows us to use the Header message hopefully.

def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + " Header data %s", data.header)
    #rospy.loginfo(data.image.height)
    
    pixel_list = (list(struct.unpack('1241632f', data.image.data)))
    #Converting raw bytes to float pixel values.

    pixel_list = [x for x in pixel_list if x >= 0]
    #List comp to remove all but positive disparity values.

    print(max(pixel_list))
    
    
    ave_pixel_dis = (sum(pixel_list)/len(pixel_list))

    f = data.f
    T = data.T
    
    ave_scene_depth = (f * T) / ave_pixel_dis

    print('Z ave: ' + str(round(ave_scene_depth, 3)))

    print('min_dis: ' + str(data.min_disparity))
    print('max_dis: ' + str(data.max_disparity))
    print('focal  : ' + str(data.f))
    print('base   : ' + str(data.T))
    # Z = fT/d, depth is equal to focal length*baseline / disparity.

def listener():
    rospy.init_node('repeater', anonymous=True)
    # This initializes the node named 'talker'. Cannot have any '/'. anon flag adds numbers to the end
    # of the node name to ensure it is unique.

    rospy.Subscriber('/camera/disparity', DisparityImage, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()