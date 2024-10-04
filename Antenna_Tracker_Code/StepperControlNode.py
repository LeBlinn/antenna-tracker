import rospy
from phidget22.Phidget import *
from phidget22.Devices.Stepper import *

class StepperMotorController:
    def __init__(self):
        rospy.init_node('stepper_motor_controller')
        self.stepper = Stepper()
        self.stepper.openWaitForAttachment(5000)
        rospy.Subscriber('/stepper_motor/position', Float64, self.set_position)
        self.pub = rospy.Publisher('/stepper_motor/status', Float64, queue_size=10)

    def set_position(self, position):
        self.stepper.setTargetPosition(position.data)
        self.stepper.setEngaged(True)

    def publish_status(self):
        while not rospy.is_shutdown():
            current_position = self.stepper.getPosition()
            self.pub.publish(current_position)
            rospy.sleep(0.1)

if __name__ == '__main__':
    try:
        controller = StepperMotorController()
        controller.publish_status()
    except rospy.ROSInterruptException:
        pass
