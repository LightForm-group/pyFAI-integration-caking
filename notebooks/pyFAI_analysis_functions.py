import matplotlib.pyplot as plt
import numpy as np
import pyFAI.gui.jupyter
import pyFAI
import fabio
from pyFAI.test.utilstest import UtilsTest
from pyFAI.calibrant import CALIBRANT_FACTORY
from pyFAI.goniometer import SingleGeometry
import pathlib
from tqdm import tqdm
import logging
import math
import warnings
import os
import pyFAI.azimuthalIntegrator
from pyFAI.gui import jupyter
import yaml

def get_config(path: str) -> dict:
    """Open a yaml file and return the contents."""
    with open(path) as input_file:
        return yaml.safe_load(input_file)
    
def calibrate(input_calibrant_path: str, beam_centre_x: float, beam_centre_y: float, sample_detector_distance: float, 
              wl: float, pixel_x: float, pixel_y: float, calibrant_type: str, num_calibration_rings: str, 
              output_calibration_path: str, figure_size: int):
    
    frame = fabio.open(input_calibrant_path).data
    dimensions = np.shape(frame)
    print(f"Size of the detector: \n {dimensions} \n")
    figure = plt.figure(figsize=(figure_size, figure_size))
    ax = plt.gca()
    pyFAI.gui.jupyter.display(frame, ax=ax)
    
    detector = pyFAI.detectors.Detector(pixel1=pixel_x, pixel2=pixel_y) # DESY 2021
    print(f"Definition of the detector: \n {detector} \n")
    calibrant = CALIBRANT_FACTORY(calibrant_type)
    calibrant.wavelength = wl
    print(f"Definition of the calibrant: \n {calibrant} \n")
    
    initial_geometry = pyFAI.geometry.Geometry(detector=detector, wavelength=wl)
    initial_geometry.setFit2D(sample_detector_distance, beam_centre_x, beam_centre_y)
    print(f"Initial guessed detector geometry: \n {initial_geometry} \n")
    
    # use the SingleGeometry object to perform automatic ring extraction and calibration
    sg = SingleGeometry("demo", frame, calibrant=calibrant, detector=detector, geometry=initial_geometry)
    sg.extract_cp(max_rings=num_calibration_rings)
    
    # figure showing initial fit
    figure = plt.figure(figsize=(figure_size, figure_size))
    ax = plt.gca()
    pyFAI.gui.jupyter.display(sg=sg, ax=ax)
    
    # refine geometry with fixed wavelength
    sg.geometry_refinement.refine2(fix=["wavelength"])
    
    # figure showing refined fit
    figure = plt.figure(figsize=(figure_size, figure_size))
    ax = plt.gca()
    pyFAI.gui.jupyter.display(sg=sg, ax=ax)
    
    print(f"Final calibration parameters... \n")
    # delete the calibration if it already exists
    # pathlib.Path(calibration_path).unlink(missing_ok=True) # only works for 3.8+
    try:
        pathlib.Path(output_calibration_path).unlink()
    except FileNotFoundError:
        pass

    # save the geometry obtained
    sg.geometry_refinement.save(output_calibration_path)
    with open(output_calibration_path) as f:
        print(f.read())
        
    print(f"Calibration .poni file written to: {output_calibration_path}")

def azimuthal_integration_iteration(input_path: str, input_experiment_list: list, glob_search_term: str,
                                    output_path: str, output_experiment_list: list,
                                    ai, mask, number_of_points: int):

    # suppress warnings when TIFFs are read
    logging.getLogger("fabio.TiffIO").setLevel(logging.ERROR)

    for input_experiment, output_experiment in zip(input_experiment_list, output_experiment_list):

        # get a list of the files
        image_list = sorted(pathlib.Path(input_path + input_experiment).glob(glob_search_term))

        for image_path in tqdm(image_list):
            # create an image array and integrate the data
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                image = fabio.open(image_path)
            pattern_image_array = image.data
            result = ai.integrate1d(pattern_image_array,
                                number_of_points,
                                azimuth_range=(-180,180),
                                mask = mask,
                                unit="2th_deg",
                                correctSolidAngle=True,
                                polarization_factor=0.99,
                                method='full_csr')

            result_array = np.column_stack((result.radial, result.intensity))
            
            # check output folder exists
            output_folder = f"{output_path}{output_experiment}/azimuthal-integration-test/"
            CHECK_FOLDER = os.path.isdir(output_folder)

            if not CHECK_FOLDER:
                os.makedirs(output_folder)
                print("Created folder : ", output_folder)
            
            # write out the integrated data to a text file
            np.savetxt(f"{output_folder}{image_path.stem}.xy", result_array)
            
        print(f"Saved .xy azimuthal integration files to folder : {output_folder}")
        
def caking_iteration_xrdfit(input_path: str, input_experiment_list: list, glob_search_term: str,
                            output_path: str, output_experiment_list: list,
                            ai, mask, number_of_points: int, number_of_cakes: int):
    
    # suppress warnings when TIFFs are read
    logging.getLogger("fabio.TiffIO").setLevel(logging.ERROR)

    # rotate the detector by half a cake width so that the cardinal direction
    # is in the center of the first cake not the edge.
    first_cake_angle = 360 / number_of_cakes
    ai.rot3 = (first_cake_angle / 2) * (math.pi / 180) # convert rotation to radians

    for input_experiment, output_experiment in zip(input_experiment_list, output_experiment_list):
        
        # get a list of the files
        image_list = sorted(pathlib.Path(input_path + input_experiment).glob(glob_search_term))

        for image_path in tqdm(image_list):
            # create empty array
            caked_data = np.zeros((number_of_cakes + 1, number_of_points))

            # create an image array and cake the data
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                image = fabio.open(image_path)
            pattern_image_array = image.data
            result2d = ai.integrate2d(pattern_image_array,
                                    number_of_points,
                                    number_of_cakes,
                                    mask = mask,
                                    unit="2th_deg",
                                    polarization_factor=0.99,
                                    method='full_csr')

            # flip the intensity data to order cakes clockwise rather than anticlockwise
            intensity = np.flip(result2d.intensity.T, axis=1)

            # reshape radial labels to 2D array so they can be attached to the intensity data.
            radial = np.reshape(result2d.radial, (-1, 1))

            result_array = np.hstack((radial, intensity))

            # check output folder exists
            output_folder = f"{output_path}{output_experiment}/caking-test/"
            CHECK_FOLDER = os.path.isdir(output_folder)

            if not CHECK_FOLDER:
                os.makedirs(output_folder)
                print("Created folder : ", output_folder)

            # write out the caked data to a text file
            np.savetxt(f"{output_folder}{image_path.stem}.dat", result_array)

        print(f"Saved .dat caked data files to folder : {output_folder}")
        
def caking_iteration_maud(input_path: str, input_experiment_list: list, glob_search_term: str,
                          output_path: str, output_experiment_list: list,
                          ai, mask, pixel_size: float, number_of_points: int, number_of_cakes: int):
    
    # suppress warnings when TIFFs are read
    logging.getLogger("fabio.TiffIO").setLevel(logging.ERROR)

    # rotate the detector by half a cake width so that the cardinal direction
    # is in the center of the first cake not the edge.
    first_cake_angle = 360 / number_of_cakes
    ai.rot3 = (first_cake_angle / 2) * (math.pi / 180) # convert rotation to radians

    for input_experiment, output_experiment in zip(input_experiment_list, output_experiment_list):
    
        # get a list of the files
        image_list = sorted(pathlib.Path(input_path + input_experiment).glob(glob_search_term))
        
        for image_path in tqdm(image_list):
            # create empty array
            caked_data = np.zeros((number_of_cakes + 1, number_of_points))

            # create an image array and cake the data
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                image = fabio.open(image_path)
            pattern_image_array = image.data
            result2d = ai.integrate2d(pattern_image_array,
                                    number_of_points,
                                    number_of_cakes,
                                    mask = mask,
                                    unit="r_mm",
                                    polarization_factor=0.99,
                                    method='full_csr')

            # flip the intensity data to order cakes clockwise rather than anticlockwise
            intensity = np.flip(result2d.intensity.T, axis=1)

            # reshape radial labels to 2D array so they can be attached to the intensity data.
            radial_mm = np.reshape(result2d.radial, (-1, 1))
            radial_pixel = radial_mm/pixel_size

            result_array = np.hstack((radial_pixel, intensity))
            
            # check output folder exists
            output_folder = f"{output_path}{output_experiment}/texture-maud/"
            CHECK_FOLDER = os.path.isdir(output_folder)

            if not CHECK_FOLDER:
                os.makedirs(output_folder)
                print("Created folder : ", output_folder)
            
            # write out the caked data to a text file
            np.savetxt(f"{output_folder}{image_path.stem}.dat", result_array)
        
        print(f"Saved .dat caked data files to folder : {output_folder}")
