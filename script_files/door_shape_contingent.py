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
USER_HARDWARE_CONFIG_PATH = '/home/pi/anne_experiment/yaml_setup_files/door_shape_contingent_hardware.yaml'
USER_SOFTWARE_CONFIG_PATH = '/home/pi/anne_experiment/yaml_setup_files/door_shape_contingent_software.yaml'


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
        
        # Close Doors to Start 
        setup_phase = box.timing.new_phase('setup')
        box.doors.door_1.close(wait=True)
        box.doors.door_2.close(wait=True)
        setup_phase.end_phase()


        for i in range(box.software_config['values']['rounds']):
            
            print(f'ROUND {i+1}')
            box.timing.new_round(length = box.software_config['values']['round_length'])

            box.speakers.speaker1.play_tone('round_start') # Round Start Tone 

            '''
            lever1 controls door2
            lever2 controls door1

            first 5 rounds, lever1 comes out 
            next 5 rounds, lever2 comes out 

            repeat this twice 
            '''

            lever_phase = box.timing.new_phase(f'round_interval_120', length = box.software_config['values']['round_length'])
            if i < 5 or (i < 15 and i > 9): 
                # First 5 rounds, extend lever 2
                press_latency_2 = box.levers.door_2.extend()
                box.levers.door_2.wait_for_n_presses(n = 1, latency_obj = press_latency_2)
            else: 
                # Second 5 Rounds; extend lever1 
                press_latency_1 = box.levers.door_1.extend()
                box.levers.door_1.wait_for_n_presses(n = 1, latency_obj = press_latency_1)

            

            # if they press w/in the roundtime: 
            # monitor for beam break
            lever_pressed = 0 # 0 represents no lever press 
            while lever_phase.active(): 

                if box.levers.door_1.presses_reached or box.levers.door_2.presses_reached: # door lever was pressed 
                    
                    #
                    # lever 1 or 2 reached Goal Presses
                    # Logic for what should happen if there is a lever press 
                    #

                    if box.levers.door_1.presses_reached: 
                        lever_pressed = 1 
                        # Monitor, Retract 
                        # box.beams.door2_ir.monitor_beam_break(end_with_phase=lever_phase) --> monitoring moved below before we open door 
                        box.levers.door_1.retract()


                    else: 
                        lever_pressed = 2
                        # Monitor, Retract
                        # box.beams.door1_ir.monitor_beam_break(end_with_phase=lever_phase) --> monitoring moved below before we open door 
                        box.levers.door_2.retract()


                    # 
                    # Tone, Delay, and Reward 
                    # 
                    
                    # tone 
                    box.speakers.speaker1.play_tone('door_open') 
                    
                    # delay 
                    try: 
                        delay = box.software_config['values']['delay_by_day'][RUNTIME_DICT['day']-1] # grab delay that corresponds with the day number 
                    except IndexError: 
                        # if day num goes over the delay_by_day values entered in the software file, use the delay default value instead 
                        delay = box.software_config['delay_default']
                    time.sleep(delay)
            
                    
                    if lever_pressed == 1: 
                        # lever 1 press reward: open the OPPOSITE door ( door 2 )
                        door2_lat_obj = box.doors.door_2.open()
                        box.beams.door2_ir.monitor_beam_break(latency_to_first_beambreak = door2_lat_obj, end_with_phase=lever_phase)
                    else: 
                        # lever 2 press reward: open the OPPOSITE door ( door 1 )
                        door1_lat_obj = box.doors.door_1.open()
                        box.beams.door1_ir.monitor_beam_break(latency_to_first_beambreak = door1_lat_obj, end_with_phase=lever_phase)

                    # Pause for Reward Time ( time that door is open for ) --> Whatever the remaining round time is is the reward time 
                    box.timing.wait_for_round_finish() # sleeps until the round time is over 
                    
                    # tone 
                    box.speakers.speaker1.play_tone('door_close')
                    # Close the opened door
                    if lever_pressed == 1: 
                        box.doors.door_2.close(wait=True)
                    else: 
                        box.doors.door_1.close(wait=True) 

                    lever_phase.end_phase() # END OF REWARD PHASE


            if lever_pressed == 0: 

                #
                # Logic for what shold happen if there is NO lever press 
                #
                if i < 5 or (i < 15 and i > 9): 
                    # First 5 Rounds; retract lever2
                    box.levers.door_2.retract()
                else: 
                    # Second 5 rounds, retract lever 2
                    box.levers.door_1.retract()

                lever_phase.end_phase()
                print('no lever press')
            

            #
            # move time 
            #
            print('\n time to move the vole over! ')
            move_phase = box.timing.new_phase(f'Move Vole', length = box.software_config['values']['move_time'])
            time.sleep(box.software_config['values']['move_time'])
            move_phase.end_phase()
            print('\n vole should be moved now.')


            #
            # Intertrial Interval --> interval where nothing is happening before we start next round ( time to move voles )
            #
            iti_phase = box.timing.new_phase(f'ITI', length = box.software_config['values']['ITI'])
            time.sleep(box.software_config['values']['ITI'])
            iti_phase.end_phase()


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

