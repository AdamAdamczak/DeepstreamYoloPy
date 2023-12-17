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
import sys
sys.path.append('/opt/nvidia/deepstream/deepstream-6.3/sources/deepstream_python_apps/apps/')
import os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GLib, Gst
from common.is_aarch_64 import is_aarch64
from common.bus_call import bus_call
import pyds
from ros2_deepstream.utils.probes import pgie_src_pad_buffer_probe
from common.bus_call import bus_call
from inspect import getsource

class Ros2Deepstream:

    def __init__(self,target_video_path,output_video_path,config_path):
        self.target_video_path=target_video_path
        self.output_video_path=output_video_path
        self.config_path=config_path
        self.init_pipeline()
        self.loop=None
        

    def init_pipeline(self):
        Gst.init(None)
        self.pipeline=Gst.Pipeline()
        print('Created self.pipeline')

        source=Gst.ElementFactory.make("filesrc", "file-source")
        source.set_property('location', self.target_video_path)

        h264parser=Gst.ElementFactory.make("h264parse", "h264-parser")
        decoder=Gst.ElementFactory.make("nvv4l2decoder", "nvv4l2-decoder")

        streammux=Gst.ElementFactory.make("nvstreammux", "stream-muxer")
        streammux.set_property('width', 960) 
        streammux.set_property('height', 540) 
        streammux.set_property('batch-size', 1)

        pgie=Gst.ElementFactory.make("nvinfer", "primary-inference")
        pgie.set_property('config-file-path', self.config_path)

        nvvidconv1=Gst.ElementFactory.make("nvvideoconvert", "convertor1")
        nvosd=Gst.ElementFactory.make("nvdsosd", "onscreendisplay")
        nvvidconv2=Gst.ElementFactory.make("nvvideoconvert", "convertor2")

        capsfilter=Gst.ElementFactory.make("capsfilter", "capsfilter")
        caps=Gst.Caps.from_string("video/x-raw, format=I420")
        capsfilter.set_property("caps", caps)

        encoder = Gst.ElementFactory.make("avenc_mpeg4", "encoder")
        encoder.set_property("bitrate", 4000000)

        mux = Gst.ElementFactory.make("mp4mux", "mux")

        filesink=Gst.ElementFactory.make('filesink', 'filesink')
        filesink.set_property('location', self.output_video_path)
        filesink.set_property("sync", 1)
        print('Created elements')

        self.pipeline.add(source)
        self.pipeline.add(h264parser)
        self.pipeline.add(decoder)
        self.pipeline.add(streammux)
        self.pipeline.add(pgie)
        self.pipeline.add(nvvidconv1)
        self.pipeline.add(nvosd)
        self.pipeline.add(nvvidconv2)
        self.pipeline.add(capsfilter)
        self.pipeline.add(encoder)
        self.pipeline.add(mux)

        self.pipeline.add(filesink)
        print('Added elements to self.pipeline')



        source.link(h264parser)
        h264parser.link(decoder)

        decoder_srcpad=decoder.get_static_pad("src")    
        streammux_sinkpad=streammux.get_request_pad("sink_0")

        decoder_srcpad.link(streammux_sinkpad)
        streammux.link(pgie)
        pgie.link(nvvidconv1)
        nvvidconv1.link(nvosd)
        nvosd.link(nvvidconv2)
        nvvidconv2.link(capsfilter)
        capsfilter.link(encoder)
        encoder.link(mux)
        mux.link(filesink)

        print('Linked elements in self.pipeline')


        pgie_src_pad=pgie.get_static_pad('src')
        probe_id=pgie_src_pad.add_probe(Gst.PadProbeType.BUFFER, pgie_src_pad_buffer_probe)
        print('Attached probe')

        print(getsource(bus_call))

        self.loop=GLib.MainLoop()


        bus=self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", bus_call, self.loop)
        print('Added bus message handler')
        print("Starting self.pipeline")
        self.pipeline.set_state(Gst.State.PLAYING)

    def run_loop(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        try:
            self.loop.run()
        except:
            pass
        self.pipeline.set_state(Gst.State.NULL)