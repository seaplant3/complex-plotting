#!/bin/bash
export PATH="$HOME/miniconda/bin:$PATH"
export PATH="$(conda info --root)/envs/complexPlottingEnv/bin:$PATH"
cd "$(dirname "$(find $HOME -type f -name complex-plotting-jupyter-notebook.ipynb | head -1)")"
jupyter notebook
read -p "Press enter to close."

