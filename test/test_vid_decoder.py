import os
import sys
import cv2

sys.path.append('.')
from vid_decoder_py.vid_decoder import VidDecoder

def run():
    # Initialize the decoder.
    camera_info = {
        'vid_type': 'Jingyang', # Dahua / Jingyang
        'usr': 'admin',
        'pwd': 'admin',
        'ip': '192.168.1.2',
        'channel': 1
    }
    # Start to decode
    frame_save_dir = "./test/frames"
    # frame_save_dir = "/data1/geng.wu/16CengImg/"
    decoder = VidDecoder(camera_info)
    print(type(decoder))
    for fps, count, frame in decoder:
        # 每1000帧执行一次
        if count % 1000 == 0:
            print("INFO: Video FPS is {}".format(fps))
            fname = "{}_{}.jpg".format(count, fps)
            full_path = os.path.join(frame_save_dir, fname)
            print(full_path)
            cv2.imwrite(full_path, frame)
    decoder.release()

if __name__ == '__main__':
    run()
