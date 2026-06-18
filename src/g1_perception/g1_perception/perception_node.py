"""
g1_perception - Perception Module
Handles head movement and computer vision for the Unitree G1.

Subscribes:
  - /camera/image_raw (sensor_msgs/Image)

Publishes:
  - perception/status (g1_interfaces/ModuleStatus)

Services:
  - perception/request_plan (g1_interfaces/RequestPlan)
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from g1_interfaces.msg import ModuleStatus
from g1_interfaces.srv import RequestPlan


class PerceptionNode(Node):

    def __init__(self):
        super().__init__('g1_perception_node')

        # --- Publishers ---
        self.status_pub = self.create_publisher(
            ModuleStatus,
            'perception/status',
            10
        )

        # --- Subscribers ---
        self.camera_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.camera_callback,
            10
        )

        # --- Services ---
        self.plan_srv = self.create_service(
            RequestPlan,
            'perception/request_plan',
            self.handle_plan_request
        )

        # --- State ---
        self.current_image = None
        self.world_state = {}

        # --- Status timer ---
        self.status_timer = self.create_timer(1.0, self.publish_status)

        self.get_logger().info('Perception node ready')

    def camera_callback(self, msg):
        """Receive raw camera image from Isaac Sim."""
        self.current_image = msg
        # TODO: run CV pipeline (object detection, depth estimation, etc.)

    def handle_plan_request(self, request, response):
        """
        Called by the Coordination Module with a task description.
        Returns a list of perception-based action candidates.

        Example candidates for 'pick up the ball':
          - 'Object detected at 0.8m — direct reach feasible'
          - 'Object occluded — head pan left to reacquire before reaching'
        """
        self.get_logger().info(f'Plan request received: {request.task_description}')

        # TODO: use self.world_state and self.current_image to generate candidates
        candidates = []

        response.success = True
        response.candidates = candidates
        response.message = 'OK'
        return response

    def publish_status(self):
        """Broadcast current module status."""
        msg = ModuleStatus()
        msg.module_name = 'perception'
        msg.status = 'idle'
        msg.description = 'Waiting for tasks'
        msg.stamp = self.get_clock().now().to_msg()
        self.status_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PerceptionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
