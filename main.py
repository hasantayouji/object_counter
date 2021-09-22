import time
import threading


def run_ui():
    from ui.main_ui import main
    main()


def run_program():
    from inference.dataprocessing import main
    main()


class UIThread(threading.Thread):
    def run(self):
        from ui.main_ui import main
        main()


class ProgramThread(threading.Thread):
    def run(self):
        from inference.dataprocessing import main
        main()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uit = UIThread()
    prt = ProgramThread()
    uit.start()
    time.sleep(1)
    prt.start()
