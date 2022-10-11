'''
    Experiment (4/4): Door Test

Questions: 
-> will there be more than one vole in the main chamber? ( i.e. is it possible that both levers will reach there goal number of presses meaning that we should open both doors in a single round? )

'''
from RPI_Operant.hardware.box import Box
import time
import random
from pathlib import Path
experiment_name = Path(__file__).stem
RUNTIME_DICT = {'vole':000, 'day':1, 'experiment':experiment_name}

# # For Running on the Raspberry Pi: 
USER_HARDWARE_CONFIG_PATH = '/home/pi/RPI_Operant2/RPI_Operant/default_setup_files/local_hardware.yaml'
USER_SOFTWARE_CONFIG_PATH = '/home/pi/anne_experiment/yaml_setup_files/two_chamber_operant_laser_software.yaml'


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

    time.sleep(0.5)
    
    #simplifying hardware calls
    lever2 = box.levers.door_2
    door = box.doors.door_1 
    beam = box.beams.door1_ir
    speaker = box.speakers.speaker1
    laser = box.lasers.laser1


    # Ensure doors are closed and laser is off at start 
    setup_phase = box.timing.new_phase('setup')
    door.close()
    box.doors.door_2.close()
    laser.turn_off()
    setup_phase.end_phase()
        
    
    for i in range(box.software_config['values']['rounds']):
        
        print(f'ROUND {i+1}')
        box.timing.new_round(length = box.software_config['values']['round_length'])

        speaker.play_tone('round_start') # Round Start Tone 

        # # Phase 1: Extending Door Levers # # 
        phase = box.timing.new_phase(f'lever_out', length = box.software_config['values']['round_length'])
        
        # door1 and door2 lever out 
        press_latency = lever2.extend()
        lever2.wait_for_n_presses(n=1, latency_obj = press_latency)
        while phase.active() and not lever2.presses_reached: 
            '''waiting here for something to happen'''
        
        # immediately end the lever-out phase 
        lever2.retract()
        phase.end_phase()


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

            # Turn Laser On 
            laser.turn_on()

            time.sleep(1) # pause another second to reach a 5 second delay

            # Tone & Open Door 
            speaker.play_tone(tone_name='door_open')
            door.open()

            # Reward Time 
            phase = box.timing.new_phase(name = 'reward_time', length = box.software_config['values']['reward_time'])
            phase.wait() # door will remain open for 30 seconds 
            phase.end_phase()

            # Turn Off 
            laser.turn_off()
            speaker.play_tone(tone_name='door_close')
            door.close()

            # Stop tracking beam breaks (interaction zone) until next round
            beam.stop_getting_beam_broken_durations() # quits thread that gets durations
            beam.end_monitoring() # quits thread that timestamps every beam break
            
        else:

            print('no lever press')


        # move time (TODO) ask if i need move Time!

        
        # Intertrial Interval --> interval where nothing is happening before we start next round ( time to move voles )
        iti_phase = box.timing.new_phase(f'ITI', length = box.software_config['values']['ITI'])
        time.sleep(box.software_config['values']['ITI'])
        iti_phase.end_phase()


    #
    # Shutdown
    #
    box.shutdown()
 

if __name__ == '__main__':
    run()

