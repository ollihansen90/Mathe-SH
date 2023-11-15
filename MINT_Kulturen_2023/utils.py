import torch
import torch.nn as nn
import torch.nn.functional as F

import matplotlib.pyplot as plt
import numpy as np

class CNN(nn.Module):
    def __init__(self):
        super().__init__()

        feature_maps_1 = 16
        feature_maps_2 = 32
        
        num_classes = 13
        
        # TODO: initialize the child-modules
        self.conv1 = torch.nn.Conv2d(1, feature_maps_1, 5)
        self.conv2 = torch.nn.Conv2d(feature_maps_1, feature_maps_2, 5)

        self.fully_connected = torch.nn.Linear(4*4*feature_maps_2, num_classes)

    def forward(self, x):
        # TODO: apply the modules and functions
        feature_map_1_pre_activations = self.conv1(x)
        feature_map_1_pre_pooling = F.max_pool2d(feature_map_1_pre_activations, 2)
        feature_map_1_post_pooling = F.relu(feature_map_1_pre_pooling)

        feature_map_2_pre_activations = self.conv2(feature_map_1_post_pooling)
        feature_map_2_pre_pooling = F.max_pool2d(feature_map_2_pre_activations, 2)
        feature_map_2_post_pooling = F.relu(feature_map_2_pre_pooling)
        
        # TODO: apply the final linear layer to get the class scores
        feature_map_2_flattened = feature_map_2_post_pooling.flatten(start_dim=1)
        #print(feature_map_2_flattened.shape)
        predictions_pre_softmax = self.fully_connected(feature_map_2_flattened)
        
        return predictions_pre_softmax