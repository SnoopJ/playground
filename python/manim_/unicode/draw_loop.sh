#!/bin/sh

while inotifywait -e modify $*; do
  python3 -m manim render $*
done
