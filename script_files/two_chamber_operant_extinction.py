'''
    Experiment (3/4): Door Shape Contingent

'''
from RPI_Operant.hardware.box import Box
import time
import random
from pathlib import Path
experiment_name = Path(__file__).stem
RUNTIME_DICT = {'vole':000, 'day':1, 'experiment':experiment_name}

# # For Running on the Raspberry Pi: 
USER_HARDWARE_CONFIG_PATH = '/home/pi/RPI_Operant2/RPI_Operant/default_setup_files/local_hardware.yaml'
USER_SOFTWARE_CONFIG_PATH = '/home/pi/anne_experiment/yaml_setup_files/two_chamber_operant_software.yaml'


box = Box()
def run():

    
    #
    # Call to Setup Box with Hardware/Software yaml files specified! 
    #
    box.setup(run_dict=RUNTIME_DICT, 
              user_hardware_config_file_path=USER_HARDWARE_CONFIG_PATH,
              user_software_config_file_path=USER_SOFTWARE_CONFIG_PATH,
              start_now=True, 
              simulated=False)

    box.reset()
    #simplifying hardware calls
    lever2 = box.levers.door_2
    door = box.doors.door_1 
    beam = box.beams.door1_ir
    speaker = box.speakers.speaker1

    progressive_ratio = box.software_config['values']['progressive_ratio']
    presses_required = 1 if not 'start_at_press' in box.run_dict else box.run_dict['start_at_press']

    experiment_length_phase = box.timing.new_phase(f'maximum_experiment_length', length = box.software_config['values']['maximum_experiment_length'])
    
    round_number=1
    print(f'ROUND {round_number}')
    box.timing.new_round()
    box.speakers.speaker1.play_tone('round_start', wait = True) # Round Start Tone 
    press_latency_2 = lever2.extend()
    
    #lets hope they cant get to 10000 presses
    lever2.wait_for_n_presses(n = 10000, latency_obj = press_latency_2, inter_press_retraction = True)

    while experiment_length_phase.active():
        
        # if they press w/in the roundtime: 
        # monitor for beam break
        while not lever2.presses_reached and experiment_length_phase.active():
            '''waiting here for something to happen'''
            time.sleep(0.05)
        


        
    try:
        print(f'####\nend of experiment, \ntotal presses: {lever2.total_presses}\n')
    except:
        print('whoops, dave tried to make a change that didnt work. maybe call him down.')
        
        # move time  ?? (TODO: ask if this script should have a move time like in door shape)


        #
        # Inter-trial Interval --> interval where nothing is happening before we start next round ( time to move voles )
        #
        


    #
    # Shutdown
    #
    
    box.shutdown()
 

if __name__ == '__main__':
    run()

