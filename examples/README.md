简体中文 | [English](#english)

# SVG 线稿示例索引（`examples/`）

本目录收录了 16 个不同结构的 SVG 矢量示例、3 组「位图原图 → SVG 线稿」对照文件，以及 `restyled/` 子目录下由 [`../tools/svg_restyle.py`](../tools/svg_restyle.py) 批量改线宽与颜色后的输出示例。

这些文件涵盖了三种常见矢量结构，便于直接对照代码或导入矢量软件、切割/绘图软件测试：
- **纯描边线稿（Pure Strokes）**：如 `coloring-page.svg`、`face-oneline.svg`、`icon-coffee.svg`、`single-line.svg`、`sketch-lines.svg`，所有路径均为 `fill="none"` 搭配 `stroke` 与 `stroke-width`。
- **描边 + 局部实心点缀（Strokes + Accent Fills）**：如 `botanical.svg`、`lighthouse.svg`、`bicycle.svg`、`cat-lines.svg`、`tattoo.svg`，主体线条为可调描边，局部色块（如浆果、灯室、瞳孔）为 `fill` 形状。
- **封闭填充轮廓（Filled Shapes）**：如 `laser-cut.svg`、`logo-mountain.svg`，仅使用封闭 `<path>` 与 `fill`（无 `stroke`），用于一体切割剪影或标志。

## 1. SVG 示例文件一览

> 注：「`<path>` 路径数量」为 XML 中 `<path>` 元素精确计数；部分文件还包含少量 `<circle>`、`<ellipse>`、`<line>`、`<polyline>` 或 `<polygon>` 基本图形。

| 文件 | 用途与结构说明 | 文件大小 | `<path>` 路径数量 |
|------|----------------|----------|-------------------|
| [`bicycle.svg`](./bicycle.svg) | 文字生成线稿插画：复古自行车侧视图，描边线条配赤陶色局部填充 | 31,357 B (30.6 KB) | 132 |
| [`bicycle-vectorize.svg`](./bicycle-vectorize.svg) | 图片描摹转线稿：复古自行车矢量描摹（描边为主，含少量填充细节） | 21,854 B (21.3 KB) | 138 |
| [`botanical.svg`](./botanical.svg) | 植物线稿：桉树枝叶鼠尾草绿描边 + 赤陶色实心浆果，适用于印刷品、标签与请柬 | 9,540 B (9.3 KB) | 47 |
| [`botanical-vectorize.svg`](./botanical-vectorize.svg) | 图片描摹植物线稿：枝叶描边搭配实心点缀色块 | 15,179 B (14.8 KB) | 97 |
| [`cat-lines.svg`](./cat-lines.svg) | 照片转线稿（对应输入图 [`cat-photo.jpg`](./cat-photo.jpg)）：猫咪可编辑描边线稿 | 20,868 B (20.4 KB) | 103 |
| [`coloring-page.svg`](./coloring-page.svg) | 可打印涂色页：蘑菇与蕨类中的狐狸，封闭轮廓、纯描边无填充，适用于儿童或成人涂色 | 37,778 B (36.9 KB) | 138 |
| [`cover-vectorize.svg`](./cover-vectorize.svg) | 图片/插画转 SVG（对应输入图 [`cover-input.png`](./cover-input.png)）：树叶枝条描边 + 实心色块 | 3,164 B (3.1 KB) | 14 |
| [`face-oneline.svg`](./face-oneline.svg) | 单线画 / 一笔画：极简侧脸连续线条，纯描边无填充，适用于绘图仪、烫金与刺绣 | 3,074 B (3.0 KB) | 12 |
| [`hero-camera.svg`](./hero-camera.svg) | 工作台演示线稿插画：深色描边线条（含 `<path>` 与 `<line>`）配赤陶色局部填充 | 20,344 B (19.9 KB) | 90 |
| [`icon-coffee.svg`](./icon-coffee.svg) | 线性图标 / SVG 编辑示例：手摇咖啡研磨机描边图标，纯描边无填充，适用于 App 与图标集 | 4,568 B (4.5 KB) | 17 |
| [`laser-cut.svg`](./laser-cut.svg) | 激光切割轮廓：山峰与松树圆形挂饰，一体相连的封闭填充剪影（无 `stroke`），适用于激光切割机与刻字机 | 4,638 B (4.5 KB) | 2 |
| [`lighthouse.svg`](./lighthouse.svg) | 文字生成插画线稿：礁石海岸灯塔、海浪与海鸟，描边配灯室赤陶色填充点缀 | 11,192 B (10.9 KB) | 40 |
| [`logo-mountain.svg`](./logo-mountain.svg) | Logo 矢量形状：山峰标志，封闭填充路径（无 `stroke`），可任意缩放与改色 | 1,031 B (1.0 KB) | 2 |
| [`single-line.svg`](./single-line.svg) | Cricut 单线文件：精致花环，每条线为单条开放描边路径、无双线、无填充，适用于笔绘、烫金与压痕划线 | 34,820 B (34.0 KB) | 115 |
| [`sketch-lines.svg`](./sketch-lines.svg) | 手绘草图转 SVG（对应输入图 [`sketch-input.jpg`](./sketch-input.jpg)）：茶壶与茶杯纯描边矢量线稿 | 7,636 B (7.5 KB) | 30 |
| [`tattoo.svg`](./tattoo.svg) | 细线纹身转印稿：蛇缠绕牡丹图案，线宽均匀、无灰阶阴影，适用于按尺寸打印转印 | 34,580 B (33.8 KB) | 108 |

## 2. 位图输入 → SVG 输出成对示例

| 输入位图文件 | 输入大小 | 输出 SVG 文件 | 输出大小 | 输出 `<path>` 数量 | 场景说明 |
|--------------|----------|---------------|----------|--------------------|----------|
| [`cat-photo.jpg`](./cat-photo.jpg) | 45,535 B (44.5 KB) | [`cat-lines.svg`](./cat-lines.svg) | 20,868 B (20.4 KB) | 103 | 实拍猫咪照片重绘为可调线宽的 SVG 线稿 |
| [`sketch-input.jpg`](./sketch-input.jpg) | 49,852 B (48.7 KB) | [`sketch-lines.svg`](./sketch-lines.svg) | 7,636 B (7.5 KB) | 30 | 铅笔手绘茶壶茶杯草图转换为干净纯描边 SVG |
| [`cover-input.png`](./cover-input.png) | 504,934 B (493.1 KB) | [`cover-vectorize.svg`](./cover-vectorize.svg) | 3,164 B (3.1 KB) | 14 | 位图树叶插画描摹为矢量描边与色块 |

## 3. 批量改样式输出示例（`examples/restyled/`）

以下文件由 `tools/svg_restyle.py` 实际生成，保留原始 `viewBox` 且通过 XML 解析校验：

| 输出文件 | 所用参数 | 文件大小 | `<path>` 路径数量 |
|----------|----------|----------|-------------------|
| [`restyled/coloring-page.svg`](./restyled/coloring-page.svg) | `--stroke-width 4 --stroke "#111827" --fill none` | 37,635 B (36.8 KB) | 138 |
| [`restyled/botanical.svg`](./restyled/botanical.svg) | `--stroke-width 2.5 --stroke "#1e3a5f"`（保留实心浆果填充） | 9,629 B (9.4 KB) | 47 |
| [`restyled/cat-lines.svg`](./restyled/cat-lines.svg) | `--stroke-width 2.2 --stroke "#2c3e50"` | 19,635 B (19.2 KB) | 103 |

---

<a id="english"></a>

# SVG Line Art Examples Index (`examples/`)

This directory contains 16 SVG vector examples across multiple vector structures, 3 paired raster-input → SVG-output examples, and 3 restyled outputs in `restyled/` produced by [`../tools/svg_restyle.py`](../tools/svg_restyle.py).

## 1. SVG Examples

| File | Use Case & Vector Structure | File Size | `<path>` Count |
|------|-----------------------------|-----------|----------------|
| [`bicycle.svg`](./bicycle.svg) | Text-to-line-art illustration: side-view vintage bicycle, strokes with terracotta accent fills | 31,357 B (30.6 KB) | 132 |
| [`bicycle-vectorize.svg`](./bicycle-vectorize.svg) | Traced line art from image: vintage bicycle, predominantly strokes with minor fills | 21,854 B (21.3 KB) | 138 |
| [`botanical.svg`](./botanical.svg) | Botanical line art: eucalyptus branch in sage-green strokes + solid terracotta berries (labels, invitations, print) | 9,540 B (9.3 KB) | 47 |
| [`botanical-vectorize.svg`](./botanical-vectorize.svg) | Traced botanical line art from image: foliage strokes + solid accent shapes | 15,179 B (14.8 KB) | 97 |
| [`cat-lines.svg`](./cat-lines.svg) | Photo to line art (paired with [`cat-photo.jpg`](./cat-photo.jpg)): editable cat line drawing | 20,868 B (20.4 KB) | 103 |
| [`coloring-page.svg`](./coloring-page.svg) | Printable coloring page: fox among mushrooms and ferns, closed outlines, pure strokes (`fill="none"`) | 37,778 B (36.9 KB) | 138 |
| [`cover-vectorize.svg`](./cover-vectorize.svg) | Image/illustration to SVG (paired with [`cover-input.png`](./cover-input.png)): traced leaf strokes + filled accents | 3,164 B (3.1 KB) | 14 |
| [`face-oneline.svg`](./face-oneline.svg) | One-line drawing: minimalist face profile, pure strokes (`fill="none"`), suited for plotters, foil, and embroidery | 3,074 B (3.0 KB) | 12 |
| [`hero-camera.svg`](./hero-camera.svg) | Workbench sample illustration: dark strokes (`<path>` and `<line>`) with terracotta accent fill | 20,344 B (19.9 KB) | 90 |
| [`icon-coffee.svg`](./icon-coffee.svg) | Line icon / SVG editor sample: hand-crank coffee grinder outline icon, pure strokes (`fill="none"`) | 4,568 B (4.5 KB) | 17 |
| [`laser-cut.svg`](./laser-cut.svg) | Laser-cut silhouette: connected mountain & pine ornament, closed filled shapes (no `stroke`) for laser & vinyl cutters | 4,638 B (4.5 KB) | 2 |
| [`lighthouse.svg`](./lighthouse.svg) | Text-to-illustration line art: coastal lighthouse, waves & seabirds, dark strokes + terracotta lantern fill | 11,192 B (10.9 KB) | 40 |
| [`logo-mountain.svg`](./logo-mountain.svg) | Logo vector shapes: mountain mark built from closed filled paths (no `stroke`) | 1,031 B (1.0 KB) | 2 |
| [`single-line.svg`](./single-line.svg) | Single-line SVG for Cricut / pen plotters: floral wreath, open strokes with no double outlines (`fill="none"`) for Draw, Foil & Score | 34,820 B (34.0 KB) | 115 |
| [`sketch-lines.svg`](./sketch-lines.svg) | Hand-drawn sketch to SVG (paired with [`sketch-input.jpg`](./sketch-input.jpg)): teapot & teacup pure-stroke line art | 7,636 B (7.5 KB) | 30 |
| [`tattoo.svg`](./tattoo.svg) | Fine-line tattoo stencil: snake and peony design, consistent thin strokes without grey shading | 34,580 B (33.8 KB) | 108 |

## 2. Raster Input → SVG Output Pairs

| Input Raster | Input Size | Output SVG | Output Size | Output `<path>` Count | Description |
|--------------|------------|------------|-------------|-----------------------|-------------|
| [`cat-photo.jpg`](./cat-photo.jpg) | 45,535 B (44.5 KB) | [`cat-lines.svg`](./cat-lines.svg) | 20,868 B (20.4 KB) | 103 | Camera photo of a cat converted into editable SVG strokes |
| [`sketch-input.jpg`](./sketch-input.jpg) | 49,852 B (48.7 KB) | [`sketch-lines.svg`](./sketch-lines.svg) | 7,636 B (7.5 KB) | 30 | Pencil sketch of a teapot and teacup converted into clean strokes |
| [`cover-input.png`](./cover-input.png) | 504,934 B (493.1 KB) | [`cover-vectorize.svg`](./cover-vectorize.svg) | 3,164 B (3.1 KB) | 14 | Raster botanical leaf illustration traced into vector strokes and fills |
