---
sidebar_label: Physical AI Edge Kit (Pro Student Build)
sidebar_position: 2
keywords: [Jetson Orin, RealSense, ReSpeaker, edge AI, humanoid robotics kit, VLA hardware, 2025]
---

# Physical AI Edge Kit — The Exact Hardware That Ships in 2025 Robots (~$950–$1,400)

This is the **real-world, production-grade edge stack** used by 2025 humanoid startups, warehouse robots, and capstone students who refuse to stay in simulation.

If your goal is **Sim→Real VLA agents that understand speech, see in 3D, and act at 15–30 Hz**, this is the kit that gets you there — today.

| Component                           | Model & Spec (2025)                                      | Price (Dec 2025) | Why It’s Non-Negotiable for Serious Physical AI                              |
|-------------------------------------|-----------------------------------------------------------|------------------|--------------------------------------------------------------------------------|
| **Compute**                         | **NVIDIA Jetson Orin NX 16GB** (275 TOPS) <br />or<br />**Orin Nano Super 8GB** (67 TOPS) | $699<br />$249    | Runs **OpenVLA-7B**, Octo, YOLOv10, RT-DETR, and Nav2 **at real-time on the robot itself** — no laptop tethering |
| **Depth + RGB Vision**              | **Intel RealSense D435i** (or D455 for outdoor)           | $349–$379        | Global shutter, built-in IMU, 0.2–10 m depth → perfect for grasping, navigation, and feeding VLA models |
| **Far-Field Audio**                 | **ReSpeaker 4-Mic Array** (Seeed Studio) + AC108 codec    | $29              | 5-meter voice pickup, VAD, DOA, beamforming → "Put the red cup on the table" works even in noisy rooms |
| **Storage & Power**                 | 256GB NVMe SSD + 10,000 mAh USB-C PD battery pack         | $85 + $59        | Fast dataset logging + 3–4 hours untethered operation                          |
| **Mounting & Cables**               | 3D-printed Jetson carrier + Arducam CSI adapters + USB hub| $60–$90          | Clean, professional integration (STL files provided in course repo)           |
| **Total (Budget Build – Nano)**     | Jetson Orin Nano Super + D435i + ReSpeaker + extras       | **≈ $950**       | Perfect for students & indie makers                                            |
| **Total (Pro Build – NX 16GB)**     | Jetson Orin NX 16GB + D455 + full accessories             | **≈ $1,399**     | Exact spec used by Figure, 1X, Covariant, and top capstone winners             |

### What You Can Actually Do With This Kit (Week 13 Demo Examples)

- "Pick the blue bottle and pour water into the glass" → works first try (OpenVLA-7B @ 18 Hz)  
- Full autonomous navigation + manipulation in unknown apartment (Nav2 + Isaac ROS + MoveIt2)  
- Speech → Whisper → VLA → action pipeline with zero cloud dependency  
- 100 % local MCAP recording + Foxglove visualization  
- One-click deploy from Isaac Sim → real robot (zero code change)

### Buy Links (Best Deals – December 2025)

- Jetson Orin NX 16GB → [NVIDIA Store](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/nx/)  
- Jetson Orin Nano Super → [Amazon / Seeed](https://www.seeedstudio.com/) (often $229 during sales)  
- RealSense D435i/D455 → [Intel Official](https://www.intelrealsense.com) or Amazon  
- ReSpeaker 4-Mic → [Seeed Studio](https://www.seeedstudio.com/ReSpeaker-4-Mic-Array-for-Raspberry-Pi.html)  

Course provides:
- Full 3D-printable mount designs  
- Pre-flashed JetPack 6.2 + ROS 2 Jazzy + Isaac ROS image  
- Day-1 launch files so your camera + mic work in 5 minutes  

**This isn’t a toy dev board. This is the same edge stack that will be inside millions of humanoids by 2030.**

Order the Pro kit → finish the capstone on real hardware → put "Deployed VLA agent on physical robot" on your resume.

The future doesn’t wait. Build it now.