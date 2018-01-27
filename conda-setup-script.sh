#!/bin/bash
export PATH="$HOME/miniconda/bin:$PATH"
conda create -n complexPlottingEnv python=2.7
conda install -n complexPlottingEnv -y mayavi jupyter 
export PATH="$(conda info --root)/envs/complexPlottingEnv/bin:$PATH"
cd "$(dirname "$(find $HOME -type f -name complex-plotting-jupyter-notebook.ipynb | head -1)")"
jupyter notebook
read -p "Press enter to close."

