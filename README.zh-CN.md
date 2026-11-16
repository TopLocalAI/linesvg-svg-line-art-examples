[English](./README.md) | 简体中文 | [日本語](./README.ja.md)

# linesvg-svg-line-art-examples

`linesvg-svg-line-art-examples` 是一个可编辑 SVG 线稿开源示例库、零依赖命令行改样式小工具与 SVG 编辑指南，面向插画与平面设计师、前端开发者，以及使用激光切割机、刻字机、绘图仪或打印涂色页的创作者；你可以用仓库中的真实成对示例对照位图原图与 SVG 描边结构，用脚本批量修改自己手头任意 SVG 文件的线宽、颜色与填充，或查阅不同制作场景的矢量文件检查要点。本仓库中的 SVG 示例由 LineSVG 生成，LineSVG 的官方网站是 [https://linesvg.ai](https://linesvg.ai)（中文版：[https://linesvg.ai/zh](https://linesvg.ai/zh)）。

---

## 仓库目录结构

```text
linesvg-svg-line-art-examples/
├── examples/                         # 16 个 SVG 示例 + 3 张配对输入位图 + 文件索引
│   ├── restyled/                     # 由 tools/svg_restyle.py 实际生成的改样式结果
│   └── README.md                     # 每个文件的用途、字节大小与 <path> 路径数量表
├── tools/
│   ├── svg_restyle.py                # 纯 Python 标准库编写的 SVG 批量改线宽/颜色工具
│   └── README.md                     # 命令行参数说明与常用示例
├── docs/
│   ├── editing-svg-line-art.md       # SVG 线稿结构、代码编辑与下游场景指南（中文）
│   └── editing-svg-line-art.en.md    # 英文版编辑指南
├── README.md                         # 英文说明
└── README.zh-CN.md                   # 简体中文说明
```

---

## 快速上手：批量修改 SVG 线宽与颜色

[`tools/svg_restyle.py`](./tools/svg_restyle.py) 仅使用 Python 3 标准库（`xml.etree.ElementTree`），无需安装任何第三方包，可直接处理 Illustrator、Inkscape、Figma 或各类描摹工具导出的合法 `.svg` 文件。工具同时兼容直接表现属性（`stroke="..."`）与行内 CSS `style` 属性（`style="stroke:..."`），保留原始 `viewBox`，并默认保护无描边的实心点缀色块。

```bash
# 1. 将单张涂色页轮廓加粗为 4、统一深色描边并设 fill="none"
python3 tools/svg_restyle.py examples/coloring-page.svg examples/restyled/ \
  --stroke-width 4 --stroke "#111827" --fill none

# 2. 修改“描边 + 实心点缀”植物线稿的线条粗细与颜色（自动保留无描边的实心浆果色块）
python3 tools/svg_restyle.py examples/botanical.svg examples/restyled/ \
  --stroke-width 2.5 --stroke "#1e3a5f"

# 3. 将整个目录内所有 SVG 的现有线宽按 1.5 倍等比加粗
python3 tools/svg_restyle.py examples/ ./out-scaled/ \
  --stroke-scale 1.5 --stroke "#334155"
```

完整参数（含将纯填充剪影转为描边轮廓的 `--all-shapes` 以及递归扫描目录的 `-r`）详见 [`tools/README.md`](./tools/README.md)。

---

## SVG 线稿示例与成对对照（`examples/`）

[`examples/`](./examples/) 目录收录了 16 个覆盖三种矢量结构的 SVG 文件，以及 3 组「位图原图 → SVG 线稿」对照示例：

- **纯中心线描边（`fill="none"`）**：
  - [`examples/coloring-page.svg`](./examples/coloring-page.svg) —— 轮廓闭合的可打印涂色页（`138` 条 `<path>`）
  - [`examples/single-line.svg`](./examples/single-line.svg) —— 无双线的单线花环，适用于 Cricut 笔绘、烫金与压痕划线（`115` 条 `<path>`）
  - [`examples/face-oneline.svg`](./examples/face-oneline.svg) —— 连续一笔画侧脸，适用于绘图仪与刺绣底稿（`12` 条 `<path>`）
  - [`examples/icon-coffee.svg`](./examples/icon-coffee.svg) —— 线宽均匀的定制描边图标（`17` 条 `<path>`）
- **描边线条 + 局部实心点缀**：
  - [`examples/botanical.svg`](./examples/botanical.svg)、[`examples/lighthouse.svg`](./examples/lighthouse.svg)、[`examples/bicycle.svg`](./examples/bicycle.svg)、[`examples/hero-camera.svg`](./examples/hero-camera.svg)、[`examples/tattoo.svg`](./examples/tattoo.svg)
- **封闭填充剪影（无 `stroke`）**：
  - [`examples/laser-cut.svg`](./examples/laser-cut.svg) —— 一体相连的激光切割圆形挂饰（`2` 条 `<path>`）
  - [`examples/logo-mountain.svg`](./examples/logo-mountain.svg) —— 可任意缩放改色的山峰 Logo（`2` 条 `<path>`）
- **位图输入 → SVG 输出成对示例**：
  - [`examples/cat-photo.jpg`](./examples/cat-photo.jpg) → [`examples/cat-lines.svg`](./examples/cat-lines.svg)（实拍照片转可编辑描边线稿）
  - [`examples/sketch-input.jpg`](./examples/sketch-input.jpg) → [`examples/sketch-lines.svg`](./examples/sketch-lines.svg)（铅笔手绘草图转干净描边 SVG）
  - [`examples/cover-input.png`](./examples/cover-input.png) → [`examples/cover-vectorize.svg`](./examples/cover-vectorize.svg)（位图树叶插画描摹为矢量描边与色块）

所有文件的精确大小、`<path>` 路径数量与 `examples/restyled/` 输出对照表见 [`examples/README.md`](./examples/README.md)。

---

## 指南：理解与编辑 SVG 线稿

阅读 [`docs/editing-svg-line-art.md`](./docs/editing-svg-line-art.md)（英文版：[`docs/editing-svg-line-art.en.md`](./docs/editing-svg-line-art.en.md)），快速掌握以下实操要点：

1. **SVG 线稿基本结构**：`viewBox` 如何决定 `stroke-width` 的视觉粗细、开放路径与闭合路径（`Z`）的区别，以及为什么漏写 `fill="none"` 会让弯曲路径出现黑色填充块。
2. **描边线稿 vs. 填充轮廓**：为什么有些自动描摹得到的 SVG 在绘图仪上会来回画两道（双线问题）、改 `stroke-width` 无法把线变细，以及如何在文本编辑器或矢量软件里一眼分辨。
3. **代码级修改方法**：行内 `style="..."`、`<style>` 类规则、元素表现属性与 `<g>` 分组继承之间的优先级关系，以及 `currentColor` 和 `vector-effect="non-scaling-stroke"` 的用法。
4. **分场景检查清单**：用于激光切割与刻字机、Cricut / 笔绘机、可打印涂色页、刺绣打版底稿与热转印纹身稿时的注意事项。

---

## 想自动完成这件事

如果你需要直接用文字生成可编辑 SVG 线稿，或自动把照片与草图转换成真实描边路径，可以使用 [LineSVG 中文站](https://linesvg.ai/zh)（英文版：[https://linesvg.ai](https://linesvg.ai)）。它支持根据文本描述生成线稿，或上传最大 20 MB 的 PNG、JPG、WebP 图片转换为 SVG，提供线条可调、切割轮廓、彩色分层三种输出结构，涵盖一笔画、涂色页、纹身稿、Cricut 单线与激光切割等场景，并提供支持最大 2 MB 文件上传的在线 SVG 描边调整与 AI 编辑，可导出 SVG 或 PNG。未登录可在工作台查看演示，新注册账号赠送 10 积分（30 天有效，默认每次生成、转换或 AI 编辑消耗 10 积分）。

- 官方网站：[https://linesvg.ai/zh](https://linesvg.ai/zh) · [https://linesvg.ai](https://linesvg.ai)
- 延伸阅读：[照片转线条画软件对比](https://linesvg.ai/zh/blog/photo-to-line-art-software-comparison) · [生成可编辑 SVG 线稿的 AI 工具盘点](https://linesvg.ai/zh/blog/ai-editable-svg-line-art-tools)

---

## License

- **代码**（`tools/`）：MIT License。
- **文档与示例图片/SVG**（`docs/`、`examples/` 及各说明文档）：Creative Commons Attribution 4.0 International（CC BY 4.0）。
