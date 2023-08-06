Chinese [English](https://gitee.com/casia_iva_engineer/pruning-tools/blob/master/README_english.md)
## 概述
EasyPruner是一个轻量且实用的PyTorch神经网络剪枝工具包，提供了一系列即插即用的网络结构裁剪接口。任何不具备模型压缩知识背景的工程师都可通过在PyTorch工程代码中添加几行代码实现网络模型的精准瘦身，并导出用于多种平台部署的onnx模型。可使模型保持现有精度水平的情况下，成倍提升执行效率和存储效率。<br />​<br />
<a name="EHucI"></a>
## 特点
**透明性**：不需懂模型压缩知识即可流畅使用。<br />**灵活性**：无需更换训练框架，也不用为剪枝接口重构训练或评测代码，仅在原训练框架中进行几行代码增	加，即插即用。<br />**通用性**：支持所有工程场景中常用的网络结构，例如ResNet、VGGNet、Inception、MobileNet等；支持多种训练框架代码，open-mmlab系列开源框架、u版YOLO系列等。<br />**精确性**：吸取神经网络剪枝的最新研究成果，提供在公开评测集上处于SOTA水平的剪枝方法，可对网络冗余连接进行精确识别，在一些常规任务上可以实现无损压缩。<br />**实用性**：剪枝后的模型可直接导出onnx，实现在NPU、ARM、GPU、CPU等多种平台的通用部署<br />

<a name="BXs1U"></a>
## 创新
与其他开源模型剪枝工具项目相比，本项目做了如下创新，以使剪枝工具更加强大：

1. 提出基于ONNX的图分析的网络拓扑排序方法，可以实现前后依赖算子的自动化识别，以兼容多样化的训练框架。
2. 提出包含自研GradDecay稀疏剪枝方法的进阶剪枝模式，该方法针对YOLOv5目标检测算法设计，可以在不增加训练成本的情况下，最大限度保留网络原始表达能力，在一般情况下实现无损剪枝，在大剪枝率情况下依旧保持低精度损失。
3. 提出包含自研MaskL1稀疏剪枝方法的进阶剪枝模式，该方法比目前流行的Network Slimming 方法有优的剪枝精度。



详细使用文档请参加语雀：

中文版：
https://www.yuque.com/books/share/d1639c26-4a93-4274-b028-3134ebcada17?# 《EasyPruner剪枝工具》

英文版：
https://www.yuque.com/docs/share/2abac59c-942d-413c-a379-e28fef97288f
