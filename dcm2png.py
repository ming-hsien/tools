import pydicom
import numpy as np
import cv2
import os

def dcm2png(dcm_path,write_out = False):    ################### add by jerry ###################
    dcm_ = pydicom.read_file(dcm_path)
    dcmID = os.path.basename(dcm_path).replace('.dcm','')

    # get dicom array
    dcm_image = dcm_.pixel_array

    # get pixels Hounsfield unit
    intercept = dcm_.RescaleIntercept
    slope = dcm_.RescaleSlope

    if slope != -1:
        dcm_image = slope * dcm_image.astype(np.float64)

    # clip to [-1000,400]
    dcm_image = dcm_image.astype(np.int16) + np.int16(intercept)
    dcm_image = np.clip(dcm_image,-1000,400)

    # convert [-1000,400]->[0,255]
    dcm_image += 1000
    png_ = dcm_image.astype(np.float64)/1400*255

    # write out image to the dcm path
    if write_out:
        cv2.imwrite(os.path.join(os.path.dirname(dcm_path), dcmID +'.png'), png_)

    return png_.astype(np.uint8) , dcmID