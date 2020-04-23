#!/usr/bin/bash

source venv/Scripts/activate

rm -r results/*

python run_experiments.py --batch --instance "mazes/maze12x12_3_*" --solver ICTS
python run_experiments.py --batch --instance "mazes/maze25x25_3_*" --solver ICTS
python run_experiments.py --batch --instance "mazes/maze50x50_3_*" --solver ICTS
python run_experiments.py --batch --instance "mazes/maze100x100_3_*" --solver ICTS

python run_experiments.py --batch --instance "open_maps/open12x12_3_*" --solver ICTS
python run_experiments.py --batch --instance "open_maps/open25x25_3_*" --solver ICTS
python run_experiments.py --batch --instance "open_maps/open50x50_3_*" --solver ICTS
python run_experiments.py --batch --instance "open_maps/open100x100_3_*" --solver ICTS

python run_experiments.py --batch --instance "mazes/maze12x12_3_*" --solver EPEA
python run_experiments.py --batch --instance "mazes/maze25x25_3_*" --solver EPEA
python run_experiments.py --batch --instance "mazes/maze50x50_3_*" --solver EPEA
python run_experiments.py --batch --instance "mazes/maze100x100_3_*" --solver EPEA

python run_experiments.py --batch --instance "open_maps/open12x12_3_*" --solver EPEA
python run_experiments.py --batch --instance "open_maps/open25x25_3_*" --solver EPEA
python run_experiments.py --batch --instance "open_maps/open50x50_3_*" --solver EPEA
python run_experiments.py --batch --instance "open_maps/open100x100_3_*" --solver EPEA



