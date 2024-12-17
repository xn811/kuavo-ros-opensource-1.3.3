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
        'basic_usage/kuavo_ros1_workspace/docs/1产品介绍/产品介绍',
      ],
    },
    {
      type: 'category',
      label: '快速开始',
      items: [
        'basic_usage/kuavo/kuavo_ros1_workspace/2快速开始/快速开始',
        'basic_usage/kuavo/kuavo_ros1_workspace/2快速开始/机器人关节标定'
      ],
    },
    {
      type: 'category',
      label: '开发接口',
      items: [
        'basic_usage/kuavo/kuavo_ros1_workspace/3开发接口/仿真环境使用',
        'basic_usage/kuavo/kuavo_ros1_workspace/3开发接口/SDK介绍',
        'basic_usage/kuavo/kuavo_ros1_workspace/3开发接口/sdk_use',
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
            'basic_usage/kuavo_ros1_workspace/docs/4功能案例/通用案例/1_自定义启动案例',
            'basic_usage/kuavo_ros1_workspace/docs/4功能案例/通用案例/2_H12遥控器使用开发案例',
            'basic_usage/kuavo_ros1_workspace/docs/4功能案例/通用案例/3_VR使用开发案例',
            'basic_usage/kuavo_ros1_workspace/docs/4功能案例/通用案例/4_单步控制案例(落足点规划)',
            'basic_usage/kuavo_ros1_workspace/docs/4功能案例/通用案例/5_二维码检测使用案例',
            'basic_usage/kuavo_ros1_workspace/docs/4功能案例/通用案例/6_灵巧手手势使用案例',
            'basic_usage/kuavo_ros1_workspace/docs/4功能案例/通用案例/7_路径轨迹规划案例',
            'basic_usage/kuavo_ros1_workspace/docs/4功能案例/通用案例/8_数据采集案例',
            'basic_usage/kuavo_ros1_workspace/docs/4功能案例/通用案例/9_yolov8目标检测案例',
          ],
        },
        {
          type: 'category',
          label: '扩展案例',
          items: [
            'basic_usage/kuavo_ros1_workspace/docs/4功能案例/扩展案例/大模型使用案例',
            'basic_usage/kuavo_ros1_workspace/docs/4功能案例/扩展案例/机器人导航',
          ],
        },
        'basic_usage/kuavo_ros1_workspace/docs/4功能案例/案例目录',
      ],
    },
    {
      type: 'category',
      label: 'Changelog',
      items: [
        'basic_usage/kuavo_ros1_workspace/CHANGELOG'
      ],
    },
  ],
};

module.exports = sidebars;
