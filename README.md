# 🚀 HOMO-MoneyPrinterTurbo-Enhanced

> **HOMO AI Studio 出品 — 比 MoneyPrinterTurbo 画面更好看的 AI 短视频生成器**
> 一键生成抖音图文卡片式短视频，逐条递进，品牌视觉统一

[![HOMO AI Studio](https://img.shields.io/badge/HOMO-AI%20Studio-blue)](https://github.com/sevenliuhu)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 💡 为什么不是直接用 MoneyPrinterTurbo？

**MoneyPrinterTurbo（73K⭐）很火，但实际产出的视频画面粗糙、配音机械、字幕廉价。**

我们不是魔改 MPT 的代码，而是**完全独立的视觉引擎**，专注一个 MoneyPrinterTurbo 做不了的事：
**做出能发、能火的短视频内容。**

| 对比两项 | MoneyPrinterTurbo | HOMO-Enhanced ⭐ |
|---------|-------------------|------------------|
| **架构** | 搜网络素材→拼接 | 结构化脚本→品牌卡片引擎 |
| **画面风格** | 素材风格跳跃 | 统一深色+蓝白品牌配色 |
| **文字动画** | 一次性全出 | 逐条递进（对标抖音图文模式） |
| **品牌输出** | ❌ 无品牌 | ✅ HOMO片头+片尾+水印 |
| **布局类型** | 仅图文混排 | title/bullet/numbered/quote 四种 |
| **模板系统** | ❌ 无 | ✅ JSON模板，即改即用 |
| **可定制性** | 低（搜到什么是什么） | 高（精确控制每张卡片） |
| **对标热门视频** | ❌ 不能 | ✅ 可直接复刻视频风格 |
| **代码来源** | harry0703/MoneyPrinterTurbo | 完全独立开发 |

## 快速开始

```bash
pip install -r requirements.txt
python examples/demo.py
```

## 📋 使用方式

### 方式一：从模板（推荐）

```python
from money_printer_enhanced import HOMOPipeline
pipeline = HOMOPipeline()
pipeline.from_template('five-goals', '/tmp/my_video.mp4')
```

### 方式二：自定义脚本

```python
from money_printer_enhanced import HOMOPipeline

script = [
    {'layout': 'title', 'header': '我的标题', 'duration': 3.0},
    {'layout': 'bullet', 'header': '① 第一点',
     'items': ['子项1', '子项2', '子项3'],
     'durations': [1.5, 2.0, 2.0, 2.0]},
    {'layout': 'number', 'header': '② 第二点',
     'items': ['步骤1', '步骤2']},
]

pipeline = HOMOPipeline()
pipeline.from_script(script, '/tmp/my_video.mp4')
```

### 方式三：命令行快速

```python
from money_printer_enhanced import quick_homo

quick_homo([
    {'layout': 'title', 'header': '今日分享', 'duration': 2.0},
    {'layout': 'bullet', 'header': '要点', 'items': ['重要', '紧急']},
], '/tmp/out.mp4')
```

## 🎨 卡片布局

| 布局 | 说明 | 适用场景 |
|------|------|---------|
| `title` | 大字居中 + 装饰线 | 开场标题 |
| `bullet` | 标题 + 圆点列表 | 目标/要点展示 |
| `numbered` | 标题 + 数字圆圈列表 | 步骤/排名 |
| `quote` | 引文大字号 | 金句/总结 |

所有的卡片自动带有：
- HOMO 品牌水印（右下角半透明）
- 统一深色背景 + 蓝白配色
- 片中片尾可选品牌卡

## 📁 项目结构

```
HOMO-MoneyPrinterTurbo-Enhanced/
├── money_printer_enhanced/
│   ├── __init__.py    # 模块入口+HOMO品牌信息
│   ├── brand.py       # 🆕 HOMO品牌资产管理
│   ├── composer.py    # 🆕 卡片布局引擎（4种layout）
│   ├── audio.py       # 🆕 配音+品牌音频处理
│   ├── engine.py      # 🆕 视频合成+过渡效果
│   └── pipeline.py    # 🆕 端到端管线
├── templates/
│   ├── five-goals.json
│   └── ... (持续增加)
├── examples/
│   └── demo.py
├── README.md
└── requirements.txt
```

> ⚡ 代码与 MoneyPrinterTurbo 零重叠，完全独立自主开发。
> MPT 用的是 moviepy + faster-whisper 管线，我们用的是 PIL + FFmpeg 管线，架构完全不同。

## 📐 架构对比

```
MoneyPrinterTurbo:          HOMO-MoneyPrinterTurbo-Enhanced:
                          │
  keyword_input           │  script.json
      ↓                   │      ↓
  LLM生成文案             │  CardComposer 解析layout
      ↓                   │      ↓
  Pexels搜素材            │  生成逐条递进的卡片PNG
      ↓                   │      ↓
  edge-tts配音            │  AudioEngine 配音+品牌sting
      ↓                   │      ↓
  moviepy合成             │  VideoEngine FFmpeg合成+过渡
      ↓                   │      ↓
  faster-whisper字幕      │  品牌水印+片头片尾
      ↓                   │      ↓
  输出视频                │  输出视频
```

## 🛠 依赖

```txt
Pillow>=10.0.0
edge-tts>=6.0.0
numpy>=1.24.0
```

**系统依赖:** FFmpeg + 中文字体

## 📊 路线图

- [x] 卡片引擎（4种布局）
- [x] HOMO品牌系统（片头/片尾/水印）
- [x] 多模板支持（JSON）
- [ ] 批量批量生成
- [ ] AI 文案自动生成（接入LLM）
- [ ] 多平台自动发布
- [ ] 更多视觉主题

## 🏷 关于 HOMO AI Studio

HOMO AI Studio 是一个 18 部门的 AI 多智能体系统，专注于智能眼镜和交联记忆系统的专利技术研发。
本视频生成器是我们的开源项目之一，用于展示 HOMO 在 AI 内容生产领域的工程能力。

> 官网: https://github.com/sevenliuhu/HOMO-MoneyPrinterTurbo-Enhanced

## License

MIT — 可商用，保留 HOMO 品牌标识。

---

**如果这个项目帮到了你，点个 ⭐ 支持 HOMO 的持续开源！** 🌟
