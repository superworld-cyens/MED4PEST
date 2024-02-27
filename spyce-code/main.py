import threading
from controller import Controller  # Assuming your Controller class is saved in a file named controller.py
import time

def run_uss_with_timeout(controller, timeout=300):  # 5 minutes timeout
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} USS monitoring started! Waiting for rodents to enter the stage.')
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} Rodent not entering stage. USS monitoring will stop in {(timeout - (time.time() - start_time))//60} min')

        motion_detected = controller.run_uss()
        if motion_detected:
            print(motion_detected)
            print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} Rodent entered the stage! Recording picture and audio. CHEESE!!!')
            controller.run_media()
            # break
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

def main():
    controller = Controller()  # Initialize your controller
    configuration = controller.config

    print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} User choose MODE {configuration["settings"]["mode"]}')
    try:
        if configuration["settings"]["mode"]==0:
            # PIR sensors should run first
            print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} PIR initialized and waiting to detection motion.')
            motion_detected = controller.run_pir()
            if motion_detected:
                # If motion is detected by PIR, run USS for 10 minutes or until motion is detected
                print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} Rodent entered pipe. USS initialized and waiting to detection motion.')
                run_uss_with_timeout(controller)
            else:
                print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} Waiting for Rodents.')
        elif configuration["settings"]["mode"]==1:
            # Both run_pir() and run_uss() should run independently and in parallel
            run_pir_and_uss_in_parallel(controller)
        else:
            print("Select correct mode!!!!")
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        # This is a good place to ensure all resources are cleaned up properly,
        # especially if your controller class opens any resources that need to be closed
        # controller.close()  
        pass

if __name__ == "__main__":  

    while 1:
        main()
