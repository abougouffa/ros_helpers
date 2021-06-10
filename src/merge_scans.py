#!/usr/bin/env python2
# license removed for brevity
import rospy
from sensor_msgs.msg import LaserScan

SOURCE_TOPIC = "/laser_scanner/scan"
TOPIC_NAME = "/scan"


class MergeScans:
    def __init__(self):
        rospy.init_node('scan_merge', anonymous=True)

        pub_topic_name = rospy.get_param("~topic_name", TOPIC_NAME)
        source_topic = rospy.get_param("~source_topic", SOURCE_TOPIC)

        rospy.Subscriber(source_topic, LaserScan, self._callback)

        self.pub = rospy.Publisher(pub_topic_name, LaserScan, queue_size=10)

        self.ready_to_publish = False
        self.merged_msg = LaserScan()
        self.ready_msg = None

        while not rospy.is_shutdown():
            if self.ready_to_publish:
                self.ready_to_publish = False
                self.pub.publish(self.ready_msg)

    def _callback(self, data):
        if data.angle_min < -2.:  # new cycle
            self.merged_msg = data
        elif self.merged_msg != None:
            self.merged_msg.angle_max = data.angle_max
            self.merged_msg.header = data.header
            self.merged_msg.ranges += data.ranges
            self.merged_msg.intensities += data.intensities

        if data.angle_max > 2.:  # complete range -> publish
            self.ready_to_publish = True
            self.ready_msg = self.merged_msg
            self.merged_msg = LaserScan()


if __name__ == '__main__':
    try:
        MergeScans()
    except rospy.ROSInterruptException:
        pass
