---
sidebar_label: 02 - Gazebo & Unity – The Digital Twin
sidebar_position: 2
keywords: [Gazebo, Unity, robot simulation, digital twin, physics engine, synthetic data, ROS 2 bridge]
---

# Module 2: The Digital Twin – Gazebo Classic & Unity Robotics (Complete & In-Depth)

> **Expanded**  
> **Duration**: ~22–28 hours (Theory + Hands-on + Large Mini-Project)  
> **Target Audience**: Robotics developers, simulation engineers, perception & autonomy teams  
> **Pre-requisites**: Module 1 (ROS 2), basic 3D modeling knowledge helpful

## Module Objectives
By the end of this module you will be able to:

- Choose the right simulator for any robotics use-case in 2025
- Master Gazebo Classic 11 with ROS 2 Jazzy (the last fully stable combo)
- Build high-fidelity physics worlds (contacts, friction, erosion, soft bodies)
- Use Ignition Gazebo (now Gazebo Sim) – the official future path
- Connect ROS 2 to Unity via ROS-TCP-Connector & Robotics Hub
- Generate massive synthetic datasets for ML/CV training
- Run Hardware-in-the-Loop (HIL) and Software-in-the-Loop (SIL) tests
- Seamlessly transfer algorithms from sim → real robot (Sim2Real)

## 1. Why Simulation is Non-Negotiable in 2025

| Real Robot Testing              | Simulation (Digital Twin)                     |
|----------------------------------|-----------------------------------------------|
| Expensive & slow                 | Unlimited parallel runs                       |
| Risk of hardware damage          | Zero risk                                     |
| Hard to reproduce edge cases     | Fully deterministic & scriptable              |
| Limited sensor data variety      | Infinite variations (weather, lighting, faults)|

**Industry reality**: 95 % of autonomy code is developed & validated in simulation first.

## 2. Gazebo Classic vs. Ignition Gazebo (Gazebo Sim) – 2025 Decision Matrix

| Feature                       | Gazebo Classic 11          | Gazebo Sim (Harmonic+)         | Winner 2025          |
|-------------------------------|----------------------------|--------------------------------|----------------------|
| ROS 2 Integration             | Native & rock-solid (Jazzy)| Native (but newer bridges)     | Classic (for now)    |
| Physics Engines               | ODE, Bullet, Simbody, DART | Dart 6.13+, Bullet, TPE        | Gazebo Sim           |
| Rendering Quality             | Basic OpenGL               | High-quality (OgRE Next)       | Gazebo Sim           |
| GUI & World Editing           | gazebo_gui (old)           | Gazebo GUI (modern)            | Gazebo Sim           |
| Plugin Ecosystem              | Mature (10+ years)         | Growing fast                   | Classic still leads  |
| Official Future               | End-of-life after Jazzy    | Actively developed             | Gazebo Sim           |

**2025 Recommendation**  
→ Use **Gazebo Classic 11 + ROS 2 Jazzy** for learning & production today  
→ Learn **Gazebo Sim (Harmonic)** for future-proofing (mandatory from ROS 2 Kilt onward)

## 3. Gazebo Classic 11 – Full Setup & Mastery (2025)

```bash
# Install Gazebo Classic 11 (perfectly matches ROS 2 Jazzy)
sudo apt install ros-jazzy-gazebo-ros-pkgs ros-jazzy-gazebo-ros2-control
# Optional: Full Gazebo standalone
sudo apt install gazebo libgazebo11-dev

3.1 Essential Gazebo Concepts

SDF (Simulation Description Format) 1.7–1.9
Worlds (.world files), Models (.sdf), Plugins (sensor, system, actor)
Physics profiles (real-time factor, solver settings)
ROS 2 control: ros2_control, gazebo_ros2_control, diff_drive, joint_trajectory_controller

3.2 Building a Realistic Differential-Drive Robot from Scratch
Full step-by-step tutorial included:

URDF + Xacro → SDF conversion
Inertial values, collision meshes, friction coefficients
Realistic LiDAR (ray sensor), Depth camera (gpu_lidar + camera), IMU noise
gazebo_ros2_control with hardware interface
Teleop + odometry verification (RTF > 0.95)

3.3 Advanced Physics & Sensors

Soft bodies & deformable terrain
Hydrodynamics (buoyancy plugin)
Wind & atmospheric effects
Sensor noise models (Gaussian, dropout, bias)

4. Ignition Gazebo (Gazebo Sim) – The Future is Here

sudo apt install ros-jazzy-ignition-gazebo6  # or gz-harmonic

New scene graph, levels system, deterministic physics
Built-in support for MCAP recording
Modern GUI with entity-component view

Mini-lab: Migrate your Classic robot to Gazebo Sim in < 30 minutes
5. Unity Robotics – When You Need Photorealism & Synthetic Data
5.1 Why Top Companies Use Unity in 2025

NVIDIA Omniverse, Tesla Dojo, Waymo, Cruise, Zoox all use Unity-based pipelines
Perfect domain randomization → best Sim2Real transfer
100–1000× faster dataset generation than real robots

5.2 Full ROS 2 ↔ Unity Bridge Setup (2025)

# Using ROS-TCP-Connector + Unity Robotics Hub
# GitHub: Unity-Technologies/ROS-TCP-Connector
# GitHub: Unity-Technologies/Robotics-End-Effector

Step-by-step:

Install Unity 2022.3 LTS + ROS TCP Connector package
Set up ROS 2 message definitions (via Robotics Hub)
Connect via TCP Endpoint (zero message loss)
Publish /clock, /tf, sensor topics; subscribe to /cmd_vel

5.3 Synthetic Data Generation Pipeline

Domain Randomization (textures, lighting, distractors, camera parameters)
Ground-truth segmentation, depth, optical flow, bounding boxes
Export to COCO, KITTI, or custom formats
10 k–100 k labeled images per hour on a single RTX 4090

Mini-Project Part-2: Build a photorealistic warehouse in Unity with 3 moving robots and generate 50 k images for YOLO training.
6. Simulators Comparison Cheat-Sheet (2025)

SimulatorBest ForROS 2 SupportPhysicsRenderingLicenseGazebo Classic 11ROS 2 control, dynamics, sensorsExcellentGoodBasicApacheGazebo SimFuture-proof, high-quality visualsExcellentExcellentExcellentApacheUnityPerception, ML training, HMIVery goodGood (PhysX)PhotorealProprietaryWebotsEducation, quick prototypingGoodGoodGoodApacheIsaac Sim (Omniverse)NVIDIA ecosystem, ray-traced sensorsExcellentBestPhotorealFree for individualsMuJoCoReinforcement learning, contactsGrowingBest for RLMinimalApache
7. Final Mini-Project (40% weightage)
“Digital Twin of a Real Robot” – Choose one path:
Path A – Gazebo Classic (Recommended for most students)
Build a complete mobile manipulator with:

Accurate physics (mass, inertia, friction)
LiDAR + RGB-D + IMU with realistic noise
ros2_control + MoveIt2 integration
Full navigation stack (Nav2) working in simulation
MCAP bag recording + Foxglove visualization

Path B – Unity Photorealism
Re-create the same robot in Unity with:

Domain-randomized environment
50 k+ synthetic dataset with perfect labels
ROS 2 bridge running at 100 Hz+
Train a simple object detector and show Sim2Real transfer

Resources & Further Reading

Gazebo Classic Tutorials → http://gazebosim.org/tutorials
Gazebo Sim Docs → https://gazebosim.org
Unity Robotics Hub → https://github.com/Unity-Technologies/Unity-Robotics-Hub
ROS-TCP-Connector → https://github.com/Unity-Technologies/ROS-TCP-Connector
NVIDIA Isaac Sim → https://developer.nvidia.com/isaac-sim
“Simulation for Robotics 2025” – O’Reilly Report