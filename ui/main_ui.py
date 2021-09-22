import sys

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5.QtGui import *

import cv2
from utils import zmqimage
from utils.constants import *

zmq_i = zmqimage.ZmqImageShowServer(open_port="tcp://*:1234")
zmq_o = zmqimage.ZmqConnect(connect_to="tcp://localhost:2345")


def create_qimage(pic):
    pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
    qformat = QImage.Format_Indexed8
    if len(pic.shape) == 3:
        qformat = QImage.Format_RGBA8888 if pic.shape[2] == 4 else QImage.Format_RGB888
    pic = QImage(pic, pic.shape[1], pic.shape[0], pic.strides[0], qformat)
    return pic


class Thread(QThread):
    img_r = pyqtSignal(QImage)
    stat_r = pyqtSignal(dict)

    def run(self):
        while True:
            res, img = zmq_i.imreceive()
            img = create_qimage(img)
            pic = img.scaled(640, 512)
            self.img_r.emit(pic)
            self.stat_r.emit(res)


class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        loadUi(ui_path(), self)
        self.conf = capture_off()
        self.img = cv2.imread(img_path())

        # initialize button
        self.b_load.clicked.connect(self.btn_openfile)
        self.b_takepicture.clicked.connect(self.btn_capture)
        self.b_live.clicked.connect(self.btn_live)
        self.mthread()

    def mthread(self):
        mt = Thread(parent=self)
        mt.img_r.connect(self.set_image)
        mt.stat_r.connect(self.set_counter)
        mt.start()

    def set_counter(self, counter):
        if counter['mode'] in ['1', '2']:
            self.l_count.setText(counter['msg'])
            self.d_counter.display(999)
        elif counter['mode'] == '3':
            self.l_count.setText('')
            self.d_counter.display(counter['msg'])
            self.b_live.setStyleSheet('background: green')

    def set_image(self, img):
        self.l_camera.setPixmap(QPixmap(img))
        self.l_camera.setScaledContents(True)
        zmq_o.imsend(self.conf, self.img)

    def btn_capture(self):
        self.conf = capture_on()
        zmq_o.imsend(self.conf, self.img)
        self.conf = capture_off()

    def btn_live(self):
        self.conf = capture_continuous()
        zmq_o.imsend(self.conf, self.img)

    def btn_openfile(self):
        self.conf = load_image()
        fname = QFileDialog.getOpenFileName(self, 'Open File', filter='Image files (*.jpg *.png *.jpeg *.webp)')
        if fname[0] != '':
            file = fname[0]
            img = cv2.imread(file)
            zmq_o.imsend(self.conf, img)
        self.conf = capture_off()


def main():
    app = QApplication(sys.argv)
    window = MainUI()
    window.setWindowTitle('Counter Application Demo')
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
