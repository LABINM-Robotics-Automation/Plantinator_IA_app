import torch
import sys

sys.path.insert(1, 'SeedlingsNet')
from SeedlingsNet.models import MLP_classifier

import matplotlib.pyplot as plt
import numpy as np
import cv2
import numpy as np
import os

class model:
    def __init__(self, weights, device):
        # parameters of the model (definition, weights, device)
        self.weights = weights
        self.model = MLP_classifier.model(in_features=6)
        self.model.load_state_dict(torch.load(weights))
        self.model.to(device)
        self.device = device
    
    def predict(self, x):
        x = x.to(self.device)
        with torch.no_grad():
            x = self.model(x)
            return x

if __name__=='__main__':
    classifier = model(weights='SeedlingsNet/weights/seedlingnet_classifier_MLP.pt', 
                       device='cpu')