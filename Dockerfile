FROM nvcr.io/nvidia/deepstream:6.3-triton-multiarch
ENV DEBIAN_FRONTEND=noninteractive  
WORKDIR /opt/nvidia/deepstream/deepstream-6.3
LABEL maintainer="Adam Adamczak - adamadamczak123@gmail.com"
LABEL version="1.0"
RUN apt-get update && \
    apt-get install -y wget && \
    chmod +x ./install.sh && \
    chmod +x ./user_additional_install.sh && \
    chmod +x ./user_deepstream_python_apps_install.sh && \
    ./install.sh && \
    ./user_additional_install.sh && \
    ./user_deepstream_python_apps_install.sh --version 1.1.4 && \
    python -m pip install --upgrade pip && \
    apt-get clean 

RUN apt-get update -y && \
    apt install locales && \
    locale-gen en_US en_US.UTF-8 && \
    update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 && \
    export LANG=en_US.UTF-8

RUN apt install -y software-properties-common && \
    add-apt-repository universe -y && \
    apt update  -y && \
    apt install curl -y 
    
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

RUN apt update -y && \
    apt upgrade -y && \
    apt install ros-foxy-desktop python3-argcomplete -y && \
    apt install python3-colcon-common-extensions -y && \ 
    apt install ros-foxy-vision-msgs -y && \
    apt-get install ros-foxy-ament-cmake-auto && \ 
    rm -rf /var/lib/apt/lists/*


# Create a subdirectory for cloning     
RUN mkdir -p /opt/nvidia/deepstream/deepstream-6.3/sources/deepstream_python_apps/apps/DeepstreamYoloPy

# Clone into the subdirectory
RUN git clone https://github.com/AdamAdamczak/DeepstreamYoloPy.git /opt/nvidia/deepstream/deepstream-6.3/sources/deepstream_python_apps/apps/DeepstreamYoloPy && \
    wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1JUHdJwVJkAWcOinGFyDGjanLZBqDEGQ3' -O /opt/nvidia/deepstream/deepstream-6.3/sources/deepstream_python_apps/apps/DeepstreamYoloPy/model/yolov8s-oiv7.onnx
 

WORKDIR /opt/nvidia/deepstream/deepstream-6.3/sources/deepstream_python_apps/apps/DeepstreamYoloPy
