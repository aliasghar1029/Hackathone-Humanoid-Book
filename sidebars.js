/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
    docs: [
        "intro",
        "why-physical-ai",
        {
            type: "category",
            label: "Core Modules",
            collapsed: false,
            items: [
                "modules/ros2",           // ← yahi sahi hai (01-ros2.md)
                "modules/gazebo-unity",   // ← 02-gazebo-unity.md
                "modules/nvidia-isaac",   // ← 03-nvidia-isaac.md
                "modules/vla-capstone",   // ← 04-vla-capstone.md
            ],
        },
        "weekly-breakdown",
        "outcomes",
        "assessments",
        {
            type: "category",
            label: "Hardware & Kits",
            collapsed: true,
            items: [
                "hardware/economy-kit",
                "hardware/edge-kit",
                "hardware/robot-options",
                "hardware/workstation",
            ],
        },
    ],
};

module.exports = sidebars;