def ui_path():
    return 'ui/mainwindow.ui'


def ui_script():
    return '../guis/script/main_ui.py'


def program_script():
    return 'inferences/data_processing.py'


def live_model_path():
    return 'models/if3/frozen_inference_graph.pb'


def model_path():
    return 'models/centernet_hg104_512x512_kpts_coco17_tpu-32/saved_model'


def capture_on():
    return '1'


def capture_off():
    return '0'


def load_image():
    return '2'


def img_path():
    return 'tests/cup.jpeg'


def video_path():
    #return 'data/forging.mp4'
    return 'data/MAH03775.MP4'


def capture_continuous():
    return '3'


def score_threshold():
    return 0.3


def camera_source():
    return 0


def video_source():
    #return 'data/forging.mp4'
    #return 'data/MAH03775.MP4'
    return 'data/for2.mp4'


def detection_interval():
    return 50


def class_name():
    return ["BG", "Orang", "Sepeda", "Mobil", "Motor", "Pesawat", "Bis", "Kereta", "Truk", "Perahu",
                  "Lampu Merah", "Hydrant", "Rambu",    "Tanda Stop", "Parkir Meter", "Tempat Duduk", "Burung",
                  "Kucing", "Anjing", "Kuda", "Domba", "Sapi", "Gajah", "Beruang", "Zebra", "Jerapah", "Topi",
                  "Tas Ransel", "Payung", "Sepatu", "Kaca Mata", "Tas Jinjing", "Dasi", "Koper", "Frisbee", "Ski",
                  "Snowboard", "Bola", "Layangan", "Bat Baseball", "Sarung Tangan Baseball", "Skateboard",
                  "Papan Selancar", "Raket Tenis", "Botol", "Piring", "Gelas Wine", "Cangkir", "Garpu", "Pisau",
                  "Sendok", "Mangkok", "Pisang", "Apel", "Sandwich", "Jeruk", "Brokoli", "Wortel", "Hot Dog", "Pizza",
                  "Donat", "Kue", "Kursi", "Sofa", "Tanaman Pot", "Kasur", "Cermin", "Meja Makan", "Jendela",
                  "Meja Kerja", "Toilet", "Pintu", "TV", "Laptop", "Mouse", "Remot", "Keyboard", "Hape", "Microwave",
                  "Oven", "Toaster", "Sink", "Kulkas", "Blender", "Buku", "Jam", "Vas", "Gunting", "Teddy Bear",
                  "Hair Dryer", "Sikat Gigi"]


def live_class():
    return ['BG', 'Part']
