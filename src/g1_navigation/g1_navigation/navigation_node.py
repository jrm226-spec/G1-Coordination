"""
g1_navigation - Navigation Module
Handles walking and locomotion for the Unitree G1.

Subscribes:
  - /odom (nav_msgs/Odometry)

Publishes:
  - /cmd_vel (geometry_msgs/Twist)  — velocity commands to locomotion controller
  - navigation/status (g1_interfaces/ModuleStatus)

Services:
  - navigation/request_plan (g1_interfaces/RequestPlan)
"""

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from g1_interfaces.msg import ModuleStatus
from g1_interfaces.srv import RequestPlan


class NavigationNode(Node):

    def __init__(self):
        super().__init__('g1_navigation_node')

        # --- Publishers ---
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.status_pub = self.create_publisher(
            ModuleStatus,
            'navigation/status',
            10
        )

        # --- Subscribers ---
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        # --- Services ---
        self.plan_srv = self.create_service(
            RequestPlan,
            'navigation/request_plan',
            self.handle_plan_request
        )

        # --- State ---
        self.current_pose = None

        # --- Status timer ---
        self.status_timer = self.create_timer(1.0, self.publish_status)

        self.get_logger().info('Navigation node ready')

    def odom_callback(self, msg):
        """Track robot pose in the world."""
        self.current_pose = msg.pose.pose
        # TODO: update internal map / occupancy state

    def handle_plan_request(self, request, response):
        """
        Called by the Coordination Module with a task description.
        Returns a list of navigation-based action candidates.

        Example candidates for 'pick up the ball':
          - 'Already within reach — no navigation needed'
          - 'Approach table: move forward 1.2m'
          - 'Reposition to left side of table for better arm angle'
        """
        self.get_logger().info(f'Plan request received: {request.task_description}')

        # TODO: use self.current_pose and request.world_state
        # TODO: check distance to target, generate approach trajectories
        candidates = []

        response.success = True
        response.candidates = candidates
        response.message = 'OK'
        return response

    def publish_status(self):
        """Broadcast current module status."""
        msg = ModuleStatus()
        msg.module_name = 'navigation'
        msg.status = 'idle'
        msg.description = 'Waiting for tasks'
        msg.stamp = self.get_clock().now().to_msg()
        self.status_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = NavigationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
