import threading
import time

import main

k = 0


def timer():
    global k
    time.sleep(300)
    main.main()
    k = 0
    print("Прошло 5 минут")


def checkTimer():
    k += 1
    return 0


def start_submit_thread(event):
    global submit_thread
    submit_thread = threading.Thread(target=timer)
    submit_thread.daemon = True
    submit_thread.start()
    check_submit_thread()


def check_submit_thread():
    while True:
        if submit_thread.is_alive():
            time.sleep(0.2)
            check_submit_thread()
        if stop_threads:
            break
        else:
            print("Timer stopped")


def stop_upload_thread():
    if submit_thread.is_alive():
        global stop_threads
        stop_threads = True
        print("Thread stopped")
    else:
        print("something occured")


start_submit_thread(None)
