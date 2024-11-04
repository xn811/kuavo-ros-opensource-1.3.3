#!/bin/bash

echo "Checking for required dependencies..."
sudo apt-get update -q && DEBIAN_FRONTEND=noninteractive sudo apt-get install -y \
    curl \
    git \
    libgl1-mesa-dev \
    libgl1-mesa-glx \
    libglew-dev \
    libosmesa6-dev \
    software-properties-common \
    net-tools \
    vim \
    virtualenv \
    wget \
    xpra \
    xserver-xorg-dev \
    libglfw3-dev \
    liburdfdom-dev \
    liboctomap-dev \
    libassimp-dev \
    ros-noetic-rqt-multiplot \
    ros-noetic-grid-map-rviz-plugin \
    ros-noetic-realtime-tools \
    build-essential \
    libglib2.0-dev \
    ros-noetic-controller-interface

echo "Checking for MuJoCo..."
if [ ! -d "~/.mujoco/mujoco210" ]; then
    echo "Installing MuJoCo..."
    mkdir -p ~/.mujoco \
        && wget https://mujoco.org/download/mujoco210-linux-x86_64.tar.gz -O mujoco.tar.gz \
        && tar -xf mujoco.tar.gz -C ~/.mujoco \
        && rm mujoco.tar.gz \
        && echo 'export LD_LIBRARY_PATH=~/.mujoco/mujoco210/bin:$LD_LIBRARY_PATH' >> ~/.bashrc \
        && echo 'export PATH=$LD_LIBRARY_PATH:$PATH' >> ~/.bashrc \
        && echo 'export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so' >> ~/.bashrc \
        && echo 'export LD_LIBRARY_PATH=~/.mujoco/mujoco210/bin:$LD_LIBRARY_PATH' >> ~/.zshrc \
        && echo 'export PATH=$LD_LIBRARY_PATH:$PATH' >> ~/.zshrc \
        && echo 'export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so' >> ~/.zshrc
else
    echo "MuJoCo is already installed."
fi

# 安装 mujoco-py
echo "Installing mujoco-py..."
if ! pip3 show mujoco-py &> /dev/null; then
    [ -d "/tmp/mujoco-py" ] && rm -rf /tmp/mujoco-py
    git clone https://github.com/openai/mujoco-py.git /tmp/mujoco-py \
        && cd /tmp/mujoco-py/ \
        && pip3 install -U 'mujoco-py<2.2,>=2.1' \
        && pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
        && pip3 install -r requirements.dev.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
        && python3 setup.py install \
        && pip3 install mujoco \
        && pip3 install pynput \
        && cd .. && rm -rf mujoco-py
else
    echo "mujoco-py is already installed."
fi

if ! ls /usr/local/lib | grep hpp-fcl; then
    echo "Installing hpp-fcl..."
    [ -d "/tmp/hpp-fcl" ] && sudo rm -rf /tmp/hpp-fcl
    git clone --recurse-submodules https://github.com/leggedrobotics/hpp-fcl.git /tmp/hpp-fcl \
        && cd /tmp/hpp-fcl \
        && mkdir build && cd build \
        && cmake .. \
        && make -j$(nproc) \
        && sudo make install \
        && cd ../.. 
else
    echo "hpp-fcl is already installed."
fi

if ! ls /usr/local/lib | grep pinocchio; then
    echo "Installing pinocchio..."
    [ -d "/tmp/pinocchio" ] && sudo rm -rf /tmp/pinocchio
    git clone --recurse-submodules https://github.com/leggedrobotics/pinocchio.git /tmp/pinocchio \
        && cd /tmp/pinocchio \
        && mkdir build && cd build \
        && cmake .. \
        && make -j$(nproc) \
        && sudo make install \
        && cd ../.. 
else
    echo "pinocchio is already installed."
fi

if ! ls /usr/local/lib | grep lcm; then
    echo "Installing lcm..."
    [ -d "/tmp/lcm" ] && sudo rm -rf /tmp/lcm
    git clone https://github.com/lcm-proj/lcm.git /tmp/lcm \
        && cd /tmp/lcm \
        && mkdir build && cd build \
        && cmake .. \
        && make -j$(nproc) \
        && sudo make install \
        && cd ../.. \
        && rm -f /usr/local/lib/liblcm.so \
        && ln -s /usr/lib/x86_64-linux-gnu/liblcm.so /usr/local/lib/liblcm.so
else
    echo "lcm is already installed."
fi