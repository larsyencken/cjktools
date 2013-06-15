#!/bin/bash

tarball=cjkdata-2013-06-15-c54b33e.tgz
export CJKDATA=$PWD/cjkdata

if [ ! -d $CJKDATA ]; then
  wget http://files.gakusha.info/$tarball
  tar xfz $tarball
fi

nosetests
