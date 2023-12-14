FROM nvcr.io/nvidia/deepstream:6.3-triton-multiarch

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
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a subdirectory for cloning
RUN mkdir -p /opt/nvidia/deepstream/deepstream-6.3/sources/deepstream_python_apps/apps/DeepstreamYoloPy

# Clone into the subdirectory
RUN git clone https://github.com/AdamAdamczak/DeepstreamYoloPy.git /opt/nvidia/deepstream/deepstream-6.3/sources/deepstream_python_apps/apps/DeepstreamYoloPy && \
    wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1JUHdJwVJkAWcOinGFyDGjanLZBqDEGQ3' -O /opt/nvidia/deepstream/deepstream-6.3/sources/deepstream_python_apps/apps/DeepstreamYoloPy/model/yolov8s-oiv7.onnx

WORKDIR /opt/nvidia/deepstream/deepstream-6.3/sources/deepstream_python_apps/apps/DeepstreamYoloPy
