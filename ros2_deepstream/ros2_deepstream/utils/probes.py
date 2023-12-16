
import pyds
from gi.repository import GLib, Gst

def pgie_src_pad_buffer_probe(pad, info):
    gst_buffer=info.get_buffer()

    batch_meta=pyds.gst_buffer_get_nvds_batch_meta(hash(gst_buffer))
    l_frame=batch_meta.frame_meta_list
    objects=[]
    while l_frame is not None:
        try:
            frame_meta=pyds.NvDsFrameMeta.cast(l_frame.data)
        except StopIteration:
            break

        frame_num=frame_meta.frame_num
        num_obj=frame_meta.num_obj_meta
        l_obj=frame_meta.obj_meta_list
        
        print("Frame Number={} Number of Objects={}".format(frame_num, num_obj))
        
        objects.append(num_obj)
        while l_obj is not None:
            try:
                obj_meta=pyds.NvDsObjectMeta.cast(l_obj.data)
                print('\t Object: {} - Top: {}, Left: {}, Width: {}, Height: {}'.format(obj_meta.obj_label, \
                                                                                        round(obj_meta.rect_params.top), \
                                                                                        round(obj_meta.rect_params.left), \
                                                                                        round(obj_meta.rect_params.width), \
                                                                                        round(obj_meta.rect_params.height)))
            except StopIteration:
                break
            
            try: 
                l_obj=l_obj.next
            except StopIteration:
                break
        
        try:
            l_frame=l_frame.next
        except StopIteration:
            break
    return Gst.PadProbeReturn.OK