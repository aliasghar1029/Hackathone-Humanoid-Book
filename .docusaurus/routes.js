import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/Hackathone-Humanoid-Book/__docusaurus/debug/',
    component: ComponentCreator('/Hackathone-Humanoid-Book/__docusaurus/debug/', '108'),
    exact: true
  },
  {
    path: '/Hackathone-Humanoid-Book/__docusaurus/debug/config/',
    component: ComponentCreator('/Hackathone-Humanoid-Book/__docusaurus/debug/config/', 'af4'),
    exact: true
  },
  {
    path: '/Hackathone-Humanoid-Book/__docusaurus/debug/content/',
    component: ComponentCreator('/Hackathone-Humanoid-Book/__docusaurus/debug/content/', '196'),
    exact: true
  },
  {
    path: '/Hackathone-Humanoid-Book/__docusaurus/debug/globalData/',
    component: ComponentCreator('/Hackathone-Humanoid-Book/__docusaurus/debug/globalData/', '99e'),
    exact: true
  },
  {
    path: '/Hackathone-Humanoid-Book/__docusaurus/debug/metadata/',
    component: ComponentCreator('/Hackathone-Humanoid-Book/__docusaurus/debug/metadata/', '3ac'),
    exact: true
  },
  {
    path: '/Hackathone-Humanoid-Book/__docusaurus/debug/registry/',
    component: ComponentCreator('/Hackathone-Humanoid-Book/__docusaurus/debug/registry/', '47f'),
    exact: true
  },
  {
    path: '/Hackathone-Humanoid-Book/__docusaurus/debug/routes/',
    component: ComponentCreator('/Hackathone-Humanoid-Book/__docusaurus/debug/routes/', '418'),
    exact: true
  },
  {
    path: '/Hackathone-Humanoid-Book/markdown-page/',
    component: ComponentCreator('/Hackathone-Humanoid-Book/markdown-page/', '859'),
    exact: true
  },
  {
    path: '/Hackathone-Humanoid-Book/docs/',
    component: ComponentCreator('/Hackathone-Humanoid-Book/docs/', '09e'),
    routes: [
      {
        path: '/Hackathone-Humanoid-Book/docs/',
        component: ComponentCreator('/Hackathone-Humanoid-Book/docs/', '842'),
        routes: [
          {
            path: '/Hackathone-Humanoid-Book/docs/',
            component: ComponentCreator('/Hackathone-Humanoid-Book/docs/', '9f6'),
            routes: [
              {
                path: '/Hackathone-Humanoid-Book/docs/assessments/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/assessments/', '86e'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/hardware/economy-kit/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/hardware/economy-kit/', 'd20'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/hardware/edge-kit/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/hardware/edge-kit/', '5d6'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/hardware/robot-options/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/hardware/robot-options/', '45c'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/hardware/workstation/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/hardware/workstation/', 'dd7'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/intro/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/intro/', 'e31'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/modules/gazebo-unity/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/modules/gazebo-unity/', 'c19'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/modules/nvidia-isaac/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/modules/nvidia-isaac/', 'd5c'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/modules/ros2/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/modules/ros2/', 'c23'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/modules/vla-capstone/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/modules/vla-capstone/', 'a09'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/outcomes/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/outcomes/', 'e0f'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/tutorial-basics/congratulations/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/tutorial-basics/congratulations/', '5f8'),
                exact: true
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/tutorial-basics/create-a-blog-post/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/tutorial-basics/create-a-blog-post/', '5e7'),
                exact: true
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/tutorial-basics/create-a-document/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/tutorial-basics/create-a-document/', '7d2'),
                exact: true
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/tutorial-basics/create-a-page/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/tutorial-basics/create-a-page/', 'ecb'),
                exact: true
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/tutorial-basics/deploy-your-site/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/tutorial-basics/deploy-your-site/', 'e06'),
                exact: true
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/tutorial-basics/markdown-features/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/tutorial-basics/markdown-features/', '112'),
                exact: true
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/tutorial-extras/manage-docs-versions/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/tutorial-extras/manage-docs-versions/', '348'),
                exact: true
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/tutorial-extras/translate-your-site/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/tutorial-extras/translate-your-site/', '27c'),
                exact: true
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/weekly-breakdown/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/weekly-breakdown/', '93f'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/Hackathone-Humanoid-Book/docs/why-physical-ai/',
                component: ComponentCreator('/Hackathone-Humanoid-Book/docs/why-physical-ai/', 'd8b'),
                exact: true,
                sidebar: "docs"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/Hackathone-Humanoid-Book/',
    component: ComponentCreator('/Hackathone-Humanoid-Book/', '3b8'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
