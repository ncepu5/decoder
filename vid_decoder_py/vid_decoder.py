import cv2

class VidDecoder(object):
    """
    Video Decoder.
    The input video stream can be from a file, a usb camber or a web camber under rstp.
    """

    def __init__(self, caminfo):
        """
        Create the video capture.
        Arg(s):
          caminfo: the basic inforamtion of the camera to set the video stream path.
        """
        self._offline_flag = False
        vid_type = caminfo['vid_type']
        usr = caminfo['usr']
        pwd = caminfo['pwd']
        ip = caminfo['ip']
        channel = caminfo['channel']
        # Set the rstp path for different cameras.
        if  vid_type == 'Hikvision':
            # Now only for the new version.
            # rtsp://admin:12345@172.18.33.29:554/h264/ch1/main/av_stream
            vid_stream_path = \
                "rtsp://%s:%s@%s//Streaming/Channels/%d" % (usr, pwd, ip, channel)
        elif vid_type == 'Dahua':
            vid_stream_path = \
                "rtsp://%s:%s@%s/cam/realmonitor?channel=%d&subtype=0" % (usr, pwd, ip, channel)
        elif vid_type == 'Jingyang':
            vid_stream_path = \
                "rtsp://%s:%s@%s:554/snl/live/%d/1" % (usr, pwd, ip, channel) # sunell
        elif vid_type == 'Tiandy':
            # "rtsp://admin:1111@172.18.33.29/1/1"
            vid_stream_path = \
                "rtsp://%s:%s@%s/%d/1" % (usr, pwd, ip, channel)
        elif vid_type == 0:
            # Load local usb camera.
            vid_stream_path = 0
        elif vid_type.find('.'):
            # Load offline video file.
            self._offline_flag = True
            vid_stream_path = vid_type
        else:
            raise Exception("Bad video type", vid_type)
        # Create video capture.
        self._vid_cap = cv2.VideoCapture(vid_stream_path)
        if not self._vid_cap.isOpened():
            raise Exception("Open video FAILED")
        self._count = 0
        # Video header information
        self._fps = int(round(self._vid_cap.get(cv2.CAP_PROP_FPS)))
        if self._offline_flag:
            self._vid_counts = int(self._vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def __iter__(self):
        self._count = -1
        return self

    def __next__(self):
        """
        Decode the video stream frame by frame.
        Arg(s):
        Return:
          fps: number of frames per second.
          count: number of frames have been decoded.
          frame: decoded video frame.
        """
        self._count += 1
        if self._offline_flag:
            if self._count == self._vid_counts:
                raise StopIteration
        vid_cap = self._vid_cap
        # Read image
        if vid_cap.isOpened():
            ret, frame = vid_cap.read()
            if frame is None:
                raise Warning('Failed to decode frame {:d}'.format(self._count))
        else:
            raise StopIteration
        return self._fps, self._count, frame

    def release(self):
        """
        Release the video capture.
        """
        if self._vid_cap.isOpened():
            self._vid_cap.release()
