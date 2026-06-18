"""
g1_coordination - Coordination Module
Queries perception, manipulation, and navigation modules for candidate
action plans given a task, then aggregates them into a unified plan set.

This is the novel contribution of the G1 HRI system.

Publishes:
  - coordination/status (g1_interfaces/ModuleStatus)
  - coordination/plans  (std_msgs/String)  — JSON of aggregated plan candidates

Services called (as client):
  - perception/request_plan
  - manipulation/request_plan
  - navigation/request_plan
"""

import json
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from g1_interfaces.msg import ModuleStatus
from g1_interfaces.srv import RequestPlan


class CoordinationNode(Node):

    def __init__(self):
        super().__init__('g1_coordination_node')

        # --- Service clients (one per module) ---
        self.perception_client = self.create_client(
            RequestPlan, 'perception/request_plan'
        )
        self.manipulation_client = self.create_client(
            RequestPlan, 'manipulation/request_plan'
        )
        self.navigation_client = self.create_client(
            RequestPlan, 'navigation/request_plan'
        )

        # --- Publishers ---
        self.status_pub = self.create_publisher(
            ModuleStatus,
            'coordination/status',
            10
        )
        self.plans_pub = self.create_publisher(
            String,
            'coordination/plans',
            10
        )

        # --- Status timer ---
        self.status_timer = self.create_timer(1.0, self.publish_status)

        self.get_logger().info('Coordination node ready')

    def request_plans(self, task_description: str, world_state: dict):
        """
        Query all three modules for candidate action plans.
        Returns aggregated dict of candidates per module.

        Args:
            task_description: natural language task, e.g. 'pick up the ball'
            world_state: current world state as a dict (from perception)
        """
        world_state_json = json.dumps(world_state)
        results = {}

        for module_name, client in [
            ('perception',   self.perception_client),
            ('manipulation', self.manipulation_client),
            ('navigation',   self.navigation_client),
        ]:
            if not client.wait_for_service(timeout_sec=2.0):
                self.get_logger().warn(f'{module_name} service not available')
                results[module_name] = []
                continue

            req = RequestPlan.Request()
            req.task_description = task_description
            req.world_state = world_state_json

            future = client.call_async(req)
            rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)

            if future.result() is not None and future.result().success:
                results[module_name] = future.result().candidates
                self.get_logger().info(
                    f'{module_name} returned {len(results[module_name])} candidates'
                )
            else:
                self.get_logger().warn(f'{module_name} plan request failed')
                results[module_name] = []

        return results

    def aggregate_plans(self, module_candidates: dict) -> list:
        """
        Combine per-module candidates into a unified set of composite plans.

        Each composite plan is a dict describing what each module would do.
        Example output for 'pick up the ball':
          [
            {
              'plan_id': 'plan_0',
              'navigation': 'Approach table: move forward 1.2m',
              'perception': 'Track ball during approach',
              'manipulation': 'Extend right arm, grasp from above',
            },
            {
              'plan_id': 'plan_1',
              'navigation': 'Already within reach — no navigation needed',
              'perception': 'Object detected at 0.8m — direct reach feasible',
              'manipulation': 'Extend right arm, grasp from above',
            },
            ...
          ]

        TODO: implement combinatorial plan assembly
        TODO: filter out physically infeasible combinations
        """
        plans = []
        # Placeholder: wrap each module's candidates individually for now
        for i, nav in enumerate(module_candidates.get('navigation', ['none'])):
            for j, manip in enumerate(module_candidates.get('manipulation', ['none'])):
                plan = {
                    'plan_id': f'plan_{i}_{j}',
                    'navigation': nav,
                    'perception': module_candidates.get('perception', ['none'])[0]
                                  if module_candidates.get('perception') else 'none',
                    'manipulation': manip,
                }
                plans.append(plan)

        return plans

    def run_task(self, task_description: str, world_state: dict = None):
        """
        Top-level entry point: given a task, generate and publish all candidate plans.
        """
        if world_state is None:
            world_state = {}

        self.get_logger().info(f'Running task: {task_description}')

        # Step 1: query all modules
        module_candidates = self.request_plans(task_description, world_state)

        # Step 2: aggregate into composite plans
        plans = self.aggregate_plans(module_candidates)

        self.get_logger().info(f'Generated {len(plans)} composite plans')

        # Step 3: publish
        out = String()
        out.data = json.dumps({
            'task': task_description,
            'plans': plans,
        }, indent=2)
        self.plans_pub.publish(out)

        return plans

    def publish_status(self):
        """Broadcast current module status."""
        msg = ModuleStatus()
        msg.module_name = 'coordination'
        msg.status = 'idle'
        msg.description = 'Waiting for tasks'
        msg.stamp = self.get_clock().now().to_msg()
        self.status_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = CoordinationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
