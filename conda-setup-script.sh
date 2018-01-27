#!/bin/bash
export PATH="$HOME/miniconda2/bin:$HOME/miniconda/bin:$PATH"
conda create -y -n complexPlottingEnv python=2.7
conda install -y -n complexPlottingEnv mayavi jupyter 
export PATH="$(conda info --root)/envs/complexPlottingEnv/bin:$PATH"
cd "$(dirname "$(find $HOME -type f -name complex-plotting-jupyter-notebook.ipynb | head -1)")"
jupyter notebook
read -p "Press enter to close."

