/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: '产品介绍',
      items: [
        'basic_usage/kuavo-ros-control/docs/1产品介绍/产品介绍',
      ],
    },
    {
      type: 'category',
      label: '快速开始',
      items: [
        'basic_usage/kuavo-ros-control/docs/2快速开始/快速开始',
        'basic_usage/kuavo-ros-control/docs/2快速开始/机器人关节标定'
      ],
    },
    {
      type: 'category',
      label: '开发接口',
      items: [
        'basic_usage/kuavo-ros-control/docs/3开发接口/仿真环境使用',
        'basic_usage/kuavo-ros-control/docs/3开发接口/SDK介绍',
        'basic_usage/kuavo-ros-control/docs/3开发接口/接口使用文档',
      ],
    },
    {
      type: 'category',
      label: '功能案例',
      items: [
        {
          type: 'category',
          label: '通用案例',
          items: [
            'basic_usage/kuavo-ros-control/docs/4功能案例/通用案例/自定义启动案例',
            'basic_usage/kuavo-ros-control/docs/4功能案例/通用案例/H12遥控器使用开发案例',
            'basic_usage/kuavo-ros-control/docs/4功能案例/通用案例/VR使用开发案例',
            'basic_usage/kuavo-ros-control/docs/4功能案例/通用案例/落足点规划案例',
            'basic_usage/kuavo-ros-control/docs/4功能案例/通用案例/二维码检测使用案例',
            'basic_usage/kuavo-ros-control/docs/4功能案例/通用案例/灵巧手手势使用案例',
            'basic_usage/kuavo-ros-control/docs/4功能案例/通用案例/路径轨迹规划案例',
            'basic_usage/kuavo-ros-control/docs/4功能案例/通用案例/数据采集案例',
            'basic_usage/kuavo-ros-control/docs/4功能案例/通用案例/yolov8目标检测案例',
            'basic_usage/kuavo-ros-control/docs/4功能案例/通用案例/手臂逆运动学案例',
          ],
        },
        {
          type: 'category',
          label: '扩展案例',
          items: [
            'basic_usage/kuavo-ros-control/docs/4功能案例/拓展案例/大模型使用案例',
            'basic_usage/kuavo-ros-control/docs/4功能案例/拓展案例/机器人导航案例',
          ],
        },
        'basic_usage/kuavo-ros-control/docs/4功能案例/案例目录',
      ],
    },
    {
      type: 'category',
      label: 'Changelog',
      items: [
        'basic_usage/kuavo-ros-control/CHANGELOG'
      ],
    },
  ],
};

module.exports = sidebars;
