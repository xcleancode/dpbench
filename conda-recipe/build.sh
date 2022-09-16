#!/bin/bash

CC=icx CXX=icpx ${PYTHON} setup.py install -- -Dpybind11_DIR=$(${PYTHON} -m pybind11 --cmakedir) -DDPCTL_MODULE_PATH=$(${PYTHON} -m dpctl --cmakedir)
