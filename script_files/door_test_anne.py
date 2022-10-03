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
USER_HARDWARE_CONFIG_PATH = '/home/pi/anne_experiment/yaml_setup_files/door_test_hardware.yaml'
USER_SOFTWARE_CONFIG_PATH = '/home/pi/anne_experiment/yaml_setup_files/door_test_software.yaml'


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
        # Ensure doors are closed at start 
        setup_phase = box.timing.new_phase('setup')
        box.doors.door_1.close(wait=True)
        box.doors.door_2.close(wait=True)
        box.lasers.laser1.turn_off()
        setup_phase.end_phase()
        
        for i in range(box.software_config['values']['rounds']):
            
            print(f'ROUND {i+1}')
            box.timing.new_round(length = box.software_config['values']['round_length'])

            box.speakers.speaker1.play_tone('round_start') # Round Start Tone 

            # # Phase 1: Extending Door Levers # # 
            lever_phase = box.timing.new_phase(f'lever_out', length = box.software_config['values']['round_length'])
            
            # door1 and door2 lever out 
            press_latency_1 = box.levers.door_1.extend()
            press_latency_2 = box.levers.door_2.extend()
            box.levers.door_1.wait_for_n_presses(n = 1, latency_obj = press_latency_1)
            box.levers.door_2.wait_for_n_presses(n = 1, latency_obj = press_latency_2)

            lever_pressed = 0 # 0 represents no lever press 
            while lever_phase.active(): 

                if box.levers.door_1.presses_reached or box.levers.door_2.presses_reached: # door lever was pressed 
                    #
                    # lever 1 or 2 reached Goal Presses
                    # Logic for what should happen if there is a lever press 
                    #

                    if box.levers.door_1.presses_reached: 
                        lever_pressed = 1 
                    else: 
                        lever_pressed = 2


                    # Retract All Levers
                    box.levers.door_1.retract()
                    box.levers.door_2.retract()
                    # lever_phase.end_phase()

                    # 
                    # Tone, Delay, Lasers, 1 Sec Delay, Reward (Door Opens)
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
            

                    # Reward: Open the Opposite Door and monitor for a beam break                     
                    if lever_pressed == 1: 
                        time.sleep(1) # pause another second to reach a 5 second delay until door opens

                        # lever 1 press reward: open the OPPOSITE door ( door 2 )
                        door2_lat_obj = box.doors.door_2.open(wait=True)
                        # Monitor door 2 for First Beam Break 
                        box.beams.door2_ir.monitor_beam_break(latency_to_first_beambreak = door2_lat_obj, end_with_phase=lever_phase)
                    else: 
                        # Lasers Come On until Door Closes 
                        box.lasers.laser1.turn_on()

                        time.sleep(1) # pause another second to reach a 5 second delay until door opens

                        # lever 2 press reward: open the OPPOSITE door ( door 1 )
                        door1_lat_obj = box.doors.door_1.open(wait = True)
                        # monitor door 1 for first beam break 
                        box.beams.door1_ir.monitor_beam_break(latency_to_first_beambreak = door1_lat_obj, end_with_phase=lever_phase)


                    # Pause for Reward Time ( time that door is open for )
                    box.timing.wait_for_round_finish()
                    
                    # QUESTION: should we end phase ( to stop monitoring for a beam break ) or close door FIRST?? --> move placement of reward_phase.end_phase() to before or after closing the door to decide this
                    
                    # Laser Off
                    box.lasers.laser1.turn_off() 
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
                box.levers.door_1.retract() # retract levers
                box.levers.door_2.retract()
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

