# ImageProcessing_Project

NCSU ECE 558 Image Processing
A.J. Beckmann, Bryan Wilson, Henry Pickett

This repository houses the final project for ECE 558 Image Processing, project option 1. 

This project creates a Laplacian blending function and GUI. The blended function is then saved in your local repository as "blend.png".

Running the GUI:
    1. Create venv and pip install -r requirements.txt.
    2. Run gui.py.
    3. In GUI, select foreground and background images.
    4. Create mask by clicking and dragging over desired region of foreground image.
    5. Select the "Blend Images" button. 

    

    Note: Only two images of the same size can be used for blending.

Bryan's Contribution:
    Bryan wrote the gui.py script. This script renders a user interface that interacts with the laplacian blending function, 
    allowing a user to upload two images for which they would like to merge. The user can 
    capture a window of the foreground image that they would like to merge with the background image. 
    The merged image then appears between the two selected images and is saved in their local repository. 
    The process can be done repeatedly with various images and various window sizes. 
    
Henry's Contribution:
    Henry wrote the function to implement Gaussian and Laplacian pyramid. This function works by taking an input image and a desired number of layers for the pyramids. The function tests if the pyramid can have the number of desired layers, and if not creates a pyramid with the maximum number of layers possible. The first layer (level 0) of the gaussian pyramid is the input image, the following levels are created by applying a gaussian filter over the image and then downsampling using nearest neighbor interpolation. The gaussian filter is applied using the convolution function created in project 2. Once the Gaussian pyramid is created the Laplcian pyramid can be created. The top layer of the Laplacian pyramid is the top layer of the Gaussian pyramid. Each lower level of the Laplacian pyramid is created by taking a difference of gaussians. The laplacian pyramid level is created by taking the gaussian pyramid image that is one level higher, upsampling it to the size of the size of the image in the equivalent level of the gaussian pyramid and the subtracting the upsampled image from the image of the gaussian pyramid at the desired layer. The lower levels of the pyramid give you the higher frequency details of the image, while the higher levels provide the lower frequency details

A.J.'s Contribution:
    A.J. created the laplacian blending function, blend(). This function works by taking
    the foreground image, background image, and mask and using ComputePyr() to generate their 
    laplacian and gaussian pyramids. It then computes the blended pyramid of the two images, 
    where blended_pyramid = gpMask * gpForegroundImage + (1-gpMask) * gpBackgroundImage at each
    pyramid level. It then collapses the blended pyramid, starting from the top down, by taking layer i
    and upscaling it, smoothing it to remove nearest neighbor interpolation artifacts, and adding it 
    to layer i-1. The resulting blended image is the 0th layer of the blended pyramid. Finally,
    normalization is performed.

Challenges:
    Data type issues were problematic in the developement of the gaussian pyramid, laplacain pyramid, convolution, and blending functions. Since images are input as datatype uint8 these functions were designed to work for arrays with the datatype uint8. However uint8 did not provide the precision we required for this project so we had to change all these functions to be more robust an work regardless of datatype. This allowed us to use the float data type which gave us the precision we required.

    Picking the correct way to blur posed a challenge as well. Deteremining what type of gaussian kernel as well as what sort of padding to use when convoluting our images with the gaussian kernel to blur them took a process of both online research as well as trial and error.

    Using nearest neighbor interpolation, used for upsampling and downsampling, resulted in pixelation like artifacts in our blended image. To combat this, we implemented a gaussian smoothing when upsampling every pyramid level in the laplacian pyramid collapsing process. This succesfully smoothed out the artifacts. 

    Combining all our individual parts into a single, concise means of operation was also difficult, as we were pretty unfamiliar with python GUI generation and object oriented programming. Although our implementation may be slighlty rough, I think it acheived a good job of implementing a self-contained GUI.


