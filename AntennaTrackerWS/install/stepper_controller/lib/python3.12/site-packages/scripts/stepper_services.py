from std_msgs.msg import String
from stepper_controller.srv import getPosition, addPositionOffset, getVelocity, getAcceleration, setAcceleration, getEngaged, setEngaged

def setup_services(self):

    # Services
    self.get_position_srv = self.create_service(getPosition, '/stepper/get_position', get_position_callback)
    self.add_position_offset_srv = self.create_service(addPositionOffset, '/stepper/add_position_offset', add_position_offset_callback)

    self.get_acceleration_srv = self.create_service(getAcceleration, '/stepper/get_acceleration', get_acceleration_callback)
    self.set_acceleration_srv = self.create_service(setAcceleration, '/stepper/set_acceleration', set_acceleration_callback)

    self.get_velocity_srv = self.create_service(getVelocity, '/stepper/get_velocity', get_velocity_callback)

    self.get_engaged_srv = self.create_service(getEngaged, '/stepper/get_engaged', get_engaged_callback)
    self.set_engaged_srv = self.create_service(setEngaged, '/stepper/set_engaged', set_engaged_callback)

    # currently baked in code (or default values), but could be a service one day - The List
    # setCurrentLimit, setMinVelocity, setMaxVelocity

    # Add a get info on board service? Such as, board serial number
    return

def get_position_callback(self, request, response):
    try:
        response.position = self.stepper.getPosition()
        response.success = True
    except self.PhidgetException as e:
        errorMsg = str(e)
        msg = String()
        msg.data = errorMsg
        self.error_pub.publish(msg)
        response.position = 0.0 # default value (on error)
        response.success = False
    return response

def add_position_offset_callback(self, request, response):
    try:
        self.stepper.addPositionOffset(request.offset)
        response.success = True
    except self.PhidgetException as e:
        errorMsg = str(e)
        msg = String()
        msg.data = errorMsg
        self.error_pub.publish(msg)
        response.success = False
    return response

def get_acceleration_callback(self, request, response):
    try:
        response.acceleration = self.stepper.getAcceleration()
        response.success = True
    except self.PhidgetException as e:
        errorMsg = str(e)
        msg = String()
        msg.data = errorMsg
        self.error_pub.publish(msg)
        response.acceleration = 0.0 # default value (on error)
        response.success = False
    return response

def set_acceleration_callback(self, request, response):
    try:
        self.stepper.setAcceleration(request.acceleration)
        response.success = True
    except self.PhidgetException as e:
        errorMsg = str(e)
        msg = String()
        msg.data = errorMsg
        self.error_pub.publish(msg)
        response.success = False
    return response

def get_velocity_callback(self, request, response):
    try:
        response.velocity = self.stepper.getVelocity()
        response.success = True
    except self.PhidgetException as e:
        errorMsg = str(e)
        msg = String()
        msg.data = errorMsg
        self.error_pub.publish(msg)
        response.velocity = 0.0 # default return value (on error)
        response.success = False
    return response

def get_engaged_callback(self, request, response):
    try:
        response.engaged = self.stepper.getEngaged()
        response.success = True
    except self.PhidgetException as e:
        errorMsg = str(e)
        msg = String()
        msg.data = errorMsg
        self.error_pub.publish(msg)
        response.engaged = False # default return value (on error)
        response.success = False
    return response

def set_engaged_callback(self, request, response):
    try:
        self.stepper.setEngaged(request.engaged)
        response.success = True
    except self.PhidgetException as e:
        errorMsg = str(e)
        msg = String()
        msg.data = errorMsg
        self.error_pub.publish(msg)
        response.success = False
    return response
