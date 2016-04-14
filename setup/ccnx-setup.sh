#!/bin/bash


git clone https://github.com/PARC/CCNx_Distillery
sudo apt-get install cmake
# errors with this command
cd CCNx_Distillery
make update
make all


