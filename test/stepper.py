from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *

# Global Values
STEP_ANGLE = 200 # Stepper motor specific
VOLTAGE = 5 # Stepper motor specific
CURRENT_LIMIT = 1 # Stepper motor specific

class StepperController(Stepper):

    def __init__(self, serialNumber, stepAngle, acceleration, velocityLimit, currentLimit):
        super().__init__()  # Call the parent class (Stepper) constructor

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

    # Move by X steps
    def moveBySteps(self, steps):
        self.stepper.setTargetPosition(steps)
        self.stepper.setEngaged(True)

        # wait for movement to complete
        while self.stepper.getIsMoving():
            pass  # Using Time could reduces CPU usage, but idk how fast we gotta react.

    # Convert degrees to steps
    # I'd prefer to avoid this as it's uneccesary overhead, but it makes it easier to code
    def degreesToSteps(self, degrees):
        return int((degrees / 360) * self.stepsPerRevolution)

    # Move by X degrees
    def moveByDegrees(self, degrees):
        steps = self.degreesToSteps(degrees)
        self.stepper.setTargetPosition(steps)
        self.stepper.setEngaged(True)

        # wait for movement to complete
        while self.stepper.getIsMoving():
            pass  # Using time could reduces CPU usage, but idk how fast we gotta react.

    # Close the connection when done
    def close(self):
        self.stepper.close()

def main():
    # Initialize the stepper controller
    stepper1 = StepperController(serialNumber, stepAngle, acceleration, velocityLimit, currentLimit)

    # Engage Motor
    stepper1.setEngaged(False)

    # Move to a target position by degrees (e.g., 90 degrees)
    stepper1.moveByDegrees(90)

    # Disengage after moving
    stepper1.setEngaged(False)

    # Close the stepper controller when done
    stepper1.close()

if __name__ == "__main__":
    main()