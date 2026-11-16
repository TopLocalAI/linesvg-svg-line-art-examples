English | [简体中文](./editing-svg-line-art.md)

# Editing SVG Line Art: Structure, Code & Craft Guidelines

An `.svg` extension alone does not guarantee that a drawing's lines can be thickened or recolored cleanly. Some SVGs store every stroke as a true centerline path whose thickness is controlled by `stroke-width`; others trace both outer edges of each line into closed filled shapes (`fill`), or simply wrap a raster image inside an `<image>` tag.

Using the real files in [`examples/`](../examples/), this guide explains the XML structure of editable SVG line art, how stroked paths differ from filled outlines, how to change line weight and color in code, and what to check before sending an SVG to a laser cutter, plotter, printer, embroidery workflow, or tattoo stencil printer.

---

## 1. Basic Structure of SVG Line Art

Open a clean line-art file such as [`../examples/face-oneline.svg`](../examples/face-oneline.svg) in a text editor and you will see four core building blocks:

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

### 1.1 `viewBox`: The Internal Coordinate Space Behind `stroke-width`

- `viewBox="min-x min-y width height"` defines the internal user coordinate system of the SVG, while `width` and `height` on `<svg>` set its default rendered size.
- **Unitless `stroke-width` values are measured in `viewBox` user units**:
  - On `viewBox="0 0 1000 1000"` (e.g. [`../examples/face-oneline.svg`](../examples/face-oneline.svg)), `stroke-width="4"` is `0.4%` of the canvas width—a crisp thin line.
  - On `viewBox="0 0 150 150"` (e.g. [`../examples/botanical-vectorize.svg`](../examples/botanical-vectorize.svg)), the same visual weight is around `stroke-width="0.6"`; setting `stroke-width="4"` there makes lines `2.7%` of the canvas width and visibly heavy.
- **Golden rule**: Never strip or alter `viewBox` when restyling strokes, or the artwork will clip, shift, or scale unexpectedly.

### 1.2 `<path>` and Basic Shape Primitives

- `<path d="...">` carries most freehand and traced geometry. Its `d` string chains move (`M`/`m`), line (`L`/`l`, `H`, `V`), cubic/quadratic Bézier (`C`/`S`, `Q`/`T`), arc (`A`), and close-path (`Z`/`z`) commands:
  - Paths without a trailing `Z` are **open paths** (typical of single-line portraits and pen-plotter art).
  - Paths ending in `Z` are **closed paths** (typical of enclosed coloring regions and cut silhouettes).
- Line drawings may also include `<line>`, `<polyline>`, `<polygon>`, `<circle>`, `<ellipse>`, and `<rect>`, often wrapped in `<g>` groups that pass shared attributes down to child shapes.

### 1.3 `stroke` and `fill` (Watch Out for the Default Black Fill)

- `stroke`: Line color (`"#1E1D1B"`, `"black"`, `"currentColor"`). If omitted or `"none"`, no stroke is drawn.
- `stroke-width`: Line thickness.
- `stroke-linecap` / `stroke-linejoin`: End-cap style (`round`, `butt`, `square`) and corner join (`round`, `miter`, `bevel`). `round` caps and joins prevent sharp miter spikes on tight hand-drawn corners.
- `fill`: Interior paint of a shape.
  - **Critical SVG detail**: Per the SVG specification, **omitting `fill` defaults to solid black (`#000000`), not transparent**. On an open curved `<path>`, omitting `fill="none"` fills the chord between start and end points with a black wedge. Always set `fill="none"` explicitly on open line paths (or on their parent `<g>`).

---

## 2. Editable Strokes vs. Filled Outlines

Two black-and-white SVGs can look identical on screen while behaving completely differently when edited or sent to a machine:

| Aspect | Editable Strokes (Centerline) | Filled Outlines (Expanded Shapes) |
|--------|-------------------------------|-----------------------------------|
| Geometry | A single centerline `<path>` given thickness by `stroke-width` | Closed outer + inner boundaries filled with `fill` color (no `stroke`) |
| Repo examples | [`coloring-page.svg`](../examples/coloring-page.svg), [`single-line.svg`](../examples/single-line.svg), [`face-oneline.svg`](../examples/face-oneline.svg) | [`laser-cut.svg`](../examples/laser-cut.svg), [`logo-mountain.svg`](../examples/logo-mountain.svg) |
| Changing line weight | Change `stroke-width` directly to make lines thinner or thicker | Adding `stroke-width` only paints an extra border outside the filled ribbon; cannot thin lines cleanly |
| Dashed lines | `stroke-dasharray` creates dashes along the line | Dashes trace around both outer edges of the ribbon |
| Pen plotter / Cricut Draw | Pen follows each centerline once | Pen traces both left and right edges of every line ("double-line problem") |
| Best suited for | Illustration refinement, coloring pages, UI icons, pen plotters, Foil & Score | Through-cut laser silhouettes, vinyl decals, fixed-proportion logos |

Many illustrations also use a **mixed structure (strokes + accent fills)**—for instance, [`../examples/botanical.svg`](../examples/botanical.svg) draws eucalyptus leaves with `stroke="#6D8F7C" fill="none"` while keeping the berries as solid `fill="#BE6445"` shapes without strokes. When batch-editing line weight, only shapes that already carry a stroke should be restyled so solid accents stay intact.

### How to Tell Which Structure an SVG Uses

1. **Inspect the source**: Open the `.svg` in any text editor and check `<path>` attributes. `stroke="..."` + `stroke-width="..."` + `fill="none"` means editable strokes; `fill="#..."` with no `stroke` means filled shapes; an `<image xlink:href="data:image/png;base64,...">` tag means a raster image wrapped inside an SVG container rather than vector paths.
2. **Check in a vector editor**: Open the file in Illustrator, Inkscape, or Figma and switch to wireframe/outline view—editable strokes appear as single spine curves, whereas filled outlines show paired edges around every mark. Selecting a path and checking the Stroke and Fill panels also reveals immediately which property is active.

---

## 3. How to Change Stroke Width and Color in Code

### 3.1 Styling Conventions and CSS Specificity in SVG

Exporters write stroke and fill styles in three common ways:

1. **Presentation attributes**:
   ```xml
   <path d="M10 20 L90 20" fill="none" stroke="#333333" stroke-width="2" />
   ```
2. **Inline CSS `style` attribute** (common in Inkscape exports):
   ```xml
   <path d="M10 20 L90 20" style="fill:none;stroke:#333333;stroke-width:2px;stroke-linecap:round" />
   ```
3. **Internal `<style>` stylesheet classes** (common in some desktop vector exports):
   ```xml
   <style>.st0 { fill: none; stroke: #333333; stroke-width: 2px; }</style>
   <path class="st0" d="M10 20 L90 20" />
   ```

**Specificity order**:
`Inline style="..."` **overrides** `<style> .class / tag rules`, which **override** `presentation attributes (stroke="...")`, which **override** `inherited <g> attributes`.

> If you add `stroke="#ff0000"` to `<path style="stroke:#000" ...>` and nothing changes, inline `style` is winning. Update `stroke` inside `style="..."` as well.

### 3.2 Web & UI Techniques

- **Inherit text color with `currentColor`** (handy for outline icons like [`icon-coffee.svg`](../examples/icon-coffee.svg)):
  ```xml
  <path d="..." fill="none" stroke="currentColor" stroke-width="2" />
  ```
- **Keep constant screen stroke thickness while scaling**:
  Add `vector-effect="non-scaling-stroke"` on stroked elements so resizing the `<svg>` container does not make lines overly thick or faint.

### 3.3 Batch Editing from the Command Line

[`../tools/svg_restyle.py`](../tools/svg_restyle.py) uses only Python's standard library (`xml.etree.ElementTree`), handles both presentation attributes and inline `style="..."`, preserves `viewBox`, and leaves unstroked accent fills untouched by default:

```bash
# Thicken a coloring page to stroke-width 4 with dark charcoal lines and no fill
python3 tools/svg_restyle.py examples/coloring-page.svg examples/restyled/ \
  --stroke-width 4 --stroke "#111827" --fill none

# Scale existing stroke widths across a directory by 1.5x
python3 tools/svg_restyle.py examples/ ./out-scaled/ --stroke-scale 1.5
```

For interactive tweaks in Illustrator, Inkscape, or Figma, select the target paths (or select objects sharing the same stroke style) and adjust line weight, cap/join style, and color directly in the Stroke panel.

---

## 4. Practical Considerations by Use Case

### 4.1 Laser Cutting, Vinyl Cutters & Pen Plotters (Cricut / Plotter)

First decide whether the machine tool will **cut through material** or **follow single lines**:

- **Through-cutting (laser cutters & vinyl cutters, e.g. [`../examples/laser-cut.svg`](../examples/laser-cut.svg))**:
  - **Closed, connected geometry**: All positive parts that must stay together need to form a connected closed silhouette (`Z`). Unbridged interior islands (like the center of an `O` or floating leaves) will drop out once cut.
  - **Avoid fragile slivers and stacked duplicates**: Very narrow bridges char under a laser beam or lift when weeding vinyl, and overlapping duplicate paths cause the laser to burn the same cut line twice.
  - **Verify physical units**: Unitless `viewBox` coordinates may import at 72 DPI or 96 DPI depending on the cutter software; always check physical dimensions (`mm` or `in`) before cutting.
- **Pen plotting, foil transfer & scoring (e.g. [`../examples/single-line.svg`](../examples/single-line.svg))**:
  - Use **open or single-pass centerline strokes** with `fill="none"`. Avoid expanded filled outlines so the pen, foil tip, or scoring wheel travels along each line once rather than tracing both edges.

### 4.2 Printable Coloring Pages (e.g. [`../examples/coloring-page.svg`](../examples/coloring-page.svg))

- **Crisp dark outlines with `fill="none"`**: Remove greyscale shading blocks and background rectangles so home printers output clean black lines on white paper without wasting toner.
- **Closed regions and open white space**: Enclosed shapes make boundaries clear on paper and allow flood-fill ("paint bucket") coloring in tablet apps.
- **Match line weight to the audience**: Thicker strokes work better for young children using crayons or markers; finer strokes suit detailed adult coloring sheets with colored pencils. Export to vector PDF or 300 DPI PNG at target paper size for sharp printing.

### 4.3 Embroidery & Tattoo Stencils

- **Tattoo stencils (e.g. [`../examples/tattoo.svg`](../examples/tattoo.svg))**:
  - Thermal stencil printers transfer crisp linework rather than smooth greyscale gradients, so stencil SVGs should use consistent stroke weight with no grey shading or heavy black fills.
  - Preview the design scaled to actual body placement size to ensure closely spaced parallel lines keep enough breathing room not to merge during transfer or healing. `stroke-linecap="round"` and `stroke-linejoin="round"` keep scaled corners clean.
- **Embroidery patterns (e.g. [`../examples/face-oneline.svg`](../examples/face-oneline.svg))**:
  - **SVG is vector geometry, not a machine stitch file**: Automated embroidery machines read stitch formats (such as `.DST`, `.PES`, or `.JEF`) generated by embroidery digitizing software that assigns running stitches, satin columns, or fill stitches.
  - Whether preparing artwork for digitizing software or printing a hand-embroidery transfer pattern, remove tiny stray path fragments smaller than needle/thread width, eliminate overlapping line segments, and keep line strokes cleanly separated from solid filled areas.
