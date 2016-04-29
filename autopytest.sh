#!/bin/sh

# A simple script that runs py.test every time a python file changes.
#
# Dependencies:
# - inotify-tools
# - pytest

while true; do
  py.test;
  inotifywait -e modify -r pelper/;
done
