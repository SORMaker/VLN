# VLN: Vision-and-Language Navigation


## Overview
This repository contains the codebase for [VLN Tutorial](https://github.com/MuzK01/VLN-Tutorial)

## Contents
- Matterport3D Simulator Tutorial
- Seq2Seq
- MapGPT

## Matterport3D
we don't use docker to install the Matterport3D Simulator, but if you want to learn more about Matterport3D Simulator, you can check [Matterport3DSimulator](Matterport3DSimulator) and this is tailored from [Matterport3DSimulator](https://github.com/peteanderson80/Matterport3DSimulator)

## install Simulator
### Create Conda Environment
Set up a Conda environment for the simulator
```bash
conda create --name vln python=3.10
conda activate vln
pip install -r requirements.txt
```

### Download Dependencies 
```bash
sudo apt-get install -y wget doxygen curl libjsoncpp-dev libepoxy-dev libglm-dev libosmesa6 libosmesa6-dev libglew-dev python3-setuptools cmake libopencv-dev python3-opencv libegl1-mesa-dev
```

### Building
Ensure that you are in a conda environment(python=3.10)
```bash
conda activate vln
cd Matterport3DSimulator
```
build the simulator
```bash
mkdir build && cd build
cmake -DEGL_RENDERING=ON ..
make
cd ../
```
The main requirements are:
- Ubuntu >= 14.04
- Nvidia-driver with CUDA installed
- C++ compiler with C++11 support
- [CMake](https://cmake.org/) >= 3.10
- [OpenCV](https://opencv.org/)
- [OpenGL](https://www.opengl.org/)
- [GLM](https://glm.g-truc.net/0.9.8/index.html)
- [Numpy](https://numpy.org/)
### Set environment
```bash
vim ~/.bashrc
export PYTHONPATH=/your/path/to/Matterport3DSimulator/build
source ~/.bashrc
echo $PYTHONPATH
```
### Test
```bash
python
import MatterSim
```
### Question
you may meet this error
```bash
ImportError: /lib/x86_64-linux-gnu/libp11-kit.so.0: undefined symbol: ffi_type_pointer, version LIBFFI_BASE_7.0
```
The reason is the version of libffi is not correct.
To solute this problem, you should change the soft-link of `libffi.so.7` and you can check this [link](https://blog.csdn.net/qq_38606680/article/details/129118491) to learn more 
```bash
cd /home/your_conda/envs/vln/lib
rm libffi.so.7
sudo ln -s /lib/x86_64-linux-gnu/libffi.so.7.1.0 libffi.so.7
sudo ldconfig
```
Retest the MatterSim
```bash
python
import MatterSim
```
## Seq2Seq
todo
## MapGPT
todo