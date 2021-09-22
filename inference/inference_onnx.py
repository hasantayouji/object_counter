import numpy as np
import time
from collections import Counter
import cv2
import onnxruntime as ort
from utils.constants import *


IMAGE_PATH = 'tests/cup.jpeg'
ONNX_PATH1 = 'models/efficientdet_d0.onnx'
ONNX_PATH2 = 'models/'

sess1 = ort.InferenceSession(ONNX_PATH1)
#sess2 = ort.InferenceSession(ONNX_PATH2)


def detection(image):
    classname = class_name()
    ori = image.copy()
    image_onnx = np.expand_dims(image, 0)
    detections = sess1.run(["detection_boxes", "detection_scores", "detection_classes"], {'input_tensor': image_onnx})
    boxes = detections[0][0]
    scores = detections[1][0]
    classes = detections[2][0].astype(int)
    cls_det = []
    bbox = []
    cnt = 0
    for i in range(len(boxes)):
        if scores[i] >= score_threshold():
            cnt += 1
            kelas = classes[i]
            box = boxes[i] * np.array([image.shape[0], image.shape[1], image.shape[0], image.shape[1]])
            image = cv2.rectangle(image, (int(box[1]), int(box[0])), (int(box[3]), int(box[2])), (0, 0, 255), 2)
            image = cv2.putText(image, '%s %.2f' % (classname[int(classes[i])], scores[i]),
                                (int(box[1]) - 10, int(box[0]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255))
            cls_det.append(classname[kelas])
            bbox.append(box)
    ctr = Counter(cls_det)
    return image, bbox, ctr


def detection_live(image):
    classname = class_name()
    ori = image.copy()
    image_onnx = np.expand_dims(image, 0)
    detections = sess1.run(["detection_boxes", "detection_scores", "detection_classes"], {'input_tensor': image_onnx})
    boxes = detections[0][0]
    scores = detections[1][0]
    classes = detections[2][0].astype(int)
    cls_det = []
    bbox = []
    cnt = 0
    for i in range(len(boxes)):
        if scores[i] >= score_threshold():
            cnt += 1
            kelas = classes[i]
            box = boxes[i] * np.array([image.shape[0], image.shape[1], image.shape[0], image.shape[1]])
            image = cv2.rectangle(image, (int(box[1]), int(box[0])), (int(box[3]), int(box[2])), (0, 0, 255), 2)
            image = cv2.putText(image, '%s %.2f' % (classname[int(classes[i])], scores[i]),
                                (int(box[1]) - 10, int(box[0]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255))
            cls_det.append(classname[kelas])
            bbox.append(box)
    ctr = Counter(cls_det)
    return image, bbox, ctr


def warmup():
    dummy = cv2.imread(IMAGE_PATH)
    detection(dummy)


def main():
    dummy = cv2.imread(IMAGE_PATH)
    image, __, __ = detection(dummy)
    cv2.imshow('result', image)
    print("-------------------------------------")
    print("PRESS 'ESC' TO PERFORM BENCHMARK TEST WHEN IMAGE APPEARS AND IS IN FOCUS")
    print("-------------------------------------")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    num_samples = 50
    t0 = time.time()
    for _ in range(int(num_samples)):
        t2 = time.time()
        detection(image)
        print('%f [sec]' % (time.time() - t2))
    t1 = time.time()
    print('Average runtime: %f seconds' % (float(t1 - t0) / num_samples))


if __name__ == '__main__':
    main()
