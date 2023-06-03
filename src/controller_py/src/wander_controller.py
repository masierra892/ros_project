#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import threading
import enum

class RotationDirection(enum.Enum):
    NOT_DEFINED = 0
    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2

class WanderController(threading.Thread):

    def __init__(self, minimum_acceptable_range: float) -> None:

        threading.Thread.__init__(self)
        rospy.init_node("python_wander_controller")
        self.sensor_scan_sub = rospy.Subscriber("/scan", LaserScan, self.scanCallback)
        self.twist_publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        self.obstacle_ahead = False
        self.minimum_acceptable_range = minimum_acceptable_range
        self.angle_delta = 15
        self.current_ranges = tuple()
        self.minimum_distance = None
        self.minimum_distance_angle = None
        self.rotation = RotationDirection.NOT_DEFINED
        self.rate = rospy.Rate(10)
        rospy.loginfo("Python Controller has been initialized")
        
    def scanCallback(self, msg : LaserScan) -> None:

        self.current_ranges = msg.ranges
        self.minimum_distance = min(self.current_ranges)
        self.minimum_distance_angle = self.current_ranges.index(self.minimum_distance)
        rospy.loginfo("Values Minimum Range: %f Angle: %f Type: %s", self.minimum_distance, self.minimum_distance_angle, str(type(self.current_ranges)))

    def define_rotation_direction(self, minimum_distance: float, minimum_range_angle: float, whole_ranges: tuple, angle_delta: int) -> RotationDirection:

        if minimum_distance is None or minimum_range_angle is None or len(whole_ranges) == 0:
            return RotationDirection.NOT_DEFINED
        
        angle_right = minimum_range_angle + angle_delta
        angle_left = minimum_range_angle - angle_delta

        distance_right = whole_ranges[angle_right]
        distance_left = whole_ranges[angle_left]

        if distance_left < minimum_distance < distance_right:
            return RotationDirection.CLOCKWISE
        elif distance_left > minimum_distance > distance_right:
            return RotationDirection.COUNTERCLOCKWISE
        else:
            return RotationDirection.NOT_DEFINED

    def wanderFunction(self) -> None:

        while not rospy.is_shutdown():

            try:

                if self.minimum_distance is None or self.minimum_distance_angle is None:
                    continue
            
                if not self.obstacle_ahead:
                    if (self.minimum_distance < self.minimum_acceptable_range):
                        self.obstacle_ahead = True

                else:
                    if (self.minimum_distance > self.minimum_acceptable_range):
                        self.obstacle_ahead = False


                twist_to_publish = Twist()

                if not self.obstacle_ahead:
                    twist_to_publish.linear.x = 0.5
                    twist_to_publish.angular.z = 0.0
                else:
                    rotation_direction = self.define_rotation_direction(self.minimum_distance, self.minimum_distance_angle, self.current_ranges, self.angle_delta)
                    if rotation_direction == RotationDirection.CLOCKWISE or rotation_direction == RotationDirection.NOT_DEFINED:
                        sign = 1
                    elif rotation_direction == RotationDirection.COUNTERCLOCKWISE:
                        sign = -1

                    twist_to_publish.linear.x = 0.0
                    twist_to_publish.angular.z = sign*0.5

                self.twist_publisher.publish(twist_to_publish)

                self.rate.sleep()

            except Exception as e:
                rospy.logerr("Error has occured : %s", str(e))

            except KeyboardInterrupt:
                rospy.logwarn("Keyboard Interrup: Stop Publishing Commands")
                break

    def run(self):
        self.wanderFunction()
        
if __name__ == '__main__':
    
    controller = WanderController(0.8)
    controller.start()
    rospy.spin()
    controller.join()

