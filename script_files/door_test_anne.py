
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
