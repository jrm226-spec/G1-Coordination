"""
g1_manipulation - Manipulation Module
Handles pick and place applications for the Unitree G1.

Subscribes:
  - /joint_states (sensor_msgs/JointState)

Publishes:
  - manipulation/status (g1_interfaces/ModuleStatus)

Services:
  - manipulation/request_plan (g1_interfaces/RequestPlan)
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from g1_interfaces.msg import ModuleStatus
from g1_interfaces.srv import RequestPlan


class ManipulationNode(Node):

    def __init__(self):
        super().__init__('g1_manipulation_node')

        # --- Publishers ---
        self.status_pub = self.create_publisher(
            ModuleStatus,
            'manipulation/status',
            10
        )

        # --- Subscribers ---
        self.joint_state_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        # --- Services ---
        self.plan_srv = self.create_service(
            RequestPlan,
            'manipulation/request_plan',
            self.handle_plan_request
        )

        # --- State ---
        self.joint_states = None

        # --- Status timer ---
        self.status_timer = self.create_timer(1.0, self.publish_status)

        self.get_logger().info('Manipulation node ready')

    def joint_state_callback(self, msg):
        """Track current joint positions for reachability checks."""
        self.joint_states = msg
        # TODO: update arm reachability model from current joint states

    def handle_plan_request(self, request, response):
        """
        Called by the Coordination Module with a task description.
        Returns a list of manipulation-based action candidates.

        Example candidates for 'pick up the ball':
          - 'Extend right arm, grasp from above'
          - 'Bimanual grasp — stabilize with left, grasp with right'
          - 'Adjust wrist orientation, grasp from side'
        """
        self.get_logger().info(f'Plan request received: {request.task_description}')

        # TODO: use self.joint_states and request.world_state to check reachability
        # TODO: generate arm trajectory candidates via IK
        candidates = []

        response.success = True
        response.candidates = candidates
        response.message = 'OK'
        return response

    def publish_status(self):
        """Broadcast current module status."""
        msg = ModuleStatus()
        msg.module_name = 'manipulation'
        msg.status = 'idle'
        msg.description = 'Waiting for tasks'
        msg.stamp = self.get_clock().now().to_msg()
        self.status_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ManipulationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
