
'''

'''



from RPI_Operant.hardware.box import Box
import time
import random
from pathlib import Path
experiment_name = Path(__file__).stem
RUNTIME_DICT = {'vole':000, 'day':1, 'experiment':experiment_name}

# # For Running on the Raspberry Pi: 
USER_HARDWARE_CONFIG_PATH = '/home/pi/anne_experiment/yaml_setup_files/autoshape_contingent_hardware.yaml'
USER_SOFTWARE_CONFIG_PATH = '/home/pi/anne_experiment/yaml_setup_files/autoshape_contingent_software.yaml'


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
    
        
    try:
        
        for i in range(box.software_config['values']['rounds']):
            
            print(f'ROUND {i+1}')
            box.timing.new_round(length = box.software_config['values']['round_length'])

            box.speakers.speaker1.play_tone('round_start') # Round Start Tone 

            # # Phase 1: Extending Food Lever # # 
            phase = box.timing.new_phase(f'food_lever_out', length = box.software_config['values']['lever_out_time'])
            
            # food lever out 
            press_latency_1 = box.levers.food.extend()
            box.levers.food.wait_for_n_presses(n = 1, latency_obj = press_latency_1)

            while phase.active(): 
                
                if box.levers.food.presses_reached: # food lever was pressed 

                    #
                    # Logic for what should happen if there is a food lever press 
                    #

                    # retract lever 1 
                    box.levers.food.retract()

                    # Pellet Tone, Delay, and Pellet Dispense
                    box.speakers.speaker1.play_tone('pellet_tone') # sound 
                    # 
                    # Delay 
                    try: 
                        box.software_config['values']['delay_by_day'][RUNTIME_DICT['day']-1] # grab delay that corresponds with the day number 
                    except IndexError: 
                        # if day num goes over the delay_by_day values entered in the software file, use the delay default value instead 
                        time.sleep(box.software_config['delay_default']) 
                    # Dispense 
                    box.dispensers.continuous_dispenser_1.dispense()
                    phase.end_phase()

            if not box.levers.food.presses_reached: 

                #
                # Logic for what shold happen if there is NO lever press 
                #
                box.levers.food.retract() # retract food lever 

                print('no lever press')
            
            phase.end_phase() # Early exit from the Lever Out Phase, doesn't need to complete until 300 seconds finishes


            #
            # Intertrial Interval -- > 30 second interval where nothing is happening before we start next round
            #
            phase = box.timing.new_phase(f'ITI', length = box.software_config['values']['ITI'])
            time.sleep(box.software_config['values']['ITI'])
            phase.end_phase()


        #
        # Shutdown
        #
        box.shutdown()
 
    except KeyboardInterrupt:
        print('keyboard interrupt, shutting down')
        speaker1.turn_off()
        positional_dispenser_1.stop_servo()
        lever_door_1.retract()
        box.levers.door_1.retract()
        lever_door_2.retract()
        laser1.turn_off()
        box.force_shutdown()

if __name__ == '__main__':
    run()

