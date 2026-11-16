简体中文 | [English](#english)

# `svg_restyle.py` — 批量修改 SVG 线宽、颜色与填充的命令行工具

`svg_restyle.py` 是一个零第三方依赖、仅使用 Python 3 标准库（`xml.etree.ElementTree`）的命令行小工具，用于批量统一单个或整目录 SVG 线稿的描边粗细（`stroke-width`）、线条颜色（`stroke`）和填充（`fill`）。

## 特性

- **零外部依赖**：Python 3.9+ 标准库即可直接运行，无需 `pip install`。
- **兼容两种样式写法**：
  - SVG 直接表现属性：`stroke="#000" stroke-width="2" fill="none"`
  - 行内 CSS `style` 属性：`style="fill: none; stroke: #000; stroke-width: 2px; stroke-linecap: round"`（同时保留其他样式声明）
  - 含 `<style>` 简单类/标签规则（如 `.st0`）时，自动写入行内 `style` 保证优先级生效。
- **保留坐标与画布**：严格保持根元素 `viewBox`、`width`、`height` 及路径几何数据不变，并注册标准命名空间避免生成 `ns0:` 前缀。
- **默认保护实心点缀**：默认仅对已有有效描边（`stroke` 非空且不为 `none`/`transparent`，含从父级 `<g>` 继承的描边）的图形修改线宽与描边色，不会给原本无描边的实心色块（如植物浆果、人像瞳孔或背景块）强行加外框；如需为纯填充剪影统一加描边，可传入 `--all-shapes`。

## 命令行参数

```text
python3 tools/svg_restyle.py <input> <output_dir> [options]
```

| 参数 | 说明 |
|------|------|
| `input` 或 `-i, --input` | 输入 `.svg` 文件路径，或包含 `.svg` 文件的目录 |
| `output` 或 `-o, --output-dir` | 输出目录（当输入为单文件且该路径以 `.svg` 结尾时，也可直接指定输出文件路径） |
| `--stroke-width <值>` | 设置固定线宽，例如 `2`、`2.5`、`0.4mm`、`1.5px`（与 `--stroke-scale` 二选一） |
| `--stroke-scale <倍数>` | 按比例缩放原有线宽并保留原单位，例如 `1.5`（加粗 50%）或 `0.75` |
| `--stroke <颜色>` | 设置描边颜色，例如 `"#1e3a5f"`、`"black"`、`"currentColor"` |
| `--fill <填充>` | 可选，设置填充值，例如 `"none"`、`"#ffffff"`、`"transparent"` |
| `--all-shapes` | 可选，对原本没有 `stroke` 的图形也应用 `--stroke` 和 `--stroke-width` |
| `-r, --recursive` | 可选，输入为目录时递归处理子目录（会自动跳过位于输入目录内的输出目录） |

## 常用示例

1. **加粗单张涂色页线条并清除填充**：

```bash
python3 tools/svg_restyle.py examples/coloring-page.svg examples/restyled/ \
  --stroke-width 4 --stroke "#111827" --fill none
```

2. **给混合结构线稿换线条颜色与粗细（保留实心点缀色块）**：

```bash
python3 tools/svg_restyle.py examples/botanical.svg examples/restyled/ \
  --stroke-width 2.5 --stroke "#1e3a5f"
```

3. **批量把整个目录的 SVG 线宽放大 1.5 倍**：

```bash
python3 tools/svg_restyle.py examples/ ./out-scaled/ --stroke-scale 1.5
```

4. **将纯填充剪影（如激光切割轮廓）转为红色细描边路径**：

```bash
python3 tools/svg_restyle.py examples/laser-cut.svg ./out-cutline/ \
  --all-shapes --fill none --stroke "#dc2626" --stroke-width 0.5
```

---

<a id="english"></a>

# `svg_restyle.py` — Batch SVG Stroke Width, Color & Fill CLI

`svg_restyle.py` is a zero-dependency command-line utility built solely on the Python 3 standard library (`xml.etree.ElementTree`). It restyles `stroke-width`, `stroke` color, and `fill` across a single `.svg` file or an entire directory of SVGs.

## Features

- **Pure Python standard library**: Works with Python 3.9+ out of the box—no `pip install` needed.
- **Supports both SVG styling conventions**:
  - Direct presentation attributes (`stroke="#000" stroke-width="2" fill="none"`)
  - Inline CSS `style` attributes (`style="fill: none; stroke: #000; stroke-width: 2px; stroke-linecap: round"`), keeping non-paint declarations intact.
  - Also detects simple `<style>` class/tag paint rules (such as `.st0`) and writes inline `style` overrides when needed so CSS specificity is respected.
- **Preserves `viewBox` and clean namespaces**: Never alters `viewBox`, dimensions, or path coordinates, and registers SVG namespaces so outputs stay clean `<svg>` / `<path>` tags without `ns0:` prefixes.
- **Stroke-aware by default**: `--stroke` and `--stroke-width` / `--stroke-scale` target shapes that already have an active stroke (direct or inherited from `<g>`), leaving unstroked accent fills untouched. Pass `--all-shapes` when converting fill-only silhouettes into stroked paths.

## CLI Options

| Argument | Description |
|----------|-------------|
| `input` or `-i, --input` | Input `.svg` file or directory containing `.svg` files |
| `output` or `-o, --output-dir` | Output directory (or output `.svg` file path when input is a single file) |
| `--stroke-width <value>` | Set a fixed stroke width, e.g. `2`, `2.5`, `0.4mm`, `1.5px` (mutually exclusive with `--stroke-scale`) |
| `--stroke-scale <factor>` | Multiply existing stroke widths by a factor while keeping units, e.g. `1.5` |
| `--stroke <color>` | Set stroke color, e.g. `"#1e3a5f"`, `"black"`, `"currentColor"` |
| `--fill <value>` | Optional fill value, e.g. `"none"`, `"#ffffff"`, `"transparent"` |
| `--all-shapes` | Apply `--stroke` and `--stroke-width` to unstroked shapes as well |
| `-r, --recursive` | Recursively scan subdirectories when input is a directory (skips nested output directory) |

## Usage Examples

```bash
# Thicken outlines on a coloring page and force fill="none"
python3 tools/svg_restyle.py examples/coloring-page.svg examples/restyled/ \
  --stroke-width 4 --stroke "#111827" --fill none

# Recolor and resize strokes on a mixed botanical SVG while preserving berry fills
python3 tools/svg_restyle.py examples/botanical.svg examples/restyled/ \
  --stroke-width 2.5 --stroke "#1e3a5f"

# Batch-process a directory of SVGs
python3 tools/svg_restyle.py examples/ ./out-batch/ \
  --stroke-width 2 --stroke "#334155"
```
