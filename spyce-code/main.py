import threading
from controller import Controller  # Assuming your Controller class is saved in a file named controller.py
import time

def run_uss_with_timeout(controller, timeout=600):  # 10 minutes timeout
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        motion_detected = controller.run_uss()
        if motion_detected:
            controller.run_media()
            break
        time.sleep(1)  # Check every second

def run_pir_and_uss_in_parallel(controller):
    def run_uss_and_media_on_motion():
        while True:
            motion_detected = controller.run_uss()
            if motion_detected:
                controller.run_media()
                break
            time.sleep(1)  # Check every second

    # Start run_uss in a separate thread
    uss_thread = threading.Thread(target=run_uss_and_media_on_motion)
    uss_thread.start()
    # Run run_pir in the main thread or another thread as needed
    # Assuming run_pir is designed to continuously monitor and write to CSV
    controller.run_pir()  
    uss_thread.join()

def main(usv_pir_com):
    controller = Controller()  # Initialize your controller
    try:
        if usv_pir_com:
            # PIR sensors should run first
            motion_detected = controller.run_pir()
            if motion_detected:
                # If motion is detected by PIR, run USS for 10 minutes or until motion is detected
                run_uss_with_timeout(controller)
            else:
                print("No motion detected by PIR.")
        else:
            # Both run_pir() and run_uss() should run independently and in parallel
            run_pir_and_uss_in_parallel(controller)
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    # finally:
    #     # This is a good place to ensure all resources are cleaned up properly,
    #     # especially if your controller class opens any resources that need to be closed
    #     controller.close()  

if __name__ == "__main__":
    usv_pir_com = True  # or False, depending on your needs
    main(usv_pir_com)
