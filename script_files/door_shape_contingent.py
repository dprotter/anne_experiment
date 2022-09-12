
'''

default_setup_dict = {'vole':'000','day':1, 'experiment':'Door_shape_contingent',
                    'user':'Test User', 'output_directory':'/home/pi/test_outputs/', 'partner':'door_1', 'novel_num':'000'}


key_values = {'num_rounds': 0,
              'repetitions':5,
              'sets':2,
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
              'delay by day':[1,2,3,5,5],
              'delay default':5}

key_values['num_rounds'] = 2 * key_values['repetitions'] * key_values['sets'] 

key_values_def = {'num_rounds':'number of rounds',
                  'repetitions':'number of consecutive rounds',
                  'sets':'number of sets of training (1 set = partner reps + novel reps)',
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

#for display purposes. put values you think are most likely to be changed early
key_val_names_order = ['num_rounds', 'repetitions','round_time', 'time_II', 'move_time','pellet_tone_time',
                        'ITI','pellet_tone_hz','door_close_tone_time','door_close_tone_hz',
                        'door_open_tone_time','door_open_tone_hz', 'round_start_tone_time',
                        'round_start_tone_hz']



'''