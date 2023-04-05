#!/bin/bash

function run_manim {
    python3 -m manim render $*
}

run_manim $*

while inotifywait -e modify *; do
  run_manim $*
done
