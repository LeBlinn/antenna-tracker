from stepper_controller.srv import getPosition, setPosition

def setup_position_services(node):
    node.get_position_srv = node.create_service(GetPosition, '/stepper/get_position', get_position_callback)
    node.set_position_srv = node.create_service(SetPosition, '/stepper/set_position', set_position_callback)

def get_position_callback(request, response):
    # Logic to handle the service request
    response.position = node.position
    return response
