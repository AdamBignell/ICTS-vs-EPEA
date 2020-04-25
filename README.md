# CMPT 417 Final Project
### Spring 2020

##### Jeffrey Yamasaki, Marko Miletic, and Adam Bignell

In this project we implement and test ICTS and EPEA*, and compare the algorithms in both typical and pathological search spaces.

Our solution is built on top of the skeleton code provided in the assignment *Model AI Assignments 2020: A Project on Multi-Agent Path Finding (MAPF)* by Wolfgang Hönig, Jiaoyang Li, and Sven Koenig of the University of Southern California.

#### PREREQUISITES

Note: I am running these commands on a windows machine using powershell. If you are not, please use the appropriate slash (\ or /) for your terminal.
It is a requirement you have python (at least 3.7 or higher), pip, and git already installed on your machine

## Setting up the environment
Clone the repo using either of the commands

HTTPS:
```git clone https://github.com/AdamBignell/ICTS-vs-EPEA.git```

Navigate to the ICTS-vs-EPEA folder and create a virtual environment using this command:

```python -m venv venv```

To activate your virtual environment, consult the documentation, https://docs.python.org/3/library/venv.html.
For windows powershell, I use the following command to activate my virtual environment

```.\venv\Scripts\Activate.ps1```

To deactivate the environment, simply run the command 'deactivate'

## Installing the packages
To install all the necessary packages, run this command:

```pip install -r requirements.txt```

To verify the installation was correct, the output of 'pip list' should print this to your console

```
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
```

## Generating map instances
Map instances have already been generated for you and are provided in the 'mazes' and 'open_maps' directories.
If you would like to generate your own maps, you can run the following commands

Note: Running these commands will overwrite the maps provided.

For Open Maps:

```python open_map_generator.py --dim 50 50 --agents 3 --startnum 1 --nummaps 10 --probability 0.42 --adjacentprobability -0.08```

The probability parameter sets the probability an open space becomes an obstacle.
The adjacent probability parameter is added to the probability parameter for each adjacent obstacle. This prevents having too many adjacent obstacles.

For Mazes:

```python maze_map_generator.py --dim 50 50 --agents 3 --startnum 1 --nummaps 10 --probability 0.75```

The probability paramter sets the probability of opening a (non-cycle creating) cell during BFS from some seed location. 0.75 will branch in 3 directions on average. 0.50 will branch in 2 directions on average.

## Running the map instances
Note: if the below commands do not work, try use the same commands without the tick character (') around the --instance argument. Powershell and Git Bash terminals worked fine but the command prompt on windows interprets the ' character differently.

The results of these commands will be saved to a file in a 'results' folder.
This command will run all open map instances that are 12 by 12 and write the results to
the file 'results/open12x12_3_ICTS_results.txt'.

Testing ICTS:

```python run_experiments.py --batch --instance 'open_maps\open12x12_3_*' --solver ICTS```

Testing EPEA*:

```python run_experiments.py --batch --instance 'open_maps\open12x12_3_*' --solver EPEA```

Here is a sample of the results:

```
{"algorithm": "ICTS", "map_name": "mazes\\maze12x12_3_0.txt", "heuristic_time": 0.0009975433349609375, "time": 0.0069463253021240234, "expanded nodes": 7}
{"algorithm": "ICTS", "map_name": "mazes\\maze12x12_3_1.txt", "heuristic_time": 0.0, "time": 0.006977081298828125, "expanded nodes": 11}
{"algorithm": "ICTS", "map_name": "mazes\\maze12x12_3_10.txt", "heuristic_time": 0.0, "time": 0.003987789154052734}
{"algorithm": "ICTS", "map_name": "mazes\\maze12x12_3_100.txt", "heuristic_time": 0.0009891986846923828, "time": 0.0029921531677246094, "expanded nodes": 4}
```

To run a single instance with an animation showing the solution, use the following command:

For ICTS:

```python run_experiments.py --instance 'open_maps\open12x12_3_0.txt' --solver ICTS```

For EPEA*:

```python run_experiments.py --instance 'open_maps\open12x12_3_0.txt' --solver EPEA```

