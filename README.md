# G1 HRI Coordination

ROS2 modules for humanoid robot task coordination on the Unitree G1 — perception, manipulation, navigation, and a coordination layer for multi-modal action plan generation.

## Packages

| Package | Description |
|---|---|
| `g1_interfaces` | Custom ROS2 messages, services, and actions shared across all modules |
| `g1_perception` | Head movement and computer vision |
| `g1_manipulation` | Pick and place applications |
| `g1_navigation` | Walking and locomotion |
| `g1_coordination` | Multi-modal action plan generation across modules |

## Requirements

- ROS2 Jazzy
- Isaac Sim
- Python 3.10+

## Setup

```bash
cd ~/your_ws/src
git clone git@github.com:YOUR_USERNAME/g1-hri-coordination.git
cd ..
colcon build
source install/setup.bash
```

## Running

Launch individual modules:
```bash
ros2 launch g1_perception perception.launch.py
ros2 launch g1_manipulation manipulation.launch.py
ros2 launch g1_navigation navigation.launch.py
ros2 launch g1_coordination coordination.launch.py
```

## Project Structure

```
g1_hri_coordination/
├── g1_interfaces/        # Shared msgs, srvs, actions
├── g1_perception/        # Perception module
├── g1_manipulation/      # Manipulation module
├── g1_navigation/        # Navigation module
└── g1_coordination/      # Coordination module
```
