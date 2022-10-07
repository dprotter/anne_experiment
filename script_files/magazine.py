
from RPI_Operant.hardware.box import Box
import time
import random
from pathlib import Path
experiment_name = Path(__file__).stem
RUNTIME_DICT = {'vole':000, 'day':1, 'experiment':experiment_name}
# # For Running on the Raspberry Pi: 
USER_HARDWARE_CONFIG_PATH = '/home/pi/RPI_Operant2/RPI_Operant/default_setup_files/local_hardware.yaml'
USER_SOFTWARE_CONFIG_PATH = '/home/pi/anne_experiment/yaml_setup_files/magazine_software.yaml'


box = Box()

def run():
    
    box.setup(run_dict=RUNTIME_DICT, 
              user_hardware_config_file_path=USER_HARDWARE_CONFIG_PATH,
              user_software_config_file_path=USER_SOFTWARE_CONFIG_PATH,
              start_now=True, simulated = False)
    
    # Ensure doors are closed at start 
    setup_phase = box.timing.new_phase('setup')
    box.doors.door_1.close(wait=True)
    box.doors.door_2.close(wait=True)
    setup_phase.end_phase()

    #simplifying hardware calls
    lever = box.levers.food
    dispenser = box.dispensers.continuous_dispenser_1
    speaker = box.speakers.speaker1

    
    for i in range(1,box.software_config['values']['rounds']+1, 1):
        box.timing.new_round(length = box.software_config['values']['round_length'])
        
        phase = box.timing.new_phase('lever_out', box.software_config['values']['lever_out_time'])
        speaker.play_tone(tone_name = 'round_start')
        press_latency = box.levers.food.extend()
        
        #start the actual lever-out phase
        lever.wait_for_n_presses(n=1, latency_obj = press_latency)
        while phase.active() and not lever.presses_reached:
            '''waiting here for something to happen'''
        
        if lever.presses_reached:
            # if pressed w/in the 2 seconds: Buzz, Retract, Dispense
            speaker.play_tone(tone_name = 'pellet_tone')
            lever.retract()
            dispenser.dispense()  
        
        #wait to the end of the first lever-out phase    
        phase.wait()
        phase.end_phase()
        phase = box.timing.new_phase(name = 'dispense', length = 0)
        
        #only dispense if not already dispensed
        if not lever.presses_reached: # No Press w/in 2 seconds
            print('no lever press')
            # Buzz, Dispense
            speaker.play_tone(tone_name = 'pellet_tone')
            dispenser.dispense()
            time.sleep(2) # 2 second delay before retraction when there is no lever press 
            lever.retract()

        phase.end_phase()
        
        
        phase = box.timing.new_phase(name='ITI', length = box.timing.round_time_remaining())
        box.timing.wait_for_round_finish()
        phase.end_phase()
    
    
    box.shutdown()

if __name__ == '__main__':
    run()
    
