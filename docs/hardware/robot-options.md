---
sidebar_label: Robot Lab Options
sidebar_position: 3
---

# Robot Lab Options (Choose One)

Choose the hardware platform that best fits your research goals and budget. Each option comes with complete ROS 2 integration, pre-configured launch files, and curriculum-aligned lab exercises.

| Option | Robot Model | Price Range (2025) | Best For | Key Specifications | ROS 2 Support |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A** | **Unitree Go2 Pro** | $2,500–$3,200 | Mobile robotics, navigation research, outdoor applications | • Quadruped with 12 DOF<br />• 5 km/h max speed<br />• 2–3 hour battery life<br />• Built-in IMU, depth camera<br />• Payload: 5 kg | Full ROS 2 Humble/Jazzy<br />• Unified robot description (URDF)<br />• Real-time motor control<br />• SLAM and navigation stack<br />• Official Unitree SDK integration |
| **B** | **Unitree G1** | $7,000–$9,000 | Humanoid research, bipedal locomotion, manipulation | • Humanoid with 43 DOF<br />• Height: 127 cm<br />• Weight: 35 kg<br />• Max payload: 5 kg (arm)<br />• Intel RealSense D435i | ROS 2 + MoveIt2 + Isaac ROS<br />• Whole-body control<br />• Bipedal walking algorithms<br />• Manipulation planning<br />• Vision-language integration |
| **C** | **Hiwonder xArm 6DOF** | $800–$1,200 | Manipulation research, pick-and-place, VLA demos | • 6 DOF robotic arm<br />• Reach: 550 mm<br />• Payload: 750 g<br />• Repeatability: ±0.1 mm<br />• ROS-native control | ROS 2 Control + MoveIt2<br />• Trajectory planning<br />• Force sensing<br />• Gripper integration<br />• Easy camera mounting |

### Quick Decision Guide

**Choose Option A (Go2 Pro) if:**
- You want a robust, mobile platform for outdoor/indoor navigation
- Your research focuses on SLAM, path planning, or autonomous exploration
- You need a robot that can handle uneven terrain and real-world environments
- Budget is moderate but you still want professional-grade hardware

**Choose Option B (G1 Humanoid) if:**
- Your goal is humanoid robotics research
- You want to work on bipedal locomotion and balance
- You plan to integrate advanced vision-language-action models
- Budget allows for cutting-edge humanoid hardware
- You want to publish research in top robotics conferences

**Choose Option C (xArm 6DOF) if:**
- Your primary focus is manipulation and grasping
- You want to experiment with VLA models for pick-and-place tasks
- Space and budget are constrained
- You need a reliable arm for repetitive lab experiments
- You're building a custom mobile manipulator platform

### What's Included With Each Option

**All options include:**
- Pre-configured ROS 2 workspace with all necessary packages
- Complete URDF/Xacro robot description files
- Calibrated sensor launch files (cameras, IMU, etc.)
- Simulation models for Gazebo and Isaac Sim
- Step-by-step lab manuals for hardware setup
- Troubleshooting guide and community support

**Additional for Option B (G1):**
- Pre-trained walking gait parameters
- Whole-body controller configurations
- Motion capture calibration tools
- Advanced manipulation demos

### Ordering Information

**Recommended Suppliers:**
- Unitree Robotics (Official): [unitree.com](https://www.unitree.com/)
- Hiwonder Official Store: [hiwonder.com](https://www.hiwonder.com/)
- RobotShop (North America): [robotshop.com](https://www.robotshop.com/)

**Lead Time:** 3–6 weeks for international shipping  
**Educational Discount:** 10–15% available with university credentials  
**Warranty:** 1 year standard, extended options available

### Simulation-First Approach

Don't have hardware yet? No problem! Start with our **fully simulated versions** in:
1. **Gazebo + Ignition** – Physics-based simulation
2. **NVIDIA Isaac Sim** – High-fidelity rendering and synthetic data
3. **Webots** – Cross-platform simulation

All curriculum labs work identically in simulation, so you can begin immediately and add hardware when ready.

**Pro Tip:** Start with simulation, validate your algorithms, then deploy to physical hardware with minimal code changes using our unified ROS 2 framework.

Choose your robot, and let's start building the future of physical AI!