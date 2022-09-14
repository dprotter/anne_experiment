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
        
        for i in range(box.software_config['values']['rounds']):
            
            print(f'ROUND {i+1}')
            box.timing.new_round(length = box.software_config['values']['round_length'])

            box.speakers.speaker1.play_tone('round_start') # Round Start Tone 

            # # Phase 1: Extending Door Levers # # 
            phase = box.timing.new_phase(f'door_levers_out', length = box.software_config['values']['lever_out_time'])
            
            # door1 and door2 lever out 
            press_latency_1 = box.levers.door_1.extend()
            press_latency_2 = box.levers.door_2.extend()
            box.levers.door_1.wait_for_n_presses(n = 1, latency_obj = press_latency_1)
            box.levers.door_2.wait_for_n_presses(n = 1, latency_obj = press_latency_2)

            while phase.active(): 
                
                if box.levers.door_1.presses_reached: # door lever was pressed 

                    #
                    # Logic for what should happen if there is a door 1 lever press 
                    #

                    # retract lever 1 
                    box.levers.door_1.retract()


                    # Tone, Delay, and Open the OPPOSITE door

                    #
                    # Delay 
                    try: 
                        box.software_config['values']['delay_by_day'][RUNTIME_DICT['day']-1] # grab delay that corresponds with the day number 
                    except IndexError: 
                        # if day num goes over the delay_by_day values entered in the software file, use the delay default value instead 
                        time.sleep(box.software_config['delay_default']) 
                    
                    #
                    # Open door 2 
                    door2_lat_obj = box.doors.door_2.open(wait=True)
                    # Monitor door 2 for First Beam Break 
                    box.beams.door2_ir.monitor_beam_break(latency_to_first_beambreak = door2_lat_obj, end_with_phase=phase)

                    # 
                    #  Assuming we should pause here to allow a moment for the vole to run thru the newly opened door ?? 
                    # 
                    
                    # End Phase: we will stop monitoring for a beam break at the point that we choose to end phase. 
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
'''

Anne Experiment (4/4)
Description: 
- implementing lasers turning on/off 

key_values = {'num_rounds': 20,
              'round_time':2*60,
              'reward_time':60,
              'move_time':20,
              'ITI':30,
              'pellet_tone_time':1, 
              'pellet_tone_hz':2500,
              'door_close_tone_time':1, 
              'door_close_tone_hz':7000,
              'door_open_tone_time':1,
              'door_open_tone_hz':10000,
              'round_start_tone_time':1, 
              'round_start_tone_hz':5000,
              'delay by day':[5],
              'delay default':5}


key_values_def = {'num_rounds':'number of rounds',
                  'round_time':'total round length',
                  'reward_time':'time door is left open',
                  'move_time':'seconds to move the vole back to the lever room',
                  'ITI':'time immediately preceeding the start of a new round',
                  'pellet_tone_time':'in s', 
                  'pellet_tone_hz':'in hz',
                  'door_close_tone_time':'in s', 
                  'door_close_tone_hz':'in hz',
                  'door_open_tone_time':'in s',
                  'door_open_tone_hz':'in hz',
                  'round_start_tone_time':'in s', 
                  'round_start_tone_hz':'in hz',
                  'delay by day':'delay between lever press and reward',
                  'delay default':'delay between lever press and reward if beyond delay by day length'}



setup --> reverse lever position; causes the lever further from the door to be the lever that opens that door instead of the lever that is closest to the door 

round buzz 

extend and monitor lever 1 & 2 
if a lever is pressed, open the OPPOSITE door
    monitor for a beam break to track if vole walks thru door 
if the lever is not pressed, retract levers



'''
