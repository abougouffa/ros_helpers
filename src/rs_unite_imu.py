#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu
from threading import Lock

ACCEL_TOPIC_DEFAULT = "/camera/accel/sample"
GYRO_TOPIC_DEFAULT = "/camera/gyro/sample"
OUT_IMU_TOPIC_DEFAULT = "/imu_uni"

class UniteImu:
    def __init__(self):
        rospy.init_node('rs_unite_imu', anonymous=True)

        gyro_topic_name = rospy.get_param("~gyro_topic", GYRO_TOPIC_DEFAULT)
        accel_topic_name = rospy.get_param("~accel_topic", ACCEL_TOPIC_DEFAULT)
        out_imu_topic_name = rospy.get_param("~out_imu_topic", OUT_IMU_TOPIC_DEFAULT)
        
        rospy.Subscriber(accel_topic_name, Imu, self._callback_accel)
        rospy.Subscriber(gyro_topic_name, Imu, self._callback_gyro)

        self.pub = rospy.Publisher(out_imu_topic_name, Imu, queue_size=100)

        self._accel_data = Imu()
        self._accel_mutex = Lock()

        while not rospy.is_shutdown():
            pass

    def _callback_accel(self, data):
        self._accel_mutex.acquire()
        self._accel_data = data
        self._accel_mutex.release()

    def _callback_gyro(self, data):
        self._accel_mutex.acquire()
        data.linear_acceleration = self._accel_data.linear_acceleration
        data.linear_acceleration_covariance = self._accel_data.linear_acceleration_covariance
        self._accel_mutex.release()

        self.pub.publish(data)

if __name__ == '__main__':
    try:
        UniteImu()
    except rospy.ROSInterruptException:
        pass
