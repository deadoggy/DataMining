#!/bin/bash

if [ -f "result" ]; then
  rm result
fi

touch result
python Hash.py > result
