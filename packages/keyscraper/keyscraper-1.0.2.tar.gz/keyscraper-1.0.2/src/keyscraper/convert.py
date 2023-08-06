from datetime import datetime
import os, cv2, numpy, random, math, sys
#b from matplotlib import pyplot
np = numpy
#from imutils.video import WebcamVideoStream
from os.path import exists
#from urllib.request import urlretrieve
#from tensorflow.keras import models
#import h5py
# from matplotlib import image
from urllib.request import urlretrieve
import time

absolutePath = "./"

# download model if not exists
prototxt = absolutePath + "deploy.prototxt"
caffemodel = absolutePath + "res10_300x300_ssd_iter_140000.caffemodel"

if not exists(prototxt) or not exists(caffemodel):
    urlretrieve(f"https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/{prototxt}", prototxt)
    urlretrieve(f"https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/{caffemodel}", caffemodel)


# initialize model
net = cv2.dnn.readNetFromCaffe(prototxt=prototxt, caffeModel=caffemodel)

# Detect function
# min_confidence: the minimum probability to filter detections, i.e., the minimum probability to keep a detection
def detect(img, min_confidence=0.6):
    # get the height and width of the image
    try:
        (h, w) = img.shape[:2]
    except:
        return None

    # create a 4D blob from the image
    # the parameters are:
    # 1. the input image
    # 2. the scalar value that normalizes the pixel values
    # 3. the width and height of the image
    # 4. b subtract 104, g subtract 117, r subtract 123
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    # setup the input(blob) and get the results
    net.setInput(blob)
    detectors = net.forward()

    # initialize our list of bounding boxes
    bounding_boxs = []

    # loop all the results after detection
    for i in range(0, detectors.shape[2]):
        # get the confidence of the prediction
        confidence = detectors[0, 0, i, 2]

        # filter out weak detections, which is lower than 60%
        if confidence < min_confidence:
            continue

        # box is a list that contains the distances of the left, top, right and bottom of the bounding box
        box = detectors[0, 0, i, 3:7] * np.array([w, h, w, h])
        (x0, y0, x1, y1) = box.astype("int")
        bounding_boxs.append({"box": (x0, y0, x1 - x0, y1 - y0)})

    return bounding_boxs

class BasicData:
    
    
    """
    
        The dimension of jpeg files: 
            
            (1080, 1080) when dim = 1080
            ( 300,  300) when dim =  300
            ( 160,  160) when dim =  160
        
    """
    
    dim = 160
    
    
    """
    
        The extension of neural network models.
        
    """
    
    #modelExtension = ".h5"
    
    modelExtension = ".hdf5"

class Images(BasicData):
    
    
    # This function confines batchScale to ( 0.0, 1.0 ]
    
    def __check_scale(self, scale):
        
        
        """
            
            To ensure that at least 1 file will be loaded when there are some files available,
        we pick an arbitrarily-small number 1e-10 as the lower bound of batchScale instead of 0.
        
            => [ 1e-10, 1.0 ] ≈ ( 0.0, 1.0 ] 
        
        """
        
        return max(1e-10, min(scale, 1.0))
    
    
    # This function identifies whether or not a file name is that of a jpeg one
    
    def __is_jpeg(self, name):
        
        return ((name[-4:].lower() == ".jpg") or (name[-5:].lower() == ".jpeg"))
    
    def __init__(self, folderPath = "./", batchScale = 1.0, shuffle = False):
        
        
        # The names of all jpeg files inside the folder are found and placed in a list
        
        self.nameList = [ 
            folderPath + name for name in os.listdir(folderPath) \
                if (self.__is_jpeg(name) and os.path.isfile(folderPath + name))
        ]
        
            
        # Shuffling the list containing the names of jpeg files
        
        if (shuffle):
            random.shuffle(self.nameList)
        
        
        # The number of jpeg files found in the folder
        #   An index pointing to the beginning of the next batch
        
        self.total, self.pointer = len(self.nameList), 0
        
        
        # The maximum number of jpeg files to be loaded at a time
        
        self.batch = math.ceil(self.total * self.__check_scale(batchScale))
        
    def load_images(self):
        
        self.imageList = []
        
        
        # No images will be loaded when the pointer has reached the end of the list
        
        if (self.pointer < self.total):
            
            
            # Loading jpeg files in grayscale mode and normalizing pixel data from [ 0, 255 ] to [ 0.0, 1.0 ]
            
            # .reshape(-1, self.dim, self.dim, 1)
            
            self.imageList = [
                cv2.imread(name, cv2.IMREAD_COLOR) \
                    for name in self.nameList[ self.pointer : self.pointer + self.batch ]
            ]
                
            
            # Converting [ numpy.array([1]), numpy.array([2]) ] to numpy.array([ [1], [2] ])
            
            #self.imageList = numpy.stack(self.imageList, axis = 0)
                
            
            # Updating the pointer and bounding it within [ 0, self.total ]
            
            self.pointer = min(self.pointer + self.batch, self.total)
        
        
        # Saving the number of images in the current batch
        
        self.curBatch = len(self.imageList)
        
        return self.curBatch
    
imagePath = absolutePath + "imageset4/"

mask = Images(folderPath = imagePath)

numImage = mask.load_images()

for index in range(numImage):
    cur = mask.imageList[index]
    bounding_boxes = detect(cur)
    if(bounding_boxes == None):
        continue
    name = mask.nameList[index]
    for _index, bounding_box in enumerate(bounding_boxes):
        (x, y, w, h) = bounding_box["box"]
        
        frame = cur
        crop = cv2.cvtColor(
            cv2.resize(cur[y : y + h, x : x + w], (160, 160), interpolation = cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
        sys.stdout.write(f"\r{index}_{_index}")
        cv2.imwrite(name + f"{index}_{_index}.jpg", crop)
        sys.stdout.flush()