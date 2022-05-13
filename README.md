# pyFAI-integration-caking
A series of python notebooks for the azimuthal integration and caking of synchrotron X-ray diffraction (SXRD) pattern images, using the pyFAI and FabIO packages.

# Contents
**It is recommended the user works through the example notebooks in the following order:**
    
1. `pyFAI-calibration-example.ipynb` How to create a .poni detector calibration file, based on calibration diffraction pattern image.

2. `pyFAI-sample-rotation-example.ipynb` How to rotate data when detector alignment is not satisfactory.

3. `pyFAI-caking-example.ipynb` How to azimuthally integrate and cake a series of diffraction pattern images, based on calibration parameters.

4. `notebooks/pyFAI-analysis.ipynb` A script for caking and azimuthal integration of large datasets, based on yaml text file input, for reproducible recording of the input parameters.

*Note, the `example-calibration/`, `example-data/` and `example-analysis/` contain files supporting the first 3 notebooks, but a clear external file structure should be setup to support the analysis of large synchrotron datasets in step 4.*

## Installation and Virtual Environment Setup
Follow along by copying / pasting the commands below into your terminal (for a guide on using a python virtual environments follow steps 4-7).

**1. First, you'll need to download the pyFAI repository to your PC. Open a unix command line on your PC and navigate to your Desktop or GitHub repositiory:**
```unix
cd ~/Desktop/
```
**2. In your teminal, use the following command to clone this repository to your Desktop:**
```unix
git clone https://github.com/LightForm-group/pyFAI-integration-caking.git
```
**3. Navigate inside `Desktop/pyFAI-integration-caking/` and list the contents using `ls`(macOS) or `dir`(windows):**
```unix
cd ~/Desktop/pyFAI-integration-caking/
```
**4. Next, create a python virtual environment (venv) which contains all of the python libraries required to use pyFAI.
Firstly, use the following command to create the venv directory which will contain the necessary libraries:**
```unix
python -m venv ~/Desktop/pyFAI-integration-caking/venv
```
**5. Your `pyFAI-integration-caking/` directory should now contain `venv/`. Install the relevant libraries to this venv by first activating the venv:**
```unix
source ~/Desktop/pyFAI-integration-caking/venv/bin/activate
```
*Note, the beginning of your command line should change from `(base)` to include `(venv)`.*

**6. Install the python libraries to this virtual environment using pip and the `requirements.txt` file included within the repository:**
```unix
pip install -r ~/Desktop/pyFAI-integration-caking/requirements.txt
```
**7. To ensure these installed correctly, use the command `pip list` and ensure the following packages are installed:**
```unix
pip list
# Check to ensure that all of the following are listed:
#jupyter
#pyFAI
#xrdfit
#fabio
#numpy
#pyyaml
```
**8. If all in step 7 are present, you can now run the pyFAI example notebooks.
Ensure the venv is active and use the following command to boot jupyter notebook (using all libraries installed in the venv)
Warning - using just `jupyter notebook` without `python -m` can result in using your default python environment (the pyFAI library may not be recognised):**
```unix
python -m jupyter notebook
```
**9. Work through the notebooks and setup yaml text files for reproducible caking and azimuthal integration analysis of large synchrotron datasets.

**10. When you're finished using the virtual environment, deactivate it!
This will avoid confusion when using different python libraries that are not installed within the virtual environment:**
```unix
deactivate
```
