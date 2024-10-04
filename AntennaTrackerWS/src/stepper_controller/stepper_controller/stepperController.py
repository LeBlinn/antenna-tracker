#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *


class stepperControllerNode(Node):

    def __init__(self):
        super().__init__("stepper_controller")
        self.get_logger().info("Ros2")

        # Publishers
        self.position_pub = self.create_publisher(float, '/stepper/position', 10)
        self.velocity_pub = self.create_publisher(float, '/stepper/velocity', 10)
        self.acceleration_pub = self.create_publisher(float, '/stepper/acceleration', 10)
        self.is_moving_pub = self.create_publisher(float, '/stepper/is_moving', 10)
        self.engaged_pub = self.create_publisher(float, '/stepper/engaged', 10)
        self.error_pub = self.create_publisher(float, '/stepper/error_status', 10)

        # Subscribers
        self.set_velocity_sub = self.create_subscription(float, '/stepper/set_velocity', self.set_velocity_callback, 10)
        self.set_acceleration_sub = self.create_subscription(float, '/stepper/set_acceleration', self.set_acceleration_callback, 10)
        self.set_position_sub = self.create_subscription(float, '/stepper/set_position', self.set_position_callback, 10)

        # Assume you have a Phidget stepper controller object here
        self.stepper = stepperController(step_angle=1.8)

class stepperController(Stepper):

    def __init__(self, serialNumber, stepAngle, acceleration, velocityLimit, currentLimit):
        super().__init__()

        # We lose some torque with microstepping, but it's locked in by phidget. @ 1/16
        self.stepAngle = stepAngle
        self.stepsPerRevolution = (360 / self.stepAngle) * 16  # Microsteps per revolution
        self.stepsPerDegree = 16 / self.stepAngle # Microsteps per Degree

        self.setRescaleFactor(self.stepsPerDegree) # This should allow us to use normal degree's for our functions

        self.acceleration = acceleration
        self.velocityLimit = velocityLimit
        self.currentLimit = currentLimit

        self.serialNumber = serialNumber
        self.setDeviceSerialNumber() # This is one way to chose the correct board. (Phidget makes a hub as another option)
        self.openWaitForAttachment(5000)  # Call the Stepper class's method directly

        # Set Phidget-specific parameters
        self.setAcceleration(self.acceleration)
        self.setVelocityLimit(self.velocityLimit)
        self.setCurrentLimit(self.currentLimit)

        # Attach event handlers
        self.setOnAttachHandler(self.onAttach)
        self.setOnDetachHandler(self.onDetach)

    # Event handler for when the stepper is attached
    def onAttach(self, self_instance):
        print("Stepper attached!")

    # Event handler for when the stepper is detached
    def onDetach(self, self_instance):
        print("Stepper detached!")

    # Close the connection when done
    def close(self):
        self.stepper.close()


def main(args=None):
    rclpy.init(args=args) 
    node = stepperControllerNode()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == '__main__':
    main()