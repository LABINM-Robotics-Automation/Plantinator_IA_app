import sys
import warnings
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, 'classifiers')
sys.path.insert(2, 'classifiers/SeedlingsNet/models')

# from detectors.maskrcnn import MaskRCNN
from classifiers import seedlingsnet_mlp_classifier
import cv2
import torch


class Classifier:
    def __init__(self, name, weights, device):

        print("Classifier in building............!!!")

        self.model = None

        # '''''''''' Warning: NoneType variable '''''''''''
        if name is None:
            warnings.warn('name is a NoneType object')
            return

        # '''''''''''''''''' MLP '''''''''''''''''''
        elif name == 'seedlingsnet_mlp_classifier':
            self.model = seedlingsnet_mlp_classifier.model(
                weights=weights,
                device=device)

        # '''''''''' Not available model '''''''''''
        else:
            warnings.warn('Model is not in available')
            return


    def inference(self, input):
        if self.model is None:
            warnings.warn('self.Model is a NoneType object, please select an available model')
            return
        
        predictions = self.model.predict(input)
        return predictions
    

if __name__ == '__main__':
    classifier = Classifier(name='seedlingsnet_mlp_classifier',
                            weights='./classifiers/SeedlingsNet/weights/seedlingnet_classifier_MLP.pt',
                            device='cuda')
    x = torch.randn([1,6])
    y = classifier.inference(x)
    print(y)

