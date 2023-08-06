<p align="center">
  <img src="./docs/gui/images/paddlex.png" width="360" height ="55" alt="PaddleX" align="middle" />
</p>
 <p align= "center"> PaddleX -- 飞桨全流程开发工具，以低代码的形式支持开发者快速实现产业实际项目落地 </p>

<p align="left">
    <a href="./LICENSE"><img src="https://img.shields.io/badge/license-Apache%202-red.svg"></a>
    <a href="https://github.com/PaddlePaddle/PaddleOCR/releases"><img src="https://img.shields.io/github/release/PaddlePaddle/PaddleX.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/python-3.6+-orange.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/os-linux%2C%20win%2C%20mac-yellow.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/QQ_Group-957286141-52B6EF?style=social&logo=tencent-qq&logoColor=000&logoWidth=20"></a>
</p>

## 近期活动
为了更好的满足大家对部署需求，PaddleX举办《工业级视觉算法跨平台部署方案深入解析》两日课。

* 基于QT实现的跨平台图形化部署工具，支持Windows、Linux系统和X86、ARM架构[欢迎体验](https://github.com/cjh3020889729/The-PaddleX-QT-Visualize-GUI)
* 基于C#实现的Windows系统高效部署方案[欢迎体验](https://github.com/PaddlePaddle/PaddleX/tree/develop/deploy/cpp/docs/csharp_deploy)
* 从0-1构建工业级部署线程池，[欢迎体验](https://github.com/ximitiejiang/model_infer_multiThreads)



<p align="center">
  <img src="./docs/activities.png" width="800"  />
</p>



## 近期动态
2021.09.10 PaddleX发布2.0.0正式版本。
- 全新发布Manufacture SDK，支持多模型串联部署。[欢迎体验](./deploy/cpp/docs/manufacture_sdk)
- PaddleX部署全面升级，支持飞桨视觉套件PaddleDetection、PaddleClas、PaddleSeg、PaddleX的端到端统一部署能力。[欢迎体验](./deploy/cpp/docs/deployment.md)
- 发布产业实践案例：钢筋计数、缺陷检测、机械手抓取、工业表计读数。[欢迎体验](./examples)
- 升级PaddleX GUI，支持30系列显卡、新增模型PP-YOLO V2、PP-YOLO Tiny 、BiSeNetV2。[欢迎体验](https://github.com/PaddlePaddle/PaddleX/blob/develop/docs/install.md#2-padldex-gui%E5%BC%80%E5%8F%91%E6%A8%A1%E5%BC%8F%E5%AE%89%E8%A3%85)

详情内容请参考[版本更新文档](./docs/CHANGELOG.md)。

## 产品介绍
:hugs: PaddleX 集成飞桨智能视觉领域**图像分类**、**目标检测**、**语义分割**、**实例分割**任务能力，将深度学习开发全流程从**数据准备**、**模型训练与优化**到**多端部署**端到端打通，并提供**统一任务API接口**及**图形化开发界面Demo**。开发者无需分别安装不同套件，以**低代码**的形式即可快速完成飞桨全流程开发。

:factory: **PaddleX** 经过**质检**、**安防**、**巡检**、**遥感**、**零售**、**医疗**等十多个行业实际应用场景验证，沉淀产业实际经验，**并提供丰富的案例实践教程**，全程助力开发者产业实践落地。

<p align="center">
  <img src="./docs/paddlex_whole.png" width="800"  />
</p>

## 安装与快速体验
PaddleX提供了图像化开发界面、本地API、Restful-API三种开发模式。用户可根据自己的需求选择任意一种开始体验
- [PadldeX GUI开发模式](./docs/quick_start_GUI.md)
- [PaddleX API开发模式](./docs/quick_start_API.md)
- [PaddleX Restful API开发模式](./docs/Resful_API/docs/readme.md)
- [快速产业部署](#4-模型部署)

## 产业级应用示例

- 安防
    - [安全帽检测](./examples/helmet_detection)  
- 工业视觉
    - [表计读数](./examples/meter_reader)  |  [钢筋计数](./examples/rebar_count)  |  [视觉辅助定位抓取](./examples/robot_grab)



## PaddleX 使用文档
本文档介绍了PaddleX从数据准备、模型训练到模型剪裁量化，及最终部署的全流程使用方法。
<p align="center">
  <img src="./docs/process.png" width="600"  />
</p>

### 1. 数据准备

- [数据准备流程说明](./docs/data)
- [数据标注](./docs/data/annotation/README.md)
- [数据格式转换](./docs/data/convert.md)
- [数据划分](./docs/data/split.md)

### 2. 模型训练/评估/预测

- [GUI开发模式](./docs/quick_start_GUI.md)
  - 视频教程：[图像分类](./docs/quick_start_GUI.md/#视频教程) | [目标检测](./docs/quick_start_GUI.md/#视频教程) | [语义分割](./docs/quick_start_GUI.md/#视频教程) | [实例分割](./docs/quick_start_GUI.md/#视频教程)
- API开发模式
  - [API文档](./docs/apis)
    - [数据集读取API](./docs/apis/datasets.md)
    - [数据预处理和数据增强API](./docs/apis/transforms/transforms.md)
    - [模型API/模型加载API](./docs/apis/models/README.md)
    - [预测结果可视化API](./docs/apis/visualize.md)
  - [模型训练与参数调整](tutorials/train)
    - [模型训练](tutorials/train)
    - [训练参数调整](./docs/parameters.md)
  - [VisualDL可视化训练指标](./docs/visualdl.md)
  - [加载训好的模型完成预测及预测结果可视化](./docs/apis/prediction.md)
- [Restful API开发模式](./docs/Resful_API/docs)
  - [使用说明](./docs/Resful_API/docs)


### 3. 模型压缩

- [模型剪裁](tutorials/slim/prune)
- [模型量化](tutorials/slim/quantize)

### 4. 模型部署

- [部署模型导出](./docs/apis/export_model.md)
- [部署方式概览](./deploy/README.md)
  - 本地部署
    - C++部署
      - [C++源码编译](./deploy/cpp/README.md)
      - [C#工程化示例](./deploy/cpp/docs/csharp_deploy)
    - [Python部署](./docs/python_deploy.md)
  - 服务化部署
    - [HubServing部署（Python）](./docs/hub_serving_deploy.md)
  - [基于ONNX部署（C++）](./deploy/cpp/docs/compile/README.md)
    - [OpenVINO推理引擎](./deploy/cpp/docs/compile/openvino/README.md)
    - [Triton部署](./deploy/cpp/docs/compile/triton/docker.md)
- [模型加密](./deploy/cpp/docs/demo/decrypt_infer.md)

### 5. 附录

- [PaddleX模型库](./docs/appendix/model_zoo.md)
- [PaddleX指标及日志](./docs/appendix/metrics.md)
- [无联网模型训练](./docs/how_to_offline_run.md)

## 常见问题汇总
- [GUI相关问题](./docs/FAQ/FAQ.md/#GUI相关问题)
- [API训练相关问题](./docs/FAQ/FAQ.md/#API训练相关问题)
- [推理部署问题](./docs/FAQ/FAQ.md/#推理部署问题)

## 交流与反馈

- 项目官网：https://www.paddlepaddle.org.cn/paddle/paddlex
- PaddleX用户交流群：957286141 (手机QQ扫描如下二维码快速加入)  
  <p align="center">
    <img src="./docs/gui/images/QR2.png" width="180" height ="180" alt="QR" align="middle" />
  </p>

## :hugs: 贡献代码:hugs:

我们非常欢迎您为PaddleX贡献代码或者提供使用建议。如果您可以修复某个issue或者增加一个新功能，欢迎给我们提交Pull Requests。

### 开发者贡献项目

* [工业相机实时目标检测GUI](https://github.com/xmy0916/SoftwareofIndustrialCameraUsePaddle)
（windows系统，基于pyqt5开发）
* [工业相机实时目标检测GUI](https://github.com/LiKangyuLKY/PaddleXCsharp)
（windows系统，基于C#开发）
