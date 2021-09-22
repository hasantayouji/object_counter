import numpy as np

from utils import zmqimage
from utils.constants import *
import threading
from utils.centroidtracker import CentroidTracker
from utils.trackableobject import TrackableObject
import imutils
import dlib
from inference.inference_onnx import detection, detection_live
from ui import main_ui
import cv2

zmq_i = zmqimage.ZmqImageShowServer(open_port="tcp://*:2345")
zmq_o = zmqimage.ZmqConnect(connect_to="tcp://localhost:1234")
cap = cv2.VideoCapture(camera_source())
vid = cv2.VideoCapture(video_source())
total_frame = 0
total_down = 0
W = None
H = None
trackers = []
trackable_objects = {}
ct = CentroidTracker(maxDisappeared=80, maxDistance=100)


class InputThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            in_trigger, img = zmq_i.imreceive()
            cc = ''
            if in_trigger == capture_on():
                print(capture_on())
                img = load_camera(cap)
                img, __, ctr = detection(img)
                for c in ctr:
                    cc = f'{cc}{c}\t: {ctr[c]}\n'
                fmt = {'mode': '1', 'msg': cc}
                cap.release()
                zmq_o.imsend(fmt, img)
            elif in_trigger == capture_continuous():
                print(capture_continuous())
                video = load_camera(vid)
                live_detection(video, detection_interval())
            elif in_trigger == load_image():
                print(load_image())
                img, __, ctr = detection(img)
                for c in ctr:
                    cc = cc + f'{c}\t: {ctr[c]}\n'
                fmt = {'mode': '2', 'msg': cc}
                zmq_o.imsend(fmt, img)


def load_camera(cp):
    if not cp.isOpened():
        cp = cv2.VideoCapture(camera_source())
    ret, frame = cp.read()
    if ret:
        return frame


def live_detection(img, interval):
    global total_frame, H, W, total_down, trackers, ct
    img = imutils.resize(img, width=640)
    if W is None or H is None:
        (H, W) = img.shape[:2]
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rects = []
    if total_frame % interval == 0:
        trackers = []
        img, bbox, ctr = detection_live(img)
        for box in bbox:
            tracker = dlib.correlation_tracker()
            rect = dlib.rectangle(int(box[1]), int(box[0]), int(box[3]), int(box[2]))
            tracker.start_track(rgb, rect)
            trackers.append(tracker)
    else:
        print('MASUK TRACKER 1')
        print(f'PANJANG TRAKCKER - {len(trackers)}')
        for tracker in trackers:
            tracker.update(rgb)
            pos = tracker.get_position()
            start_x = int(pos.left())
            start_y = int(pos.top())
            end_x = int(pos.right())
            end_y = int(pos.bottom())
            rects.append((start_x, start_y, end_x, end_y))

    objects = ct.update(rects)
    for (objectID, centroid) in objects.items():
        to = trackable_objects.get(objectID, None)

        if to is None:
            to = TrackableObject(objectID, centroid)
        else:
            y = [c[1] for c in to.centroids]
            direction = centroid[1] - np.mean(y)
            to.centroids.append(centroid)

            if not to.counted and direction > 0 and centroid[1] > H - 30:
                total_down += 1
                to.counted = True
        trackable_objects[objectID] = to
        cv2.circle(img, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
        cv2.putText(img, f'({centroid[0]}, {centroid[1]})', (centroid[0] - 10, centroid[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)
    total_frame += 1
    print(f'{H} - {W}')
    fmt = {'mode': '3', 'msg': total_down}
    zmq_o.imsend(fmt, img)


def main():
    print('enter program')
    warmup = cv2.imread(img_path())
    __, __, __ = detection_live(warmup)
    print('done warmup')
    th = InputThread()
    th.start()


if __name__ == '__main__':
    main()
    main_ui.main()
