PyFAI-integration-caking
-----------

A set of Python notebooks for the calibration, azimuthal integration and caking of synchrotron X-ray diffraction (SXRD) pattern images, using the pyFAI and FabIO packages. The notebooks can be used for calibration, and then for azimuthal integration or caking of synchrotron diffraction images, to enable further processing and analysis of synchrotron data using software packages such as [TOPAS](https://www.bruker.com/en/products-and-solutions/diffractometers-and-scattering-systems/x-ray-diffractometers/diffrac-suite-software/diffrac-topas.html), [xrdfit](https://xrdfit.readthedocs.io), or [MAUD](http://maud.radiographema.eu).

Azimuthal integration is the first step necessary for calculating bulk phase fraction from the ratio of different phase peak intensities using TOPAS. Caking is neccessary for determining elastic lattice strain, from peak shifts along particular directions, using xrdfit. And caking can also be used to determine crystallographic texture from intensity variations of different lattice plane peaks along different directions, using xrdfit or MAUD. This package supports these analyses by converting the diffraction pattern images into calibrated integrated and caked data in different text formats.

The package works with diffraction pattern image data in the form of .cbf or .tiff images. And also includes a notebook for converting diffraction pattern images from .cbf to .tiff format.

The azimuthally integrated and caked data can be output as .xy, .dat, or in other text formats, along with a .poni calibration file.

Development
--------------

This package was developed by Christopher S. Daniel and Peter Crowther at The 
University of Manchester, UK, and was funded by the Engineering and Physical Sciences Research Council (EPSRC) via the LightForm programme grant (EP/R001715/1). LightForm is a 5 year multidisciplinary project, led by The Manchester University with partners at University of Cambridge and Imperial College, London (https://lightform.org.uk/).

Contents
-----------

**It is recommended the user works through the examples in the notebooks in the following order:**
    
1. `pyFAI-calibration-example.ipynb` An example notebook demonstrating calibration of the detector and beamline setup based on a calibrant standard diffraction pattern image, such as CeO2 of LaB6. The calibration paramaters are saved as a .poni file.

2. `pyFAI-caking-example.ipynb` An example notebook demonstrating azimuthal integration and caking of diffraction pattern images for saving as text files. Includes an example for saving data in a format to be used in TOPAS, xrdfit and MAUD.

3. `pyFAI-sample-rotation-example.ipynb` An example notebook demonstrating how the diffraction pattern image is displayed in the notebook and how to rotate the data if required.

4. `pyFAI-analysis.ipynb` A notebook for automatically calibrating, azimuthally integrating and caking large synchrotron diffraction pattern image datasets, using input parameters contained in .yaml input files.

5. `cbf_to_tif_image_converter.ipynb` A notebook for converting diffraction pattern images from .cbf to .tiff format, using input parameters contained in .yaml input files.

*Note, the `example-data/`, `example-calibration/` and `example-analysis/` folders contain data that can be used as an example analysis, but a clear external file structure should be setup to support the analysis of large synchrotron datasets.*

Installation and Virtual Environment Setup
-----------

Follow along by copying / pasting the commands below into your terminal (for a guide on using a python virtual environments follow steps 4-7).

**1. First, you'll need to download the repository to your PC. Open a unix command line on your PC and navigate to your Desktop (or GitHub repository):**
```unix
cd ~/Desktop
```
**2. In your teminal, use the following command to clone this repository to your Desktop:**
```unix
git clone https://github.com/LightForm-group/PyFAI-integration-caking.git
```
**3. Navigate inside `Desktop/PyFAI-integration-caking/` and list the contents using `ls`(macOS) or `dir`(windows):**
```unix
cd ~/Desktop/PyFAI-integration-caking/
```
**4. Next, create a python virtual environment (venv) which contains all of the python libraries required to use PyFAI-integration-caking.
Firstly, use the following command to create the venv directory which will contain the necessary libraries:**
```unix
python -m venv ~/Desktop/PyFAI-integration-caking/venv
```
**5. Your `PyFAI-integration-caking/` directory should now contain `venv/`. Install the relevant libraries to this venv by first activating the venv:**
```unix
source ~/Desktop/PyFAI-integration-caking/venv/bin/activate
```
*Note, the beginning of your command line should change from `(base)` to include `(venv)`.*

**6. Install the python libraries to this virtual environment using pip and the `requirements.txt` file included within the repository:**
```unix
pip install -r ~/Desktop/PyFAI-integration-caking/requirements.txt
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
**8. If all in step 7 are present, you can now run the example notebooks.
Ensure the venv is active and use the following command to boot jupyter notebook (using all libraries installed in the venv).
Warning - using just `jupyter notebook` without `python -m` can result in using your default python environment (the libraries may not be recognised):**
```unix
python -m jupyter notebook
```
**9. Work through the notebooks and setup yaml text files for reproducible calibration, azimuthal integration and caking of diffraction pattern images for large synchrotron datasets.**

**10. When you're finished using the virtual environment, deactivate it!
This will avoid confusion when using different python libraries that are not installed within the virtual environment:**
```unix
deactivate
```

Required Libraries
--------------------

The required libraries are listed in requirements.txt