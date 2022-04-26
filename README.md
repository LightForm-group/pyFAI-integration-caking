# pyFAI-integration-caking
A python script for the azimuthal integration and caking of SXRD diffraction pattern images, using the pyFAI and FabIO packages.

## Step-by-step examples
Follow along by copy/pasting the commands below into your terminal. (for a guide on using a python virtual environemnts follow steps 4-7).

**1. First, you'll need to download the pyFAI repository to your PC. Open a unix command line on your PC and navigate to your Desktop:**
```unix
cd ~/Desktop/
```
**2. In your teminal, use the following command to clone this repository to your Desktop:**
```unix
git clone https://github.com/LightForm-group/pyFAI-integration-caking.git
```
**3. Navigate inside `Desktop/pyFAI-integration-caking/` and list its contents using `ls`(macOS) or `dir`(windows):**
```unix
cd ~/Desktop/pyFAI-integration-caking/
```
**4. Next, we need to create a python virtual environment (venv) which contains all the python libraries required to use pyFAI.
Firstly, use the following command to create the venv directory which will contain the necessary libraries:**
```unix
python -m venv ~/Desktop/pyFAI-integration-caking/venv
```
**5. Your `pyFAI-integration-caking/` directory should now contain `venv/`. Now we need to install the relevant libraries to this venv.
We do this by first activating the venv:**
```unix
source ~/Desktop/pyFAI-integration-caking/venv/bin/activate
```
The beginning of your command line should change from `(base)` to include `(venv)`.

**6. Now we can install the python libraries we need to this virtual environment using pip and the `requirements.txt` file that comes with the repository:**
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
**8. If all in step 7. are present, you can now run the pyFAI example notebooks.
Ensure the venv is active and use the following command to boot jupyter notebook(using all libraries installed in the venv)
Warning - using just `jupyter notebook` without `python -m` will result in using your default python environment (the pyFAI library will not be recognised):**
```unix
python -m jupyter notebook
```
**9. It is recommended the user works through the example notebooks in the following order:**
    
1. `pyFAI-calibration-example.ipynb` How to create the .poni detector calibration file.

2. `pyFAI-caking-example.ipynb` How to cake the data with comparison to DAWN.
    
3. `pyFAI-sample-rotation-example.ipynb` Example of how to rotate data when detector alignment is not satisfactory.

**10. When you're finished using the virtual environment, !!ENSURE TO DEACTIVE IT!!
This will avoid confusion when you need to use a python library that is not installed within the venv/ you're using**
```unix
deactivate
```
