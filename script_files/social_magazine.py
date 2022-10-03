
from RPI_Operant.hardware.box import Box
import time
import random
from pathlib import Path
experiment_name = Path(__file__).stem
RUNTIME_DICT = {'vole':000, 'day':1, 'experiment':experiment_name}
# # For Running on the Raspberry Pi: 
USER_HARDWARE_CONFIG_PATH = '/home/pi/anne_experiment/yaml_setup_files/magazine_hardware.yaml'
USER_SOFTWARE_CONFIG_PATH = '/home/pi/anne_experiment/yaml_setup_files/magazine_software.yaml'


box = Box()

def run():
    
    box.setup(run_dict=RUNTIME_DICT, 
              user_hardware_config_file_path=USER_HARDWARE_CONFIG_PATH,
              user_software_config_file_path=USER_SOFTWARE_CONFIG_PATH,
              start_now=True, simulated = False)


    #simplifying hardware calls
    lever2 = box.levers.door_2
    door = box.doors.door_2 # (TODO) This should get changed to whatever the new Door object that is getting added is called!! 
    speaker = box.speakers.speaker1


    # Ensure doors are closed at start 
    setup_phase = box.timing.new_phase('setup')
    door.close()
    setup_phase.end_phase()

    
    for i in range(1,box.software_config['values']['rounds']+1, 1):
        box.timing.new_round(length = box.software_config['values']['round_length'])
        
        phase = box.timing.new_phase('lever_out', box.software_config['values']['lever_out_time'])
        speaker.play_tone(tone_name = 'round_start')
        press_latency = lever2.extend()
        
        #start the actual lever-out phase
        lever2.wait_for_n_presses(n=1, latency_obj = press_latency)
        while phase.active() and not lever2.presses_reached:
            '''waiting here for something to happen'''
        
        #immediately end the lever-out phase 
        lever2.retract()   
        phase.end_phase()

        if lever2.presses_reached:
            # if pressed w/in the 5 seconds: Tone/Open Door, Wait for Reward Time, Tone/Close Door 

            # Open Door 
            speaker.play_tone(tone_name = 'door_open')
            door.open()

            # Reward Time 
            phase = box.timing.new_phase(name = 'reward time', length = box.software_config['values']['reward_time'])
            phase.wait() # doors will remain open for 30 seconds 
            phase.end_phase()

            # Tone and Close Door 
            speaker.play_tone(tone_name = 'door_close')
            door.close()
        
        else: # No Press w/in 2 seconds. Go straight to ITI
            print('no lever press')
        

        # ITI Time
        phase = box.timing.new_phase(name='ITI', length = box.software_config['values']['ITI'])
        phase.wait() # ITI 30 seconds
        phase.end_phase()
    
    
    box.shutdown()

if __name__ == '__main__':
    run()
    
