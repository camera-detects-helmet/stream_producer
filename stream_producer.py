import cv2 as cv
import subprocess as sp
from threading import Thread
import argparse
import os



class StreamingVideo:
    
    def __init__(self,src=0,path=''):
        self.cap = cv.VideoCapture(src)
        self.sizeStr = str(int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))) + 'x' + str(int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
        self.fps = int(self.cap.get(cv.CAP_PROP_FPS))
        self.rtsp_server = os.environ.get('RTSP_ADDRESS') + path
        self.command = ['ffmpeg',
                    '-re',
                    '-s', self.sizeStr,
                    '-r', str(self.fps),  # rtsp fps (from input server)
                    '-i', '-',
                    # You can change ffmpeg parameter after this item.
                    '-pix_fmt', 'yuv420p',
                    '-r', '25',  # output fps
                    '-g', '50',
                    '-c:v', 'libx264',
                    '-b:v', '2M',
                    '-bufsize', '64M',
                    '-maxrate', "4M",
                    '-preset', 'veryfast',
                    '-rtsp_transport', 'tcp',
                    '-segment_times', '5',
                    '-f', 'rtsp',
                    self.rtsp_server]
        self.process = sp.Popen(self.command, stdin=sp.PIPE)
        self.thread = Thread(target=self.run)
        self.thread.start()

    def run(self):
        while True:
            ret, frame = self.cap.read()
            ret2, frame2 = cv.imencode('.png', frame)
            self.process.stdin.write(frame2.tobytes())
            
    def stop(self):
        self.process.terminate()
        self.cap.release()
        cv.destroyAllWindows()
        print("Video Stopped")
    
    def __del__(self):
        self.stop()


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', type=int, default=0, help='Video Source')
    parser.add_argument('--path', type=str, default='', help='Video Path')
    args = parser.parse_args()
    return args


def main():
    
    if os.environ.get('RTSP_ADDRESS') is None:
        print("❗️Please set RTSP_ADDRESS => export RTSP_ADDRESS=<address>")
        exit()
        
    if parse_opt().path == '':
        print("❗️Please set path => --path <path>")
        exit()
    
    if os.environ.get('RTSP_ADDRESS')[-1] != '/':
        print("❗️Please set RTSP_ADDRESS with '/' at the end => export RTSP_ADDRESS=<address>/")
        exit()
    
    StreamingVideo(**vars(parse_opt()))

if __name__ == "__main__":
    main()
    
