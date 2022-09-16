

Running Experiments 
=====

Terminal Commands
------

*for all of these commands, ensure that you are positioned in the RPI_Operant2 directory* 


command to run experiment(s) that are specified by the csv file lasers_csv_mac.csv: 
~~~
python3 -m RPI_Operant.launcher -i '/home/pi/anne_experiment/csv_input_files/experiments.csv'
~~~


Steps for Adding a New Script
========
1. add a python script file in the directory script_files that contains logic for how we want experiment to execute 
2. add a software configuration yaml file in the directory yaml_setup_files 
3. add a hardware configuartion yaml file in the directory yaml_setup_files 
4. make updates to the CSV File that you plan to run so it contains the file paths to the newly created script and configuration files 
5. push changes to Github! ( then pull from the other raspberry pis to update each pi with the new changes )

CSV File Inputs
------
Fill out the CSV file with values that will direct the launcher to the script you want to run and what hardware/software configurations should be used when running that script.

**script_path** contains the filepath to the directory with the scripts to run 
~~~
/home/pi/anne_experiment/script_files/file_name.py
~~~

**script_setup** contains the filepath to the yaml file that specifies the *software* configurations. **hardware_setup** contains the filepath to the yaml file that specifies the *hardware* configurations. The filepath to the directory containing the setup files is: 
~~~
/home/pi/anne_experiment/yaml_setup_files/file_name.yaml
~~~

**output_path** contains the path to a directory where the experiments output data should get written 
~~~
/home/pi/anne_experiment/outputs
~~~


SSH Into Pi
====
*these steps utilize the extension: Visual Studio Code Remote - SSH*
- open VS code
- on keyboard: CMND-Shift-P 
- in the search bar, click on the item that says "Remote-SSH: Connect to Host..."
- in the input field, enter "pi@00.000.0.000" ( replace numbers with the ip address specific to the raspberry pi )
- type in password when prompted 
- if successful, when you navigate to the Explorer tab in Visual Studio Code, you should see an option that says "Open Remote" which when clicked, allows you to choose what directory you would like to navigate to on the pi.  

Github Things
=====
    this section explains how to get the code that sits in the github repository (https://github.com/sarah-litz/anne_repository.git) onto a Raspberry Pi. It also explains the process of when changes are made to a file in the repository, how to push those changes to github, and then how to pull those changes in order to update the code on every Raspberry Pis that is connected to this repository.

Cloning Repository to get code stored on github onto a new Raspberry Pi
-----

*this command is for when a repository of code does not exist on a pi. If the repository already exists and you are trying to update the code with changes, then instead you need to pull updates from github (covered in more detail below).*

Ensure that you are positioned in the directory that you want the repository to appear in, and then run the following command in a terminal.  
~~~
git clone https://github.com/sarah-litz/anne_repository.git
~~~

Pushing new changes to Github
------
after making changes or writing a new python script for running an experiment, in order to save the changes we have made to github, we need to push the changes to github with the following commands: 
~~~
git add . 
git commit -m "message describing what changes are getting made"
git push 
~~~

*note that files in the output folder will NOT be saved to github. These files can be downloaded and saved separately.*

Pulling updates from Github
----- 
if the scripts that are stored on a pi are not up to date with the latest changes that were made to a script, then we should pull from github in order to get the new changes on the pi. 
~~~
git pull 
~~~


Other Notes
=====
commands to run hardware tests: 
----
~~~
python3 -m RPI_Operant.default_scripts.calibrate_lasers
python3 -m RPI_Operant.default_scripts.calibrate_levers
python3 -m RPI_Operant.default_scripts.calibrate_dispenser
python3 -m RPI_Operant.default_scripts.show_outputs
python3 -m RPI_Operant.default_scripts.test_beambreak
~~~
notes on script syntax 
----
**notes on Laser Script Syntax when writing new scripts**
- to iterate thru every laser pattern, loop thru any laser object's pattern list ( e.g. for pattern in box.lasers.laser1.patterns )
- to add logic for when we should trigger playing a certain pattern, we can use the phase functionality ( like while phase.active, check for a certain condition that if met will cause us to exit from the phase early and enter a new phase)