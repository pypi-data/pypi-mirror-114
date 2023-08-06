## Use pip and Conda to make your software easy to install for everyone and reach a larger audience!

In this tutorial, you will learn how to make your existing tool pip and conda installable. Go ahead and start with cloning this repository:

`` git clone https://github.com/balabanmetin/pip-conda-tutorial-diameter.git``

`` cd pip-conda-tutorial-diameter``

Next, install the dependency packages for this tutorial using pip. Make sure your Python distribution has `pip` and `conda` installed. For pip:

``pip install twine setuptools``

For conda, download and install the correct [conda version](https://conda.io/projects/conda/en/latest/user-guide/install/index.html). Then, install conda-build:

`` conda install conda-build``

The application we are creating is [nw_diameter](nw_diameter). It is a simple script that takes a newick file as an input and computes its diameter (a.k.a. the largest pairwise tree distance within the tree).


### Pip tutorial 

In order to upload you project to PyPi (where pip packages are stored), you must create a PyPi account first using the following link:

[PyPi Register](https://pypi.org/account/register/)

Once the account is ready, you must create a [setup.py](setup.py) file. Go ahead and edit this file. You must change the package name (`name` field) since I already reserved the name `'tutorial-diameter'` for this tutorial ;)

`setup.py` is ready. Next we create a distribution archive by running the following command inside the repository directory:

`python setup.py sdist`

This creates a `tar.gz` file in a new directory `dist`. Final step is to upload this archive into PyPi servers using `twine`

`twine upload dist/*`

Type in the username and password of your PyPi account, and your package is now live!. Let's test it. Change to the `data` directory.

`cd data`

Install your package using pip. Since I named my package as `tutorial-diameter`, I install it using the following command:

`pip install tutorial-diameter`

If everything went well, run the command `nw_diameter` using the test newick file:

`nw_diameter data/tree.nwk`

Diameter of this tree is 0.7!.

### Conda tutorial
#### Using PyPi skeleton
If you have already built and uploaded your package to PyPi, you can use it as a skeleton to make the Conda build easier.

`conda skeleton pypi tutorial-diameter`

Now you should see the directory `tutorial-diameter` created for you, inside which you can see the file `meta.yaml`. This is the recipe needed to build a conda package. Now execute the following command to build:

`conda build tutorial-diameter`

You built package will be stored in `$HOME/anaconda3/conda-bld/<YOUR_PLATFORM>/tutorial-diameter-1.0.1-py<YOUR_PYTHON_VERSION>_0.tar.bz2`. To upload to Anaconda cloud, run the following :

```
anaconda login
anaconda upload `$HOME/anaconda3/conda-bld/<YOUR_PLATFORM>/tutorial-diameter-1.0.1-py<YOUR_PYTHON_VERSION>_0.tar.bz2`
```
where `<YOUR_PLATFORM>` is the platform of your machine (e.g. linux-64, osx-64, etc.)

#### Using Github
If you do not have a PyPi package, you can build a Conda package directly from your code on Github. To do so, simply change the `source` section of your `meta.yaml` to:

```
git_rev: main
git_url: https://github.com/balabanmetin/pip-conda-tutorial-diameter.git 
```

#### Building for multiple Python versions
As you may have noticed, so far we can only build a conda package that is limited to the Python version of the host machine that it was built on. To build the variants for multiple Python versions (e.g. 3.7, 3.8, and 3.9), you can add inside your `tutorial-diameter` directory the file `conda_build_config.yaml` with the following content:

```
python:
    - 3.9.*
    - 3.8.*
    - 3.7.*
```
Now when you run `conda build`, it will create three conda versions, corresponding to Python versions 3.7, 3.8, and 3.9, for your package.

#### Converting to other platforms
The conda built is platform specific. To convert to other platforms, use `conda convert`:

`conda convert --platform all <YOUR_CONDA_BUILT> -o outputdir/`

Now you should see multiple built versions, one for each platform. To upload all of them to Anaconda, type:

`anaconda upload outputdir/*/*`

Note: to choose a specific platform to convert to, change the keyword *all* to the platform of your choice (e.g. osx-64, linux-32, linux-64, win-32, win-64, etc.)

#### Installing and Testing
Install your package using conda:

`conda install -c <YOUR_CONDA_USERNAME> tutorial-diameter`

Now you should be able to run the command `nw_diameter` as before!
