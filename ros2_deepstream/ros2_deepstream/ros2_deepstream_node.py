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
        self.ros2_deepstream = Ros2Deepstream()
        self.param_name = self.declare_parameter('param_name', 456).value
        self.ros2_deepstream.foo(self.param_name)


def main(args=None):
    rclpy.init(args=args)
    node = Ros2DeepstreamNode()
    try:
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
