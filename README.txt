This README file details how to setup your environment to run our code and how to run the code.
Note: I am running these commands on a windows machine. If you are not, please replace '\' with '/'

PREREQUISITE:
It is a requirement you have python (at least 3.7) and pip already installed on your machine

------ Setting up the environment ------
Follow the steps to install all necessary packages and setup a python virtual environment
Create a virtual environment in the ICTS-vs-EPEA folder:

python -m venv venv

To activate your virtual environment, consult the documentation, https://docs.python.org/3/library/venv.html
For windows powershell, I use the following command to activate my virtual environment

.\venv\Scripts\Activate.ps1

To deactivate the environment, simply run the command 'deactivate'

------ Installing the packages ------
To install all the necessary packages, run this command:

pip install -r .\requirements.txt

To verify the installation was correct, the output of 'pip list' should print this to your console

Package         Version
--------------- -------
cycler          0.10.0
kiwisolver      1.2.0
matplotlib      3.2.1
numpy           1.18.3
pandas          1.0.3
pip             19.0.3
pyparsing       2.4.7
python-dateutil 2.8.1
pytz            2019.3
scipy           1.4.1
seaborn         0.10.0
setuptools      40.8.0
six             1.14.0

------ Generating map instances ------
Map instances have already been generated for you and are provided in the 'mazes' and 'open_maps' directories.
If you would like to generate your own maps, you can run the following commands

Note: Running these commands will overwrite the maps provided.
To make new maps, create a new folder and change 'open_maps' in the output parameter to the new directory name.
This only works for open_map_generator.py.

python open_map_generator.py --output open_maps/test.txt --dim 50 50 --agents 3 --startnum 1 --nummaps 10 --probability 0.42 --adjacentprobability -0.08
python generate_mazes.py

The probability parameter sets the probability an open space becomes an obstacle
The adjacent probability parameter is added to the probability parameter for each adjacent obstacle. This prevents having too many adjacent obstacles

------ Running the map instances ------
The results of these commands will be saved to a file in a 'results' folder.
This command will run all open map instances that are 12 by 12 and write the results to
the file 'results/open12x12_3_ICTS_results.txt'.

python run_experiments.py --batch --instance open_maps\open12x12_3_* --solver ICTS

Here is a sample of the results:

{"algorithm": "ICTS", "map_name": "mazes\\maze12x12_3_0.txt", "heuristic_time": 0.0009975433349609375, "time": 0.0069463253021240234, "expanded nodes": 7}
{"algorithm": "ICTS", "map_name": "mazes\\maze12x12_3_1.txt", "heuristic_time": 0.0, "time": 0.006977081298828125, "expanded nodes": 11}
{"algorithm": "ICTS", "map_name": "mazes\\maze12x12_3_10.txt", "heuristic_time": 0.0, "time": 0.003987789154052734}
{"algorithm": "ICTS", "map_name": "mazes\\maze12x12_3_100.txt", "heuristic_time": 0.0009891986846923828, "time": 0.0029921531677246094, "expanded nodes": 4}

To run a single instance with an animation showing the solution, use the following command:

python run_experiments.py --instance open_maps\open12x12_3_0.txt --solver ICTS
