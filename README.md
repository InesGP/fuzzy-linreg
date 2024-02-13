## ACM Scripts
* [MCA_Analysis.ipynb](https://github.com/InesGP/fuzzy-linreg/blob/main/MCA_Analysis.ipynb) contains the code to generate the figures in the ACM Rep 2024 paper under the section "Boxplots for Magnitude" and "Correlation Plots". The beginning of the notebook is primarily exploratory analysis that is not used in the paper
* [Sigmap_visualization.ipynb](https://github.com/InesGP/fuzzy-linreg/blob/main/Sigmap_visualization.ipynb) visualizes all OASIS subjects sigmaps for Fuzzy MCA and a concatenation of Docker and Guix. To see it, the notebook must be downloaded
* [utils](https://github.com/InesGP/fuzzy-linreg/tree/main/utils) folder contains helper scripts to run analusis
  * [calculate_sigmaps.py](https://github.com/InesGP/fuzzy-linreg/blob/main/utils/calculate_sigmaps.py) is a script that calculates the significant digits within the linearly registered images
  * [make_gifs.py](https://github.com/InesGP/fuzzy-linreg/blob/main/utils/make_gifs.py) is a script that will make a gif out of different executions of a file in order to observe the variability in the images
  * [create_invocations.py](https://github.com/InesGP/fuzzy-linreg/blob/main/utils/create_invocations.py) creates the input files that the Boutiques FSL FLIRT image requires
  * [transfo_utils.py](https://github.com/InesGP/fuzzy-linreg/blob/main/utils/transfo_utils.py) is a copy of the script from the [CREATIS team](https://gitlab.in2p3.fr/reprovipgroup/reprovip-notebooks-and-scripts) used to extract the parameters from the transformation matrices
* [build-docker.sh](https://github.com/InesGP/fuzzy-linreg/blob/main/build-docker.sh) can instrument any docker image with Fuzzy libmath. As an additional output to the instrumented image, it produces an instrumented Dockerfile. For FSL FLIRT, [Dockerfile.mcalibmath](https://github.com/InesGP/fuzzy-linreg/blob/main/Dockerfile.mcalibmath) is the instrumented Dockerfile

### [BrainHack Presentation slides](https://docs.google.com/presentation/d/1YFJpvblpDLOppZ6d7gQabD7yhvWF2xcNl2UUiX6Y-F8)
