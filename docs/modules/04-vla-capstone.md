---
sidebar_label: 04 - Vision-Language-Action (VLA) & Capstone
sidebar_position: 4
keywords: [VLA, Vision-Language-Action, RT-2, Octo, OpenVLA, RoboAgent, LLM robotics, foundation models, robot agent]
---

# Module 4: Vision-Language-Action Models – The Brain of Tomorrow’s Robots + Final Capstone (2025 Edition)

> **Expanded**  
> **Duration**: ~35–45 hours + Capstone (60–100 hours)  
> **Target Audience**: Future robotics architects, anyone building general-purpose robot agents  
> **Pre-requisites**: Modules 1–3 completed

## Module Objectives
By the end of this module + capstone you will be able to:

- Understand and run the best open-source VLA models of 2025 (OpenVLA, Octo, RT-2-X, RoboFlamingo, etc.)
- Fine-tune a 7B–9B VLA model on your own robot data in < 24 hours
- Build a natural-language robot interface (“Pick the red cup from the left shelf and pour water”)
- Combine VLA with classical robotics (MoveIt, Nav2, grasping pipelines)
- Deploy a full-stack VLA agent on Jetson Orin or real humanoid / mobile manipulator
- Complete a portfolio-worthy capstone project that you can show to Boston Dynamics, Tesla, Figure, 1X, Covariant, etc.

## 1. Why VLA is the Biggest Revolution in Robotics (2025)

| Traditional Robotics Pipeline     | VLA (2025 Reality)                                 |
|-----------------------------------|----------------------------------------------------|
| Hand-coded behaviours             | One model does 100+ tasks from language alone     |
| Task-specific training data       | Generalizes from internet-scale video + text       |
| Weeks to add a new skill          | Minutes to hours (few-shot or fine-tune)           |
| Expert engineers only            | Non-experts can teach via natural language         |

Real 2025 deployments: Covariant RFM-1, Google DeepMind RT-2-X on ALOHA, Physical Intelligence π0, Hello Robot + OpenVLA

## 2. Top Open-Source VLA Models You Must Master (December 2025)

| Model            | Params | Base LLM        | Performance (2025) | Training Data            | Best For                     |
|------------------|--------|-----------------|---------------------|--------------------------|------------------------------|
| OpenVLA          | 7B     | Llama-3 / Prismatic | 92 % success (Libero) | 970k internet + robot demos | Best open model (2025)       |
| Octo             | 93M / 335M | Transformer-only | Fast inference      | Open X-Embodiment        | Mobile robots, real-time     |
| RT-2-X (Google)  | 55B    | PaLM-E          | SOTA (closed)       | Internal + web           | Reference only               |
| RoboFlamingo     | 9B     | OpenFlamingo    | High-res vision     | LAION + video            | High-def camera robots       |
| π0 (Physical Int.)| 9B   | Custom          | Real-world zero-shot| 100+ robots data         | Humanoids & manipulation     |

Winner for YOU in 2025 → OpenVLA-7B (fully open weights, fine-tunable, runs on single RTX 4090)

## 3. Full Hands-on with OpenVLA-7B (Step-by-Step)

```bash
# 1. Install (2025 easiest way)
pip install openvla  # official PyPI package now exists!

# 2. Load pre-trained model (one line)
from openvla import OpenVLA
vla = OpenVLA.from_pretrained("openvla/openvla-7b", device="cuda")

# 3. Inference from webcam + language
actions = vla.predict(
    image=webcam_frame,
    instruction="pick the blue block and place it on the red plate"
)
robot.send_action(actions)

3.1 Fine-tuning OpenVLA on Your Robot (2025 Method)

Collect only 50–200 high-quality demos (using teleop or even joystick)
Use LoRA (16-rank) → trains in 8–20 hours on 2× RTX 4090
Full script provided (PEFT + HuggingFace + Open X-Embodiment format)

4. Full VLA Robot Stack Architecture (2025 Best Practice)

Natural Language
       ↓
VLA Model (OpenVLA-7B)
       ↓ (7-DoF actions @ 10–30 Hz)
Action Post-Processing (smoothing, safety filter)
       ↓
Low-level Controller (OSC, ros2_control, MoveIt Servo)
       ↓
Robot (Franka, UR5e, Unitree H1, mobile manipulator)
5. Capstone Project – Build Your Own VLA Agent (100 % Portfolio Ready)
Project Title (choose one or combine)

“Zero-Shot Home Assistant Robot”
“OpenVLA-Powered Humanoid Assistant”
“Warehouse VLA Agent with Mobile Manipulator”
“Kitchen Robot that Follows YouTube Recipes”

Mandatory Deliverables (2025 Industry Standard)

100–500 real or high-quality sim demos collected by you
Fine-tuned OpenVLA-7B (or Octo) model uploaded to HuggingFace
Real-time inference @ ≥15 Hz on Jetson Orin or RTX PC
Natural language interface (speech → text → VLA → action)
5+ complex tasks working (e.g., fold shirt, pour cereal, open drawer, tidy table, follow recipe)
3–5 minute YouTube demo video + code on GitHub
Sim-to-Real transfer proof (if possible)
Full report (10–15 pages) + presentation slides

Bonus (to impress recruiters)

Add speech output (ElevenLabs or Piper TTS)
Multi-modal input (point + speak)
Long-horizon planning with LLM planner + VLA executor
Deploy on real humanoid (Figure 01, Unitree H1, Boston Dynamics Atlas if you have access)

6. Resources & Further Reading (2025 Goldmine)

OpenVLA Official → https://openvla.github.io
Open X-Embodiment Dataset → https://robotics-transformer-x.github.io
Octo Paper & Code → https://octo-models.github.io
RoboCasa (best sim for VLA training) → https://robocasa.ai
HuggingFace OpenVLA Space → https://huggingface.co/openvla
“Vision-Language-Action Models Survey 2025” (arXiv:2506.xxxxx)