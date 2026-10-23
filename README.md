# Hoyo-style AI 3D Workflow

**面向仿星铁／米哈游画风角色的 AI 建模、Blender 改模与成片工作流。**

从下载软件开始，完成基础模型、脸与头发、UV 与贴图、卡通材质、表情动作、物理、灯光相机，最后输出可编辑工程和视频。

## 逆向

照着官方实机截图改。

## 开始

按以下顺序阅读。每章说明输入、操作、应得到什么，以及完成后怎样检查。

| 章节 | 内容 | 本章产物 |
|---|---|---|
| [安装](docs/installation.md) | Blender、AI 建模、绘图、渲染与编码工具 | 可正常运行的环境 |
| [角色资产](docs/character/assets.md) | AI 生成基础模型／导入已有模型、单位与整理 | `character_base.blend` |
| [建模与改模](docs/character/modeling.md) | 脸眼、分束头发、衣饰、拓扑与法线 | `character_model.blend` |
| [UV 与贴图](docs/character/textures.md) | 颜色、控制图、脸影、接缝与清晰度 | 可编辑图层、贴图与语义表 |
| [材质](docs/character/materials.md) | 身体、脸、眼、头发和描边分别处理 | 外观工程与正侧背静帧 |
| [表情与动作](docs/character/animation.md) | 形态键、骨骼、动作导入、镜头表演 | `shot_animation.blend` |
| [物理](docs/character/physics.md) | 发束、裙摆、衣饰的跟随、碰撞和烘焙 | 经过相关动作检查的缓存 |
| [渲染控制](docs/rendering/controller.md) | 光、相机、显示变换、采样与输出 | `shot_final.blend` |
| [出片](docs/rendering/delivery.md) | PNG 序列、断点恢复、后期、声音与编码 | 成片、检查记录和借物表 |
| [高级：数据约定](docs/advanced/contracts.md) | 文件结构、控制通道、有效节点和冻结依赖 | 可复用项目模板 |

从零做角色走完整顺序；已有可用模型从资产检查开始；已有完成动画的 `.blend` 可以直接使用下面的渲染入口。

## 可运行工具

需要 Python 3.11+ 和 Git：

```sh
python -m venv .venv
# Windows PowerShell
.venv/Scripts/Activate.ps1
# macOS / Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

python tools/project.py init --blender "你的Blender可执行文件" --scene "你的shot_final.blend" --work "输出目录"
python tools/project.py run --work "输出目录"
python tools/project.py encode --work "输出目录" --ffmpeg "ffmpeg可执行文件" --ffprobe "ffprobe可执行文件"
```

`init` 在后台读取实际工程，记录场景帧区间、尺寸、帧率、网格、UV、形态键、材质、图片和外部依赖；有缺失文件、无相机或未保存工程时拒绝初始化。`run` 复用固定版本的 [CG Workbench](https://github.com/3218782248-Firefly/cg-workbench)，逐帧验证并恢复；`encode` 输出经过实际帧数与完整解码检查的**无声预览**。配乐与最终投稿版按出片章完成。

这些工具从准备好的 Blender 工程开始运行。AI 生成、角色改模、材质适配、绑定和美术判断按教程完成；仓库没有把这些步骤伪装为已经实现的一键生成系统。

## 工具路线

- 主线环境：Blender 4.5；先固定可用版本，换版本在副本验证。
- AI 基础模型：按 [Hunyuan3D-2.1 上游](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1) 安装与运行，导出 GLB。生成结果作为可修改输入，不直接当成可动画角色。
- 通用卡通材质：参考 [StellarToon](https://github.com/festivities/Blender-StellarToon) 的实际运行环境与接口；不把 Unity Shader 当 Blender 插件安装。
- 模型与动作互通：[MMD Tools](https://extensions.blender.org/add-ons/mmd-tools/)；绘制可用 [Ucupaint](https://github.com/ucupumar/ucupaint)。
- 可靠渲染与检查：固定提交的 CG Workbench；视频编码使用 FFmpeg。

工具需要的 GPU、显存、许可证及模型权重以对应版本上游说明为准。教程不要求安装全部候选插件，也不要求付费后期软件。

## 文档组织参考

参照 [stalomeow/StarRailNPRShader](https://github.com/stalomeow/StarRailNPRShader) 的“安装、角色资产、材质、渲染控制、高级”文档组织方式，在这里补齐 AI 建模到 Blender 成片的步骤。该项目本身使用 Unity URP；本仓库是独立编写的 Blender 制作教程与辅助脚本，没有移植它的着色器源码。

## 状态与参与

当前版本是可阅读的完整制作路线和可运行的工程检查／渲染入口。实际工具验证范围见 [验证记录](docs/validation.md)。尚未提供从 AI 生成到最终画面全部验证过的公开角色样例；不能把文档覆盖全部阶段等同于自动完成全部阶段。

[贡献指南](CONTRIBUTING.md) · [第三方来源](THIRD_PARTY_NOTICES.md) · [MIT 许可](LICENSE)
