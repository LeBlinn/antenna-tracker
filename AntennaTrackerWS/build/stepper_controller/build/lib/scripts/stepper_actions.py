from rclpy.action import ActionServer, CancelResponse, GoalResponse
from stepper_controller.action import moveToTargetPosition

def setup_actions(self):

    # Actions
    self.move_to_target_position_act = ActionServer( #shorthand MTTPA
        self,
        moveToTargetPosition,
        '/stepper/move_to_target_position',
        self.mttpa_execute_callback, # execute action
        goal_callback=self.mttpa_goal_callback, # Goal acceptance
        cancel_callback=self.mttpa_cancel_callback # cancel action
    )
    return

# Action callbacks
def mttpa_execute_callback(self, goal_handle):
    self.get_logger().info('Executing goal...')

    # Get the target position from the goal
    target_position = goal_handle.request.target_position
        
    # Initialize feedback and result
    feedback_msg = moveToTargetPosition.Feedback()
    feedback_msg.current_position = 0.0

    # Probably want a loop here
    if goal_handle.is_cancel_requested:
        self.get_logger().info('Goal canceled')
        goal_handle.canceled()
        return target_position.Result()

    # Publish feedback
    self.get_logger().info(f'Feedback: current_position = {feedback_msg.current_position}')
    goal_handle.publish_feedback(feedback_msg)

    # Goal succeeded
    self.get_logger().info('Goal succeeded')
    goal_handle.succeed()

    # Prepare and return the result
    result = moveToTargetPosition.Result()
    result.success = True
    result.final_position = feedback_msg.current_position
    return result
    
def mttpa_goal_callback(self, goal_request):
    self.get_logger().info('Received goal request for target position: %f' % goal_request.target_position)
        
    # Add logic for if target position is within valid range
    if 0 <= goal_request.target_position <= 100:
        self.get_logger().info('Goal accepted')
        return GoalResponse.ACCEPT
    else:
        self.get_logger().info('Goal rejected: Target position out of range')
        return GoalResponse.REJECT
        
def mttpa_cancel_callback(self, goal_handle):
    self.get_logger().info('Received cancel request')
    # add code that cancels movement
    return CancelResponse.ACCEPT