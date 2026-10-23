# 安装

## 输入与目标

准备一台能运行 Blender 的电脑以及用于工程、贴图和缓存的磁盘。先完成一张小尺寸渲染，再决定是否安装本地 AI 建模环境。

## Blender

1. 从 [Blender 官方下载页](https://www.blender.org/download/) 获取安装程序或便携包。本教程脚本面向 4.5；需要固定版本时从官网的历史版本入口选择。
2. 启动后确认能保存 `.blend`。界面语言可在 Preferences → Interface 选择；本教程同时使用常见英文功能名。
3. 在默认场景按 F12 渲染，确认得到图像。把工程保存到自己的项目目录。
4. 记下 Blender 可执行文件路径。Windows 示例 `D:/Apps/Blender/blender.exe` 只是写法示例，替换为真实路径；macOS 通常在应用包的 `Contents/MacOS/Blender`，Linux 可由 PATH 调用。

基本操作：中键旋转视图，滚轮缩放，Shift+中键平移；G 移动、R 旋转、S 缩放；Tab 切换对象／编辑模式；数字键盘 0 看相机，1/3/7 看前／侧／顶。先用立方体练习变换、撤销和保存，避免直接破坏角色。

## AI 基础模型

按 [Hunyuan3D-2.1 的 README](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1) 为该版本建立独立 Python 环境、安装依赖和模型权重。AI 运行环境与本教程的工具环境分开，避免 CUDA／PyTorch 依赖互相覆盖。

先用自己能使用的单张干净角色图运行上游示例，确认能导出 GLB，再处理正式角色。设备不足时可使用自己已有授权的生成服务，保留服务名、模型版本、输入图、输出文件和生成设置；后面的 Blender 步骤保持一致。

本仓库不自动安装权重、登录服务或调用付费接口。生成服务和本地模型并非必须同时使用。

## 辅助工具

- 绘图：任选已有的图层绘图软件；Ucupaint 可在 Blender 内绘制。先确认软件能导出颜色图与单独的数据通道。
- PMX/VMD：按 [MMD Tools 扩展页](https://extensions.blender.org/add-ons/mmd-tools/) 安装匹配 Blender 版本的扩展；GLB 直接用 Blender 原生导入。
- FFmpeg：从 [官方入口](https://ffmpeg.org/download.html) 获取适合系统的构建，同时保留 `ffmpeg` 和 `ffprobe`。
- Python 与 Git：安装后在终端执行 `python --version`、`git --version`。本仓库渲染工具环境通过根目录 `requirements.txt` 安装。

## 完成检查

Blender 能保存和重开工程、能出一张图；需要的格式能够导入；终端能定位工具。把这些实际版本写入项目记录。仅安装成功还不代表角色材质或动画已经适配。
