import sys
sys.path.append('../')
import os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GLib, Gst
from common.is_aarch_64 import is_aarch64
from common.bus_call import bus_call
import pyds
from utils.probes import pgie_src_pad_buffer_probe
from common.bus_call import bus_call
from inspect import getsource


config_path = "configs/config_infer_primary_yoloV8.txt"
output_video_path = os.environ.get('OUTPUT_PATH',"output/output.mp4")
target_video_path = os.environ.get('INPUT_PATH',"../../../../samples/streams/sample_720p.h264")

Gst.init(None)

pipeline=Gst.Pipeline()
print('Created pipeline')

source=Gst.ElementFactory.make("filesrc", "file-source")
source.set_property('location', target_video_path)

h264parser=Gst.ElementFactory.make("h264parse", "h264-parser")
decoder=Gst.ElementFactory.make("nvv4l2decoder", "nvv4l2-decoder")

streammux=Gst.ElementFactory.make("nvstreammux", "stream-muxer")
streammux.set_property('width', 960) 
streammux.set_property('height', 540) 
streammux.set_property('batch-size', 1)

pgie=Gst.ElementFactory.make("nvinfer", "primary-inference")
pgie.set_property('config-file-path', config_path)

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
filesink.set_property('location', output_video_path)
filesink.set_property("sync", 1)
print('Created elements')

pipeline.add(source)
pipeline.add(h264parser)
pipeline.add(decoder)
pipeline.add(streammux)
pipeline.add(pgie)
pipeline.add(nvvidconv1)
pipeline.add(nvosd)
pipeline.add(nvvidconv2)
pipeline.add(capsfilter)
pipeline.add(encoder)
pipeline.add(mux)

pipeline.add(filesink)
print('Added elements to pipeline')



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

print('Linked elements in pipeline')


pgie_src_pad=pgie.get_static_pad('src')
probe_id=pgie_src_pad.add_probe(Gst.PadProbeType.BUFFER, pgie_src_pad_buffer_probe)
print('Attached probe')

print(getsource(bus_call))

loop=GLib.MainLoop()


bus=pipeline.get_bus()
bus.add_signal_watch()
bus.connect("message", bus_call, loop)
print('Added bus message handler')
print("Starting pipeline")
pipeline.set_state(Gst.State.PLAYING)
try:
    loop.run()
except:
    pass
pipeline.set_state(Gst.State.NULL)