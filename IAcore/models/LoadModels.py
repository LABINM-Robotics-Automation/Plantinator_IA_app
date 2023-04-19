"""
    LoadModel class
    usando modulo TekvotHub
"""

import sys
sys.path.append('/home/pqbas/projects/LABINM_Robotics_Automation/Plantinator_IA_app/IAcore/models/TekvotHub')

sys.path.append('/home/pqbas/projects/LABINM_Robotics_Automation/Plantinator_IA_app/IAcore/models/TekvotHub/detectors')
sys.path.append('/home/pqbas/projects/LABINM_Robotics_Automation/Plantinator_IA_app/IAcore/models/TekvotHub/detectors/yolov7')

sys.path.append('/home/pqbas/projects/LABINM_Robotics_Automation/Plantinator_IA_app/IAcore/models/TekvotHub/classifiers')
sys.path.append('/home/pqbas/projects/LABINM_Robotics_Automation/Plantinator_IA_app/IAcore/models/TekvotHub/classifiers/SeedlingsNet')

import cv2
import torch
from TekvotHub.detector import Detector
from TekvotHub.classifier import Classifier
import matplotlib.pyplot as plt
from TekvotHub.classifiers.SeedlingsNet.dataset_builder import getFeatures


class model4horizontalimage:
    def __init__(self):
        self.model = Detector(name='yolo7', # eg: 'yolov7' 'maskrcnn'
                              weights='TekvotHub/detectors/yolov7/weights/yolov7-hseed.pt', 
                              data='TekvotHub/weights/opt.yaml', 
                              device='cuda:0')
        
    def inference(self, image):
        return getFeatures(self.model, image)


class model4verticalimage:
    def __init__(self):
        self.model = Detector(name='yolo7', # eg: 'yolov7' 'maskrcnn'
                              weights='TekvotHub/detectors/yolov7/weights/yolov7-vseed.pt', 
                              data='TekvotHub/weights/opt.yaml', 
                              device='cuda:0')  

    def inference(self,image,depth):
        ret, thresh1 = cv2.threshold(depth, 120, 255, cv2.THRESH_BINARY)
        image = cv2.bitwise_and(image,image,mask = thresh1)
        return getFeatures(self.model, image)


class model4classification:
    def __init__(self):
        self.model = Classifier(name='seedlingsnet_mlp_classifier',
                           weights='TekvotHub/classifiers/SeedlingsNet/weights/seedlingnet_classifier_MLP.pt',
                           device='cuda')
        
    def inference(self, features):
        """
        True: Good seedling
        False: Not good seedling
        """
        return True if self.model.inference(features).item() else False


if __name__=='__main__':

    # This is how to use the models
    horizontal_image = plt.imread('gallery/horizontal/rgb/seedlings_1_4.jpg')
    model4horizontalimage_ = model4horizontalimage()
    horizontal_features = model4horizontalimage_.inference(horizontal_image)


    vertical_image = plt.imread('gallery/vertical/rgb/seedlings_1_4.jpg')
    depth = plt.imread('gallery/vertical/depth/seedlings_1_4.jpg')
    model4verticalimage_ = model4verticalimage()
    vertical_features = model4verticalimage_.inference(vertical_image, depth)


    classifier = model4classification()

    if horizontal_features is not None and vertical_features is not None:
        h1 = vertical_features["normalized"][0]
        w1 = vertical_features["normalized"][1]
        a1 = vertical_features["normalized"][2]
        h2 = horizontal_features["normalized"][0]
        w2 = horizontal_features["normalized"][1]
        a2 = horizontal_features["normalized"][2]
        features = torch.tensor([[a1, h1, w1, a2, h2, w2]]).float()
        quality_predicted = 'Good' if classifier.inference(features) else 'Not good'

    print(quality_predicted)



# cv2.imwrite(f"{path}/horizontal/mask/seedlings_mask_{j}_{i}.jpg", mask_h*255)
# cv2.imwrite(f"{path}/vertical/mask/seedlings_mask_{j}_{i}.jpg", mask_v*255)
# vertical_mask_paths.append(f"{path}/vertical/mask/seedlings_mask_{j}_{i}.jpg")
# horizontal_mask_paths.append(f"{path}/horizontal/mask/seedlings_mask_{j}_{i}.jpg")
# quality.append(quality_status)
# img = cv2.imread('TekvotHub/detectors/gallery/seedlings0.jpg')
# predictions = detector.predict(img)
# for pred in predictions:
#     x1, y1, x2, y2 = pred.bbox
#     cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0,255,0), 2)
