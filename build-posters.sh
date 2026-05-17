#!/bin/bash
# Сборка плакатов и листа с ГОСТ-штампами для дипломного проекта.
#
# Алгоритм:
#   1. Все *.puml из uml-sources/ конвертируются в SVG (PlantUML в Docker).
#   2. SVG -> PDF через rsvg-convert / inkscape / cairosvg (любое доступное).
#   3. pdflatex собирает posters/poster_a1.tex   -> posters/build/poster_a1.pdf
#   4. pdflatex собирает posters/stamps_a4.tex   -> posters/build/stamps_a4.pdf
#
# Скриншот UI (report/picture/main_map_interface.png) подгружается напрямую,
# его рекомендуется заранее снять в высоком разрешении (см. README ниже в чате).

set -euo pipefail

SRC_DIR="./uml-sources"
POSTERS_DIR="./posters"
BUILD_DIR="$POSTERS_DIR/build"
SVG_DIR="$BUILD_DIR/svg"
PDF_DIR="$BUILD_DIR/pdf"

mkdir -p "$SVG_DIR" "$PDF_DIR"

#--- 1. PlantUML -> SVG -----------------------------------------------------
echo ">> [1/4] PlantUML -> SVG"
docker run --rm \
    -v "$PWD/$SRC_DIR:/input" \
    -v "$PWD/$SVG_DIR:/output" \
    plantuml/plantuml \
    -tsvg \
    -o "/output" \
    "/input/*.puml"

#--- 2. SVG -> PDF (векторный, без потери качества) -------------------------
echo ">> [2/4] SVG -> PDF"

svg_to_pdf() {
    local svg="$1"
    local pdf="$2"
    if command -v rsvg-convert >/dev/null 2>&1; then
        rsvg-convert -f pdf -o "$pdf" "$svg"
    elif command -v inkscape >/dev/null 2>&1; then
        inkscape "$svg" --export-type=pdf --export-filename="$pdf" >/dev/null
    elif command -v cairosvg >/dev/null 2>&1; then
        cairosvg "$svg" -o "$pdf"
    else
        echo "ERROR: install rsvg-convert (librsvg) or inkscape" >&2
        exit 1
    fi
}

for svg in "$SVG_DIR"/*.svg; do
    name=$(basename "$svg" .svg)
    svg_to_pdf "$svg" "$PDF_DIR/${name}.pdf"
    echo "   ${name}.svg -> ${name}.pdf"
done

#--- 3. Плакаты A1 ----------------------------------------------------------
echo ">> [3/4] LaTeX: poster_a1.pdf"
( cd "$POSTERS_DIR" && \
  xelatex -interaction=nonstopmode -output-directory=build poster_a1.tex >/dev/null )

#--- 4. Лист со штампами A4 -------------------------------------------------
echo ">> [4/4] LaTeX: stamps_a4.pdf"
( cd "$POSTERS_DIR" && \
  xelatex -interaction=nonstopmode -output-directory=build stamps_a4.tex >/dev/null )

echo ""
echo "OK"
echo "  плакаты A1    : $BUILD_DIR/poster_a1.pdf"
echo "  штампы A4     : $BUILD_DIR/stamps_a4.pdf"
