#!/bin/bash
# Enhance the local Python repository to add stubs for classes
# that are not included in the MacOSX distribution of boosteros.
#
REPO=/Library/Frameworks/Python.framework/Versions/3.14/lib/python3.14/site-packages/boosteros/types
LIB=${CHARLIE_HOME}/lib
mkdir -p ${REPO}
cp ${LIB}/*.pyi ${REPO}
