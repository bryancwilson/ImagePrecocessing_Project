import numpy as np
import cv2
import matplotlib.pyplot as plt
import math

class laplacian_blender:
    def __init__(self, SOURCE=None, TARGET=None, MASK=None):
        self.source = SOURCE
        self.target = TARGET
        self.mask = MASK

    #################### PART A ####################
    def Get_2D_Gaussian_kernel(self):
        kernel_size = 5
        sigma = np.sqrt(2)
        #Kernel_size should be an odd integer
        #sigma is the standard deviation of the Gaussian
        # Generate 1D Gaussian kernel
        kernel_1d = cv2.getGaussianKernel(kernel_size, sigma)
        # Create a 2D Gaussian kernel by multiplying the 1D kernel with its transpose
        kernel_2d = kernel_1d @ kernel_1d.T
        return(kernel_2d)    


    def ComputePyr(self, input_image, num_layers):
        #check if num_layers is valid
        num_layers = num_layers - 1
        #find max layers from computing how many times the smallest dimension can be divided by two, add one for the base layer
        max_layers = np.log2(min(input_image.shape[:2]))
        max_layers = math.floor(max_layers)
        if num_layers > max_layers:
            num_layers = max_layers

        #Gaussian_Kernel = (1/256)*np.array([[1,2,6,4,1],[4,16,24,16,4],[6,24,36,24,6],[1,4,6,4,1]])
        Gaussian_Kernel = self.Get_2D_Gaussian_kernel()
        #initialize the gaussian pyramid  with the first layer as the original image
        gPyr = [input_image]
        #initialize conditions for the loop to create the gaussian pyramid
        current_image = input_image
        #loop to create the Gaussian Pyramid
        for layer in range(num_layers): #iterates num_layers - 1 times
            #blur the image
            blurred_image = self.conv2(current_image,Gaussian_Kernel,"reflect across edge")
            #use nearest neighbor downsampling
            height, width = blurred_image.shape[:2]
            current_image = cv2.resize(blurred_image, (width // 2, height // 2), interpolation=cv2.INTER_NEAREST)
            #add the downsampled image to the pyramid
            gPyr.append(current_image)

        #make laplcian pyramid
        lPyr = [] #create an empty list
        for layer in range(num_layers): #iterates max_layers - 1 times
            #upsample each layer
            upscaled_image = cv2.resize(gPyr[layer+1], (gPyr[layer].shape[1],gPyr[layer].shape[0]), interpolation=cv2.INTER_NEAREST) #doubles the dimensions and upscales using nearest neighbor method
            #subtract upsampled image from the next highest level from the current layer
            lPyr.append(np.maximum(gPyr[layer] - upscaled_image,0))
        #last level of lPyr is the last level of gPyr since there is no higher level to upsample
        lPyr.append(gPyr[num_layers])    

        return gPyr, lPyr

    #################### PART C ####################
    def blend(self, numLevels):
        # Get laplacian pyramids
        _, SOURCE_LP = self.ComputePyr(self.source, numLevels)
        _, TARGET_LP = self.ComputePyr(self.target, numLevels)
        MASK_GP, _ = self.ComputePyr(self.mask, numLevels)

        # Create blended pyramid
        blended_pyramid = [MASK_GP[0]*SOURCE_LP[0] + (1-MASK_GP[0])*TARGET_LP[0]]
        for i in range(1,numLevels):
            blended_pyramid.append(MASK_GP[i]*SOURCE_LP[i] + (1-MASK_GP[i])*TARGET_LP[i])
        
        # Collapse the blended pyramid
        #scale = 2
        for i in range(numLevels-1,0,-1):
            level = blended_pyramid.pop()
            level = self.upsample(level,blended_pyramid[i-1])
            blended_pyramid[i-1] = cv2.add(blended_pyramid[i-1], level)
        blended_image = blended_pyramid[0]
        
        # Normalize blended image to 0-255
        blended_image = self.normalize(blended_image, 255).astype(np.uint8)
        
        return blended_image
    
    ################ HELPER FUNCTIONS ################
    def upsample(self, IMAGE, Image_of_desired_size):
        upsampled_image = cv2.resize(IMAGE,(Image_of_desired_size.shape[1],Image_of_desired_size.shape[0]), interpolation=cv2.INTER_NEAREST)
        #upsampled_image = cv2.resize(IMAGE, (2*IMAGE.shape[0], 2*IMAGE.shape[1]), interpolation=cv2.INTER_NEAREST)
        upsampled_image = self.conv2(upsampled_image, self.Get_2D_Gaussian_kernel(), "reflect across edge" )
        return upsampled_image
    
    def normalize(self, INPUT, SCALE=1):
        # If input is a pyramid
        if isinstance(INPUT, list):
            # Get absolute max and min of all levels
            max = 1
            min = 0
            for level in INPUT:
                levelMax = np.max(level)
                levelMin = np.min(level)
                if levelMax > max:
                    max = levelMax
                if levelMin < min:
                    min = levelMin
            # Now normalize each level
            for levelIdx, level in enumerate(INPUT):
                # Convert to float
                level = level.astype(float)
                # Work in 3D
                grey = False
                if len(level.shape) == 2:
                    grey = True
                    level = np.expand_dims(level, axis=2)
                # Iterate through channels
                for idx, channel in enumerate(level.transpose(2, 0, 1)):
                    # Edge case
                    if np.max(channel) == 0:
                        continue
                    # Normalize (max will always be 255)
                    else:
                        channel = (channel - min)/(max - min)
                    # Assign channel to level
                    level[:,:,idx] = channel
                # Assign level to pyramid
                INPUT[levelIdx] = level
                if grey:
                    level = np.squeeze(level, -1)

        # If input is just an image
        else:
            INPUT = INPUT.astype(float)
            # Work in 3D
            grey = False
            if len(INPUT.shape) == 2:
                grey = True
                INPUT = np.expand_dims(level, axis=2)
            # Iterate through every channel
            for idx, channel in enumerate(INPUT.transpose(2, 0, 1)):
                # Edge case
                if np.max(channel) == 0:
                    continue
                # Normalize
                else:
                    channel = ((channel - np.min(channel)) / (np.max(channel) - np.min(channel))) * SCALE
                INPUT[:,:,idx] = channel
            if grey:
                INPUT = np.squeeze(INPUT, -1)
        return INPUT
        
    def conv2(self,f,w,pad): #f = input image, w = 2-D kernel filter, pad = the 4 padding types 

        def pad_gray_image(f,padding_width,pad):
            #np.pad(array,pad_width,mode)
            match pad:
                case 'zero padding':
                    return np.pad(f,pad_width = padding_width,mode='constant',constant_values = 0)
                case 'wrap around':
                    return np.pad(f,pad_width = padding_width,mode='wrap')
                case 'copy edge':
                    return np.pad(f,pad_width = padding_width,mode='edge')
                case 'refelct across edge':
                    return np.pad(f,pad_width = padding_width,mode='reflect')
        
        def pad_RGB_image(f,padding_width,pad):
            #np.pad(array,pad_width,mode)
            padding = ((padding_width,padding_width),(padding_width,padding_width),(0,0))
            match pad:
                case 'zero padding':
                    return np.pad(f,padding,mode='constant',constant_values = 0)
                case 'wrap around':
                    return np.pad(f,padding,mode='wrap')
                case 'copy edge':
                    return np.pad(f,padding,mode='edge')
                case 'reflect across edge':
                    return np.pad(f,padding,mode='reflect')
            
        def convolution_range(dimension_length):
            if dimension_length % 2 == 0: #(value is even)
                convolve_min = int(-dimension_length/2 +1)
                convolve_max = int(dimension_length/2)
            else:
                convolve_min = int(-(dimension_length-1)/2)
                convolve_max = int((dimension_length-1)/2)
            return convolve_min, convolve_max
        
        #step 0 get appropriate padding size based on kernel
        padding_dimension = max(w.shape)
        padding_size = padding_dimension // 2 

        #step 1 determine if its grayscale or RGB
        #if grayscale
        if len(f.shape) == 2:
            #step2 pad the image
            padded_image = pad_gray_image(f,padding_size,pad) #since we are only using up to a 3x3 kernel we can pad all images by 1 on each side
            height,width = f.shape #get original image dimensions
            g = np.zeros((height,width)) #make an array of the same dimesions to be filled for the output image
            k_height, k_width = w.shape #get the height and width of the kernel
            height_convolve_min, height_convolve_max = convolution_range(k_height)
            width_convolve_min, width_convolve_max = convolution_range(k_width)
            kernel_height_center = int((height_convolve_max-height_convolve_min)/2 - ((height_convolve_max-height_convolve_min) % 2))
            kernel_width_center = int((width_convolve_max-width_convolve_min)/2 - ((width_convolve_max-width_convolve_min) % 2))
            for u in range(padding_size,height+padding_size): #plus one because images are padded by one on each side
                for v in range(padding_size,width+padding_size):
                    convolution_value = 0
                    for k_u in range(height_convolve_min,height_convolve_max+1):
                        for k_v in range(width_convolve_min,width_convolve_max+1):
                            convolution_value = convolution_value + padded_image[(u+k_u),(v+k_v)]*w[(kernel_height_center+k_u),(kernel_width_center+k_v)]
                    g[(u-padding_size),(v-padding_size)] = convolution_value

        #if RGB
        elif len(f.shape) == 3:
            #step 2 pad the image
            padded_image = pad_RGB_image(f,padding_size,pad)
            height,width = f.shape[:2] #get original image dimensions
            g = np.zeros((height,width,3)) #make an array of the same dimesions to be filled for the output image
            k_height, k_width = w.shape #get the height and width of the kernel
            height_convolve_min, height_convolve_max = convolution_range(k_height)
            width_convolve_min, width_convolve_max = convolution_range(k_width)
            kernel_height_center = int((height_convolve_max-height_convolve_min)/2 - ((height_convolve_max-height_convolve_min) % 2))
            kernel_width_center = int((width_convolve_max-width_convolve_min)/2 - ((width_convolve_max-width_convolve_min) % 2))
            for channel in range(0,3):
                for u in range(padding_size,height+padding_size): #plus one because images are padded by one on each side
                    for v in range(padding_size,width+padding_size):
                        convolution_value = 0
                        for k_u in range(height_convolve_min,height_convolve_max+1):
                            for k_v in range(width_convolve_min,width_convolve_max+1):
                                convolution_value = convolution_value + padded_image[(u+k_u),(v+k_v),channel]*w[(kernel_height_center+k_u),(kernel_width_center+k_v)]
                        g[(u-padding_size),(v-padding_size),channel] = convolution_value        
        return g
