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

         
    #simplifying hardware calls
    lever2 = box.levers.door_2
    door = box.doors.door_1 
    beam = box.beams.door1_ir
    speaker = box.speakers.speaker1

    progressive_ratio = box.software_config['progressive_ratio']
    # Ensure doors are closed at start 
    setup_phase = box.timing.new_phase('setup')
    door.close()
    box.doors.door_2.close()
    setup_phase.end_phase()
    presses_required = 1

    experiment_length_phase = box.timing.new_phase(f'maximum_experiment_length', length = box.software_config['values']['maximum_experiment_length'])
    
    round_number = 0
    while experiment_length_phase.active():
        
        round_number+=1
        print(f'ROUND {round_number}')
        box.timing.new_round()
        box.speakers.speaker1.play_tone('round_start') # Round Start Tone 


        lever_phase = box.timing.new_phase(f'breakpoint_timeout', length = box.software_config['values']['breakpoint_timeout'])
        press_latency_2 = lever2.extend()
        lever2.wait_for_n_presses(n = presses_required, latency_obj = press_latency_2, retract_lever = True)

        

        # if they press w/in the roundtime: 
        # monitor for beam break
        while lever_phase.active() and not lever2.presses_reached:
            '''waiting here for something to happen'''

        
        #immediately end the lever-out phase 
        lever2.retract()   
        lever_phase.end_phase()

        if lever2.presses_reached: 
            
            # Interaction Zone Durations & Beam Break Timestamps 
            beam.start_getting_beam_broken_durations() 
            beam.monitor_beam_break() # ( TODO ) -- keep only if timestamps for every beam break are wanted. 

            # Delay 
            try: 
                delay = box.software_config['values']['delay_by_day'][RUNTIME_DICT['day']-1] # grab delay that corresponds with the day number 
            except IndexError: 
                delay = box.software_config['delay_default'] # if day num goes over the delay_by_day values entered in the software file, use the delay default value instead 
            time.sleep(delay)            

            # Tone & Open Door
            speaker.play_tone(tone_name='door_open')
            door.open()

            # Reward Time 
            phase = box.timing.new_phase(name = 'reward time', length = box.software_config['values']['reward_time'])
            phase.wait() # door will be open for 30 seconds
            phase.end_phase()

            # Tone & Close Door
            speaker.play_tone(tone_name='door_close')
            door.close()
        
            # Stop tracking beam breaks (interaction zone) until next round
            beam.stop_getting_beam_broken_durations() # quits thread that gets durations
            beam.end_monitoring() # quits thread that timestamps every beam break
            
            
            #update PR
            presses_required += progressive_ratio
            
        else: # No Lever Press -> Go Straight to ITI 
            print('no lever press')

        
        # move time  ?? (TODO: ask if this script should have a move time like in door shape)


        #
        # Inter-trial Interval --> interval where nothing is happening before we start next round ( time to move voles )
        #
        iti_phase = box.timing.new_phase(f'ITI', length = box.software_config['values']['ITI'])
        time.sleep(box.software_config['values']['ITI'])
        iti_phase.end_phase()


    #
    # Shutdown
    #
    box.shutdown()
 

if __name__ == '__main__':
    run()

