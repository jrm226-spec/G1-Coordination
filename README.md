# G1 Coordination - CURRENT WIP

ROS2 modules for humanoid robot task coordination on the Unitree G1 — perception, manipulation, navigation, and a coordination layer for multi-modal action plan generation.

## Current Progress

Created overall structure and temporary code within the packages.

## Future Plans for Progress

Testing and reiterating perception code, seeing its performance in IsaacSim.

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
git clone https://github.com/jrm226-spec/G1-Coordination.git
cd G1-Coordination
cd ..
colcon build
source install/setup.bash
```

## Project Structure

```
G1-Coordination/
├── src/
│   ├── g1_interfaces/
│   ├── g1_perception/
│   ├── g1_manipulation/
│   ├── g1_navigation/
│   └── g1_coordination/
```
