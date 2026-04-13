#!/bin/bash
cd tex-generator &&
./economics.py > ../report/sections/sec_economics.tex &&
cd ../report &&
latexmk -pdf diploma/diploma_report.tex

SRC_DIR="./uml-sources"
OUT_DIR="./../pictures"


docker run --rm \
  -v "$PWD/$SRC_DIR:/input" \
  -v "$PWD/$OUT_DIR:/output" \
  plantuml/plantuml \
  -tpng \
  -o "/output" \
  "/input/*.puml"

echo "DONE!"
