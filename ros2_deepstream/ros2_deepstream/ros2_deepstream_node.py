#!/usr/bin/env python3

# Copyright 2023 AdamAdamczak
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node
try:
    from ros2_deepstream.ros2_deepstream import Ros2Deepstream
except ImportError:
    from ros2_deepstream import Ros2Deepstream


class Ros2DeepstreamNode(Node):

    def __init__(self):
        super().__init__('ros2_deepstream_node')
        self.ros2_deepstream = Ros2Deepstream(target_video_path='/opt/nvidia/deepstream/deepstream-6.3/samples/streams/sample_720p.h264',
                                              output_video_path='output.mp4',
                                              config_path='/root/ros2_ws/src/DeepstreamYoloPy/ros2_deepstream/config/config_infer_primary_yoloV8.txt')

    def start_processing(self):
        self.ros2_deepstream.run_loop()

def main(args=None):
    rclpy.init(args=args)
    node = Ros2DeepstreamNode()
    try:
        node.start_processing()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
