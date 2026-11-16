#!/usr/bin/env python3
"""Batch restyle stroke width, stroke color, and fill in SVG line-art files.

Uses only the Python standard library (xml.etree.ElementTree).
Handles both SVG presentation attributes (stroke="...", stroke-width="...")
and inline CSS style attributes (style="stroke:...;stroke-width:..."),
while preserving viewBox and document structure.
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SVG_NS = "http://www.w3.org/2000/svg"
STANDARD_NAMESPACES = {
    "": SVG_NS,
    "xlink": "http://www.w3.org/1999/xlink",
    "inkscape": "http://www.inkscape.org/namespaces/inkscape",
    "sodipodi": "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
}

SHAPE_TAGS = frozenset(
    {"path", "line", "polyline", "polygon", "circle", "ellipse", "rect"}
)
CONTAINER_TAGS = frozenset({"svg", "g", "a", "symbol", "marker"})
SKIP_SUBTREE_TAGS = frozenset(
    {
        "defs",
        "clipPath",
        "mask",
        "pattern",
        "linearGradient",
        "radialGradient",
        "style",
        "script",
        "title",
        "desc",
        "metadata",
    }
)
PAINT_PROPS = frozenset({"stroke", "stroke-width", "fill"})
WIDTH_NUM_RE = re.compile(
    r"^\s*([+-]?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?)\s*([a-zA-Z%]*)\s*$",
    re.IGNORECASE,
)


def local_name(tag: str) -> str:
    """Strip XML namespace URI from an ElementTree tag."""
    if tag.startswith("{"):
        return tag.split("}", 1)[1]
    return tag


def parse_style_attr(style_text: str) -> List[Tuple[str, str, str]]:
    """Parse an inline CSS style string into [(prop_lower, value, important_suffix), ...]."""
    items: List[Tuple[str, str, str]] = []
    for chunk in style_text.split(";"):
        chunk = chunk.strip()
        if not chunk or ":" not in chunk:
            continue
        prop, raw_val = chunk.split(":", 1)
        prop_clean = prop.strip().lower()
        val_clean = raw_val.strip()
        important = ""
        if re.search(r"!\s*important\s*$", val_clean, flags=re.IGNORECASE):
            val_clean = re.sub(
                r"!\s*important\s*$", "", val_clean, flags=re.IGNORECASE
            ).strip()
            important = " !important"
        items.append((prop_clean, val_clean, important))
    return items


def format_style_attr(items: List[Tuple[str, str, str]]) -> str:
    """Serialize parsed inline CSS declarations back to a style attribute string."""
    return "; ".join(f"{k}: {v}{imp}" for k, v, imp in items)


def extract_stylesheet_paint_rules(
    root: ET.Element,
) -> List[Tuple[str, Dict[str, str]]]:
    """Extract basic paint declarations from <style> blocks (e.g. Illustrator .st0 classes).

    Ignores @keyframes/@media blocks so animations and media queries remain untouched.
    """
    rules: List[Tuple[str, Dict[str, str]]] = []
    for el in root.iter():
        if local_name(el.tag) != "style" or not el.text:
            continue
        # Remove comments and @-blocks conservatively for read-only matching
        cleaned = re.sub(r"/\*.*?\*/", "", el.text, flags=re.DOTALL)
        cleaned = re.sub(r"@[^{]+\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", cleaned)
        for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", cleaned):
            selectors_raw, body = match.group(1), match.group(2)
            decls = {
                k: v for k, v, _ in parse_style_attr(body) if k in PAINT_PROPS
            }
            if not decls:
                continue
            for sel in selectors_raw.split(","):
                sel = sel.strip()
                if sel:
                    rules.append((sel, decls))
    return rules


def match_simple_selector(el: ET.Element, selector: str) -> bool:
    """Match simple tag, .class, #id, or tag.class selectors on an element."""
    m = re.match(r"^([a-zA-Z][\w-]*|\*)?((?:[.#][\w-]+)*)$", selector)
    if not m:
        return False
    tag_part, qualifiers = m.group(1), m.group(2)
    if tag_part and tag_part != "*" and local_name(el.tag) != tag_part:
        return False
    classes = set((el.attrib.get("class") or "").split())
    el_id = el.attrib.get("id") or ""
    for token in re.findall(r"[.#][\w-]+", qualifiers or ""):
        if token.startswith(".") and token[1:] not in classes:
            return False
        if token.startswith("#") and token[1:] != el_id:
            return False
    return bool(tag_part or qualifiers)


def scale_width_value(raw_width: Optional[str], factor: float) -> str:
    """Multiply a numeric SVG stroke-width value by factor, keeping any unit."""
    base = (raw_width or "1").strip()
    m = WIDTH_NUM_RE.match(base)
    if not m:
        return base
    scaled = float(m.group(1)) * factor
    unit = m.group(2) or ""
    formatted = f"{scaled:.6g}"
    return f"{formatted}{unit}"


def set_paint_property(
    el: ET.Element,
    prop: str,
    new_value: str,
    force_inline_style: bool = False,
) -> None:
    """Set a paint property on an element, updating style="..." and/or direct attributes."""
    raw_style = el.attrib.get("style")
    if raw_style is not None:
        items = parse_style_attr(raw_style)
        keys = {k for k, _, _ in items}
        if prop in keys:
            updated = [
                (k, new_value if k == prop else v, imp) for k, v, imp in items
            ]
            el.set("style", format_style_attr(updated))
            if prop in el.attrib:
                el.set(prop, new_value)
            return
        if force_inline_style or (
            (keys & PAINT_PROPS) and prop not in el.attrib
        ):
            items.append((prop, new_value, ""))
            el.set("style", format_style_attr(items))
            if prop in el.attrib:
                el.set(prop, new_value)
            return

    if force_inline_style:
        el.set("style", f"{prop}: {new_value}")
        if prop in el.attrib:
            el.set(prop, new_value)
    else:
        el.set(prop, new_value)


def is_active_stroke(stroke_val: Optional[str]) -> bool:
    """Return True if an effective stroke value draws a visible stroke."""
    if not stroke_val:
        return False
    norm = stroke_val.strip().lower()
    return norm not in ("none", "transparent")


def register_file_namespaces(svg_path: Path) -> None:
    """Register standard SVG namespaces plus any custom prefixes declared in the file."""
    for prefix, uri in STANDARD_NAMESPACES.items():
        ET.register_namespace(prefix, uri)
    try:
        for _, ns_pair in ET.iterparse(str(svg_path), events=("start-ns",)):
            prefix, uri = ns_pair
            if uri == SVG_NS:
                ET.register_namespace("", SVG_NS)
            elif prefix and prefix not in STANDARD_NAMESPACES:
                ET.register_namespace(prefix, uri)
    except ET.ParseError:
        pass


def restyle_svg_file(
    src_path: Path,
    dst_path: Path,
    stroke_width: Optional[str] = None,
    stroke_scale: Optional[float] = None,
    stroke_color: Optional[str] = None,
    fill_color: Optional[str] = None,
    all_shapes: bool = False,
) -> Tuple[int, int, str]:
    """Restyle one SVG file and write to dst_path.

    Returns (updated_shapes, skipped_shapes, viewbox).
    """
    raw_text = src_path.read_text(encoding="utf-8")
    if re.search(r"<!ENTITY", raw_text, flags=re.IGNORECASE):
        raise ValueError(f"Rejected XML entity declaration in {src_path}")

    register_file_namespaces(src_path)
    tree = ET.ElementTree(ET.fromstring(raw_text))
    root = tree.getroot()
    if local_name(root.tag) != "svg":
        raise ValueError(f"Root element is <{local_name(root.tag)}>, expected <svg>")

    original_viewbox = root.attrib.get("viewBox")
    stylesheet_rules = extract_stylesheet_paint_rules(root)

    updated_shapes = 0
    skipped_shapes = 0

    def walk(el: ET.Element, inherited: Dict[str, Optional[str]]) -> None:
        nonlocal updated_shapes, skipped_shapes
        tag = local_name(el.tag)
        if tag in SKIP_SUBTREE_TAGS:
            return

        current = dict(inherited)
        from_stylesheet: Dict[str, str] = {}
        for sel, decls in stylesheet_rules:
            if match_simple_selector(el, sel):
                from_stylesheet.update(decls)
                current.update(decls)

        for prop in PAINT_PROPS:
            if prop in el.attrib:
                current[prop] = el.attrib[prop]

        inline_decls: Dict[str, str] = {}
        if "style" in el.attrib:
            inline_decls = {
                k: v
                for k, v, _ in parse_style_attr(el.attrib["style"])
                if k in PAINT_PROPS
            }
            current.update(inline_decls)

        if tag in CONTAINER_TAGS:
            # Keep explicit presentation attributes on groups/containers consistent
            own_props = set(inline_decls.keys()) | (
                set(el.attrib.keys()) & PAINT_PROPS
            )
            if stroke_color is not None and "stroke" in own_props:
                if is_active_stroke(current.get("stroke")) or all_shapes:
                    set_paint_property(el, "stroke", stroke_color)
            if stroke_width is not None and "stroke-width" in own_props:
                set_paint_property(el, "stroke-width", stroke_width)
            elif stroke_scale is not None and "stroke-width" in own_props:
                set_paint_property(
                    el,
                    "stroke-width",
                    scale_width_value(current.get("stroke-width"), stroke_scale),
                )
            if fill_color is not None and "fill" in own_props:
                set_paint_property(el, "fill", fill_color)

            for child in list(el):
                walk(child, current)
            return

        if tag in SHAPE_TAGS:
            has_stroke = is_active_stroke(current.get("stroke"))
            touched = False

            if has_stroke or all_shapes:
                if stroke_color is not None:
                    set_paint_property(
                        el,
                        "stroke",
                        stroke_color,
                        force_inline_style=("stroke" in from_stylesheet),
                    )
                    touched = True
                if stroke_width is not None:
                    set_paint_property(
                        el,
                        "stroke-width",
                        stroke_width,
                        force_inline_style=("stroke-width" in from_stylesheet),
                    )
                    touched = True
                elif stroke_scale is not None:
                    new_w = scale_width_value(
                        current.get("stroke-width"), stroke_scale
                    )
                    set_paint_property(
                        el,
                        "stroke-width",
                        new_w,
                        force_inline_style=("stroke-width" in from_stylesheet),
                    )
                    touched = True

            if fill_color is not None:
                set_paint_property(
                    el,
                    "fill",
                    fill_color,
                    force_inline_style=("fill" in from_stylesheet),
                )
                touched = True

            if touched:
                updated_shapes += 1
            else:
                skipped_shapes += 1

        for child in list(el):
            walk(child, current)

    walk(root, {"stroke": None, "stroke-width": None, "fill": None})

    # Guarantee viewBox is preserved verbatim
    if original_viewbox is not None and root.attrib.get("viewBox") != original_viewbox:
        root.set("viewBox", original_viewbox)

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(str(dst_path), encoding="utf-8", xml_declaration=False)
    return updated_shapes, skipped_shapes, original_viewbox or "(none)"


def collect_svg_targets(
    input_path: Path, output_path: Path, recursive: bool = False
) -> List[Tuple[Path, Path]]:
    """Resolve input file/directory and output directory/file into (src, dst) pairs."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")

    if input_path.is_file():
        if input_path.suffix.lower() != ".svg":
            raise ValueError(f"Input file must be an .svg file: {input_path}")
        if output_path.suffix.lower() == ".svg" and not output_path.is_dir():
            return [(input_path, output_path)]
        return [(input_path, output_path / input_path.name)]

    pattern = "**/*.svg" if recursive else "*.svg"
    out_resolved = output_path.resolve()
    pairs: List[Tuple[Path, Path]] = []
    for svg_file in sorted(input_path.glob(pattern)):
        if not svg_file.is_file():
            continue
        # Skip files inside output directory when output_dir is nested inside input_dir
        try:
            svg_file.resolve().relative_to(out_resolved)
            continue
        except ValueError:
            pass
        rel = svg_file.relative_to(input_path)
        pairs.append((svg_file, output_path / rel))
    return pairs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Batch restyle stroke width, stroke color, and fill in SVG files "
            "using only Python's standard library (xml.etree.ElementTree)."
        )
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Input .svg file or directory containing .svg files.",
    )
    parser.add_argument(
        "output",
        nargs="?",
        help="Output directory (or output .svg file when input is a single file).",
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="input_opt",
        help="Input .svg file or directory (alternative to positional input).",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        "--output",
        dest="output_opt",
        help="Output directory or .svg file (alternative to positional output).",
    )

    width_group = parser.add_mutually_exclusive_group()
    width_group.add_argument(
        "--stroke-width",
        help='Set fixed stroke width, e.g. "2", "2.5", "0.4mm", "1.5px".',
    )
    width_group.add_argument(
        "--stroke-scale",
        type=float,
        help="Multiply existing stroke widths by a factor, e.g. 1.5 or 0.75.",
    )

    parser.add_argument(
        "--stroke",
        help='Set stroke color, e.g. "#1e293b", "black", "currentColor".',
    )
    parser.add_argument(
        "--fill",
        help='Set fill value, e.g. "none", "#ffffff", "transparent".',
    )
    parser.add_argument(
        "--all-shapes",
        action="store_true",
        help=(
            "Also apply --stroke and --stroke-width to shapes that previously had no stroke "
            "(useful for converting fill-only silhouettes to stroked outlines)."
        ),
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursively scan subdirectories when input is a directory.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    in_raw = args.input_opt or args.input
    out_raw = args.output_opt or args.output
    if not in_raw or not out_raw:
        parser.error("both input path and output directory/path are required.")

    if (
        args.stroke_width is None
        and args.stroke_scale is None
        and args.stroke is None
        and args.fill is None
    ):
        parser.error(
            "specify at least one style option: --stroke-width, --stroke-scale, --stroke, or --fill."
        )

    if args.stroke_scale is not None and args.stroke_scale <= 0:
        parser.error("--stroke-scale must be greater than 0.")

    input_path = Path(in_raw)
    output_path = Path(out_raw)

    try:
        targets = collect_svg_targets(
            input_path, output_path, recursive=args.recursive
        )
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not targets:
        print(f"No .svg files found in {input_path}", file=sys.stderr)
        return 1

    for src, dst in targets:
        try:
            updated, skipped, vb = restyle_svg_file(
                src_path=src,
                dst_path=dst,
                stroke_width=args.stroke_width,
                stroke_scale=args.stroke_scale,
                stroke_color=args.stroke,
                fill_color=args.fill,
                all_shapes=args.all_shapes,
            )
            note = (
                f" ({skipped} unstroked shape(s) preserved)"
                if skipped
                else ""
            )
            print(
                f"[OK] {src} -> {dst} | updated={updated}{note} | viewBox={vb}"
            )
        except Exception as exc:  # noqa: BLE001
            print(f"[ERROR] {src}: {exc}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
