# complex-plotting
Some python code for visualizing complex functions (from the complex plane to the complex plane) using domain coloring and contour lines.

By Carl Plant (cplant@berkeley.edu).

This displays an intereactive 3D plot including a section of the complex plane and the Rieman (Stereographic) Sphere (https://en.wikipedia.org/wiki/Riemann_sphere). The view can be panned, rotated, & zoomed—and the sphere or plane can be hidden—within the interactive GUI, but setting the function to be plotted, the resolution, the nature of the contours, and so forth must be done by altering the code before execution. See the code for details. 

As an amateur Pythoneer, much credit and thanks is due to the authors of the example code I stitched together to make this:
- Gael Varoquaux (using Mayavi meshes): http://docs.enthought.com/mayavi/mayavi/auto/example_spherical_harmonics.html#example-spherical-harmonics
- [Unnamed] (customizing the color LUTs): http://docs.enthought.com/mayavi/mayavi/auto/example_custom_colormap.html#example-custom-colormap
- Gael Varoquaux (interactivity using Traits): http://docs.enthought.com/mayavi/mayavi/auto/example_mlab_interactive_dialog.html
- Peter Wang (handling multiple TraitsUI windows): http://markmail.org/download.xqy?id=xwknkqhqh4uvs5bf&number=1

## Set-up instructions:
### If you don't have Python 2.7 installed:
Install it! I recommend the [Miniconda distribution](https://conda.io/miniconda.html), you'll need the Python 2.7 version.
You can then run the *conda-setup-script.sh* to get everything set up for Mayavi, the package that makes all this work. The script will open up the Jupyter notebook interface when it's done, you can just open `complex-plotting-jupyter-notebook.ipynb` and press shift+enter to run the code.

Use the *reopen-script.sh* to pick up where you left off if you close Jupyter and come back later.

### If you already have Python installed:
I recommend cut-and-pasting the contents of [complex-plotting-main.py](https://github.com/seaplant3/complex-plotting/blob/master/complex-plotting-main.py) into a [Jupyter](http://jupyter.org/install) notebook cell where you can edit it easily and press  shift+enter to run. You can also just run it from the terminal with `python /path/to/complex-plotting-main.py`. 

**The Mayavi module might not work** or install at all depending on what other modules you have installed (such as matplotlib). If you have that problem—or you're using Python 3, or have other errors—the ***conda-setup-script.sh* should fix it.** If you don't have conda installed (most people already do) you can get it [here](https://conda.io/miniconda.html).

Use the *reopen-script.sh* to pick up where you left off if you close Jupyter and come back later. Or, run `source activate complexPlottingEnv` before running `jupyter notebook` or `python ...` to load the settings for Mayavi.

### If my BASH scripts don't work, or other problems occur:

in your terminal if you have Python 2.7 installed. If you don't, or you encounter problems, read on. If your problem is just that you're using Windows, I recommend Linux (but in the meantime the command you need is probably `C:\python27\python.exe C:\path\to\where\you\downloaded\complex-plotting-main.py`).

If you don't have Python 2.7 or the Mayavi module installed already, I recommend these steps. This will build a special python environment with just the packages you need for this code, to prevent Mayavi's dependencies from conflicting with anything else (like matplotlib). Terminal commands are for Linux, but should work with little alteration on other systems.
1) Install Anaconda, Python 2.7 version: https://www.anaconda.com/download/
2) Create a clean new environment by running `conda create -n myEnvName python=2.7`
3) Switch into this environment by running `source activate myEnvName`. (myEnvName) should appear in your terminal prompt.
4) Install the mayavi and jupyter packages in this environment: run `conda install mayavi` and then `conda install jupyter`
5) Run the code! Either run `jupyter notebook` and cut-and-paste the code into a notebook cell, or run `python /path/to/where/you/downloaded/complex-plotting-main.py`. Just make sure to run `source activate myEnvName` first if it isn't already showing up in your terminal prompt.

Note that it might take ~15 seconds to start, and will probably throw some warnings like 'overflow' or 'invalid value' while it does its calculations. This is normal.

Questions or comments? I'd love to hear it! Leave them here on GitHub, send me an email (cplant@berkeley.edu), or fox them to me.
