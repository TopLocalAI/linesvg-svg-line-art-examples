[English](./editing-svg-line-art.en.md) | 简体中文

# SVG 线稿结构与编辑指南

一份扩展名为 `.svg` 的文件，并不一定意味着“里面的线条可以直接改粗细”。有的 SVG 用真正的中心线描边（Stroke）记录每一笔，改一个数字就能把整张图调粗或换色；有的 SVG 只是把线条边缘描成了闭合填充色块（Fill），甚至在 `<image>` 标签里塞了一张位图。

本文结合仓库 [`examples/`](../examples/) 中的真实文件，说明可编辑 SVG 线稿的底层结构、描边与填充轮廓的区别、代码级修改方法，以及用于激光切割、涂色页、刺绣与纹身转印稿时的检查要点。

---

## 1. SVG 线稿的基本结构

打开任意一张干净的矢量线稿（例如 [`../examples/face-oneline.svg`](../examples/face-oneline.svg)），核心结构通常由四个部分组成：

```xml
<svg width="1000" height="1000" viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
  <g stroke-linecap="round" stroke-linejoin="round">
    <path
      d="M 220 310 C 260 180, 420 180, 460 310"
      fill="none"
      stroke="#1E1D1B"
      stroke-width="4"
    />
  </g>
</svg>
```

### 1.1 `viewBox`：决定线宽视觉比例的内部坐标系

- `viewBox="min-x min-y width height"` 定义了 SVG 内部的虚拟画布坐标范围；根元素上的 `width` 和 `height` 则决定默认显示尺寸。
- **不带单位的 `stroke-width` 以 `viewBox` 用户坐标为单位**。例如：
  - 在 `viewBox="0 0 1000 1000"` 的画布中（如 [`../examples/face-oneline.svg`](../examples/face-oneline.svg)），`stroke-width="4"` 占画布宽度的 `0.4%`，视觉上是利落的细线；
  - 在 `viewBox="0 0 150 150"` 的画布中（如 [`../examples/botanical-vectorize.svg`](../examples/botanical-vectorize.svg)），同样粗细的线条对应 `stroke-width="0.6"`，如果直接改成 `4` 就会占画布宽度的 `2.7%`，视觉上变得很粗。
- **编辑原则**：修改线宽和颜色时不要删改 `viewBox`，否则整张画稿会出现裁切偏移或比例失真。

### 1.2 `<path>` 与基本图形元素

- `<path d="...">` 是线稿中最常见的几何载体，`d` 属性由移动（`M`/`m`）、直线（`L`/`l`、`H`、`V`）、三次/二次贝塞尔曲线（`C`/`S`、`Q`/`T`）、圆弧（`A`）和闭合指令（`Z`/`z`）拼成。
  - 不以 `Z` 结尾的是**开放路径**（常见于单线画、面部五官线条）；
  - 以 `Z` 结尾的是**闭合路径**（常见于涂色分区、激光切割外轮廓）。
- 除 `<path>` 外，SVG 线稿也常混用 `<line>`、`<polyline>`、`<polygon>`、`<circle>`、`<ellipse>`、`<rect>`，并通过 `<g>` 分组统一继承样式。

### 1.3 `stroke` 与 `fill`（特别注意默认填充陷阱）

- `stroke`：线条颜色（如 `"#1E1D1B"`、`"black"`、`"currentColor"`）；未设置或设为 `"none"` 时不绘制描边。
- `stroke-width`：线条粗细。
- `stroke-linecap` / `stroke-linejoin`：线端样式（`round` 圆头、`butt` 平头、`square` 方头）与转角连接（`round` 圆角、`miter` 尖角、`bevel` 斜角）。手绘感线稿通常使用 `round` 以避免折角出现尖刺。
- `fill`：路径内部填充颜色。
  - **关键细节**：根据 SVG 规范，**省略 `fill` 属性时默认值是纯黑（`#000000`），而不是透明**。对于一条未闭合的弯曲 `<path>`，如果不写 `fill="none"`，浏览器和矢量软件会自动把起点到终点连线围成的弦月区域涂黑。因此纯线条路径务必显式声明 `fill="none"`（写在元素自身或外层 `<g>` 上）。

---

## 2. 描边线稿与填充轮廓的区别

外观相似的两张黑白矢量图，底层结构可能完全不同：

| 对比维度 | 描边线稿（Editable Strokes） | 填充轮廓（Filled Outlines / Shapes） |
|----------|------------------------------|--------------------------------------|
| 几何本质 | 一条沿着笔迹中心走的 `<path>`，靠 `stroke-width` 赋予粗细 | 用闭合外圈 + 内圈围出“线条两侧边缘”，内部涂满 `fill` 色 |
| 仓库示例 | [`coloring-page.svg`](../examples/coloring-page.svg)、[`single-line.svg`](../examples/single-line.svg)、[`face-oneline.svg`](../examples/face-oneline.svg) | [`laser-cut.svg`](../examples/laser-cut.svg)、[`logo-mountain.svg`](../examples/logo-mountain.svg) |
| 改线条粗细 | 直接调整 `stroke-width` 即可无损变粗或变细 | 改 `stroke-width` 只会在色块外再套一圈描边，无法直接把原线条“变细” |
| 改虚线效果 | 设置 `stroke-dasharray` 即可生成沿线虚线 | `stroke-dasharray` 会绕着轮廓两侧边缘打点，无法变成单排虚线 |
| 绘图仪 / 笔绘机行为 | 笔尖沿中心路径走一遍 | 笔尖会沿线条左右两侧边缘各走一遍（俗称“双线问题”） |
| 典型适用场景 | 插画精修、涂色页、UI 图标、绘图仪笔绘、Cricut 烫金/压痕 | 激光切割一体剪影、刻字膜镂空贴纸、固定字形/Logo 印刷 |

此外，很多插画采用**“描边 + 局部实心点缀”的混合结构**——例如 [`../examples/botanical.svg`](../examples/botanical.svg) 中，桉树枝叶是 `stroke="#6D8F7C" fill="none"` 的可调描边，浆果则是 `fill="#BE6445"`（无 `stroke`）的实心色块。批量改线宽时，只改已有描边的元素才能保住实心浆果的原貌。

### 如何快速分辨手头的 SVG 是哪一种？

1. **看源码**：用任意文本编辑器打开 `.svg`，搜索 `<path`——看到 `stroke="..."`、`stroke-width="..."` 且 `fill="none"` 是描边线稿；只有 `fill="#..."` 而没有 `stroke` 则是填充轮廓；如果看到 `<image xlink:href="data:image/png;base64,...">`，说明只是把位图嵌进了 SVG 外壳，并非矢量路径。
2. **在矢量软件中查看**：将文件拖入 Illustrator、Inkscape 或 Figma，切换到线框/轮廓预览视图——中心线描边只会显示单根骨架线，而填充轮廓在每根线条两侧都会显示一对闭合边线；选中路径后，也可以直接在描边（Stroke）与填充（Fill）面板中查看当前生效的是哪一项。

---

## 3. 怎么在代码里修改线宽与颜色

### 3.1 识别 SVG 中的两种样式写法与优先级

不同工具导出的 SVG 会用不同语法记录颜色和线宽：

1. **直接表现属性（Presentation Attributes）**：
   ```xml
   <path d="M10 20 L90 20" fill="none" stroke="#333333" stroke-width="2" />
   ```
2. **行内 CSS `style` 属性（常见于 Inkscape 等工具导出）**：
   ```xml
   <path d="M10 20 L90 20" style="fill:none;stroke:#333333;stroke-width:2px;stroke-linecap:round" />
   ```
3. **内部 `<style>` 样式表类选择器（常见于部分设计软件导出）**：
   ```xml
   <style>.st0 { fill: none; stroke: #333333; stroke-width: 2px; }</style>
   <path class="st0" d="M10 20 L90 20" />
   ```

**CSS 优先级规则**：
`行内 style="..."` **高于** `<style> 中的 .class / 标签规则` **高于** `元素直接属性 stroke="..."` **高于** `父级 <g> 继承属性`。

> 这就是为什么很多人在代码里给 `<path style="stroke:#000" ...>` 加上 `stroke="#ff0000"` 后发现颜色根本没变——行内 `style` 覆盖了直接属性，必须同步修改 `style` 里的 `stroke` 声明。

### 3.2 常用网页与组件级改法

- **跟随文字颜色自动变色（适合线性图标，如 [`icon-coffee.svg`](../examples/icon-coffee.svg)）**：
  将 `stroke` 设为 `"currentColor"`，外部 HTML/CSS 改 `color` 即可联动换色：
  ```xml
  <path d="..." fill="none" stroke="currentColor" stroke-width="2" />
  ```
- **缩放画布时保持屏幕像素线宽恒定**：
  在 `<path>` 上添加 `vector-effect="non-scaling-stroke"`，即使 SVG 在网页中被放大或缩小，描边粗细仍保持固定的像素值而不随图形等比变粗或发虚。

### 3.3 使用命令行批量修改

仓库自带的 [`../tools/svg_restyle.py`](../tools/svg_restyle.py) 仅使用 Python 标准库，自动兼容直接属性与 `style="..."` 两种写法，并在不破坏 `viewBox` 和实心点缀的前提下批量处理单文件或整目录：

```bash
# 将单张涂色页统一加粗为线宽 4、深灰色描边、无填充
python3 tools/svg_restyle.py examples/coloring-page.svg examples/restyled/ \
  --stroke-width 4 --stroke "#111827" --fill none

# 将目录内所有 SVG 的原有线宽按 1.5 倍等比加粗
python3 tools/svg_restyle.py examples/ ./out-scaled/ --stroke-scale 1.5
```

如果在 Illustrator、Inkscape 或 Figma 等桌面/网页矢量编辑器中手动微调，只需选中目标路径（或按相同描边属性批量选中图形），在描边（Stroke）面板中统一调整线宽数值、端点/转角样式与颜色即可。

---

## 4. 不同下游场景的注意事项

### 4.1 激光切割、刻字机与绘图仪（Cricut / 笔绘机）

先明确设备要执行的是**切割穿透（Cut）**还是**单轨走线（Draw / Foil / Score）**：

- **激光切割与刻字膜切割（参考 [`../examples/laser-cut.svg`](../examples/laser-cut.svg)）**：
  - **路径闭合且整体相连**：需要保留在成品上的各个部件必须连成一体轮廓（`Z` 闭合路径），否则内部未桥接的“悬空孤岛”（例如字母 `O` 中间的圆芯或独立漂浮的树叶）切穿后会直接掉落。
  - **避免过窄细边与重叠线**：过窄的连接桥在激光下容易烧穿碳化，在刻字膜上容易揭膜断裂；同时检查是否有完全重合的两条路径，防止激光头在同一条线上重复灼烧两遍。
  - **核对物理尺寸单位**：纯数字 `viewBox` 导入不同切割软件时可能按 72 DPI 或 96 DPI 换算尺寸，切割前务必在控制软件中确认实际毫米（`mm`）或英寸（`in`）长宽。
- **绘图仪笔绘、烫金与压痕划线（参考 [`../examples/single-line.svg`](../examples/single-line.svg)）**：
  - 应使用 `fill="none"` 的**单中心线描边路径**，每根可见线条只对应一条 `<path>`，避免使用闭合填充轮廓，否则笔尖会沿着同一根线的左右外缘走两道。

### 4.2 可打印涂色页（参考 [`../examples/coloring-page.svg`](../examples/coloring-page.svg)）

- **纯线条无灰阶阴影**：保留清晰的黑白或深色轮廓线，设 `fill="none"`，清除照片阴影色块与背景底框，避免家庭喷墨/激光打印机浪费墨粉或印出灰底。
- **闭合分区与充足留白**：待涂色区域轮廓尽量闭合、少留碎线，方便小朋友辨识边界，也方便电子涂色软件使用油漆桶填充。
- **按使用人群匹配线宽**：低龄儿童使用蜡笔或水彩笔时可将 `stroke-width` 适当调粗；成人减压涂色页搭配彩铅或细头针管笔时可调细线宽。打印前建议导出为矢量 PDF 或按纸张尺寸导出 300 DPI PNG。

### 4.3 刺绣与纹身转印稿

- **纹身转印稿（参考 [`../examples/tattoo.svg`](../examples/tattoo.svg)）**：
  - 热转印机和转印纸擅长还原清晰的实线，无法平滑还原连续灰阶渐变，因此转印底稿应采用线宽一致、无灰阶阴影、无大块黑底的纯描边结构。
  - 缩放到实际身体部位尺寸打印前，检查密集平行线（如花瓣褶皱、蛇鳞细节）之间的白隙是否足够宽，防止转印墨迹粘连或恢复后晕开糊成一团；使用 `stroke-linecap="round"` 与 `stroke-linejoin="round"` 能让缩放后的转角更柔和干净。
- **刺绣底稿（参考 [`../examples/face-oneline.svg`](../examples/face-oneline.svg)）**：
  - **区分矢量文件与机绣针迹文件**：SVG 记录的是几何曲线，**不是**绣花机直接读取的针迹格式（如 `.DST`、`.PES`、`.JEF`）。用于电脑绣花机时，仍需将 SVG 导入刺绣打版软件分配平针（Running Stitch）、缎纹针（Satin）或榻榻米填充针迹参数。
  - 无论是用于机绣打版底图还是打印出来做手工刺绣描图，都建议提前删除小于针线直径的细碎杂点与重叠短线，并将走线描边路径与实心填充色块分清层次，能大幅减少打版跳针与手工走线混乱。
