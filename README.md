# ImageProcessing_Project

NCSU ECE 558 Image Processing
A.J. Beckmann, Bryan Wilson, Henry Pickett

This repository houses the final project for ECE 558 Image Processing, project option 1. 

This project creates a Laplacian blending function and GUI.

Running the GUI:
    1. Create venv and pip install -r requirements.txt.
    2. Run gui.py.
    3. In GUI, select foreground and background images.
    4. Create mask by clicking and dragging over desired region of foreground image.
    5. Select the "Blend Images" button. 

    Note: Only two images of the same size can be used for blending.

Bryan's Contribution:

Henry's Contribution:

A.J.'s Contribution:
    A.J. created the laplacian blending function, blend(). This function works by taking
    the foreground image, background image, and mask and using ComputePyr() to generate their 
    laplacian and gaussian pyramids. It then computes the blended pyramid of the two images, 
    where blended_pyramid = gpMask * gpForegroundImage + (1-gpMask) * gpBackgroundImage at each
    pyramid level. It then collapses the blended pyramid, starting from the top down, by taking layer i
    and upscaling it, smoothing it to remove nearest neighbor interpolation artifacts, and adding it 
    to layer i-1. The resulting blended image is the 0th layer of the blended pyramid. Finally,
    normalization is performed.