import cv2, os
import numpy as np
from PIL import Image

imgDir = "./experiments/VesselNet/test/test_images/uploaded/"
imgFilenames = [f for f in os.listdir(imgDir) if f.lower().endswith("tif")]
def main_test():
    for imgFilenameIndex,imgFilename in enumerate(imgFilenames):
        if imgFilenameIndex > 0:
            break
        imgPath = os.path.join(imgDir, imgFilename)
        image = cv2.imread(imgPath)
        # cv2.imshow('original image', image)
        cv2.imwrite('./experiments/VesselNet/test/result/05_test.tif',image)
        
        ############################ preprocessing ####################################
        # taking the greeen channel
        r,imageGreen,b = cv2.split(image)
        # cv2.imshow('green channel image', imageGreen)
        cv2.imwrite('./experiments/VesselNet/test/result/greenchannel.tiff',imageGreen)
        #cv2.imshow('red channel image', r)
        #cv2.imshow('blue channel image', b)
        #cv2.imshow('gray scale channel image', cv2.cvtColor(image,cv2.COLOR_BGR2GRAY))
        
        # should do histogram matching here to counter different brightness and contrast
        
        # appplying contrast limited adaptive histogram equalisation
        clahe = cv2.createCLAHE(clipLimit = 2.0, tileGridSize = (8,8))
        imageEqualized = clahe.apply(imageGreen)
        # cv2.imshow('histogram equalized image', imageEqualized)
        cv2.imwrite('./experiments/VesselNet/test/result/equalized.tiff',imageEqualized)
        
        # inversion 
        imageInv2 = 255 - imageEqualized
        imageInv = clahe.apply(imageInv2)
        # cv2.imshow('inverted image', imageInv)
        cv2.imwrite('./experiments/VesselNet/test/result/inverted.tiff',imageInv)    
        cv2.imwrite('./experiments/VesselNet/test/result/inverted.tiff',imageInv)
        
        # median filter and subtraction to remove backeground did not work well
        #imageMed = cv2.medianBlur(imageInv, 33)
        #imageBackElm = imageInv - imageMed
        #cv2.imshow('background eliminated image', imageBackElm)
        
        # median filtering noise elimination
        kernel = np.ones((9,9),np.uint8)
        imageMed = cv2.medianBlur(imageInv, 5)
        # cv2.imshow('median filtered image',imageMed)
        cv2.imwrite('./experiments/VesselNet/test/result/backeliminated.tiff',imageMed )
        
        # top hat to remove background
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))
        #imageBackElm = cv2.morphologyEx(imageMed, cv2.MORPH_TOPHAT, kernel2)
        imageOpen = cv2.morphologyEx(imageMed, cv2.MORPH_OPEN, kernel2)
        imageBackElm = imageMed - imageOpen    
        # cv2.imshow('opened image', imageOpen)
        # cv2.imshow('background eliminated image', imageBackElm)
        cv2.imwrite('./experiments/VesselNet/test/result/backeliminated.tiff',imageBackElm)
        
        # enhancement
        
        # adaptive thresholding
        imagethresh2 = cv2.adaptiveThreshold(imageBackElm,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,13,1)
        # cv2.imshow('adaptive thresholded image', imagethresh2)
        
        # area threshholding
        imageCont, contours,hierarchy = cv2.findContours(imagethresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(image, contours, contourIdx=-1, color=0, thickness=-1)    
        # cv2.imshow('contour detected image', image)
        print('length of contours {}'.format(len(contours)))
        
        delete = []
        for i in range(len(contours)):
            area = cv2.contourArea(contours[i])
            if area > 50000.0:
                delete.append(i)
        print(delete)       
        # for i,idx in enumerate(delete):
        #     del contours[idx-i]
        print('length of contours after {}'.format(len(contours)))
        
        cv2.drawContours(imagethresh2, contours, contourIdx=-1, color=0, thickness=-1)    
        # cv2.imshow('contour deleted image', imagethresh2) 
        # 2nd itereation
        imageCont, contours,hierarchy = cv2.findContours(imagethresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(image, contours, contourIdx=-1, color=0, thickness=-1)    
        # cv2.imshow('contour detected image 2', image)
        print('length of contours {}'.format(len(contours)))
        
        delete = []
        for i in range(len(contours)):
            area = cv2.contourArea(contours[i])
            if area > 10000.0:
                delete.append(i)
        print(delete)       
        for i,idx in enumerate(delete):
            del contours[idx-i]
        print('length of contours after {}'.format(len(contours)))
        
        cv2.drawContours(imagethresh2, contours, contourIdx=-1, color=0, thickness=-1)    
        # cv2.imshow('contour deleted image 2', imagethresh2) 
        # cv2.imwrite('./experiments/VesselNet/test/result/image.tiff',imagethresh2)
        
        # open (did not used)    
        kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        imageOpen2 = cv2.morphologyEx(imageBackElm, cv2.MORPH_OPEN, kernel3)
        # cv2.imshow('opened image 2', imageOpen2)
        
        imageTrain = imagethresh2*imageBackElm
        # cv2.imshow('image to be trained', imageTrain)
        
        # make a copy
        img = imageTrain.copy()
        
        # training matrix
        print(img.shape)
        trainingMat = np.array(img.flatten(), np.float32) #error may occur --> then loop
        
    

if __name__ == '__main__':
    main_test()