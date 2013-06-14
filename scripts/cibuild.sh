#!/bin/bash

export CJKTOOLS_DATA=$PWD/cjktools-data-master/data

if [ ! -d $CJKTOOLS_DATA ]; then
  wget https://github.com/larsyencken/cjktools-data/archive/master.zip
  unzip master.zip
fi

nosetests
