#!/bin/bash
#
# buildDeb.sh
#
# A script to rebuild a new debian/ubuntu package for jptools, discarding
# any earlier ones.

set -x

rm -rf *.deb MANIFEST build dist
python setup.py bdist_rpm
(
    cd dist
    fakeroot alien -d jptools*noarch*.rpm
)
mv dist/*.deb ./
