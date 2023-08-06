# train.py
#!/usr/bin/env	python3

""" train network using pytorch

author baiyu
"""

import os
import sys
import argparse
from datetime import datetime

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

from torch.utils.data import DataLoader
#from dataset import *
from torch.autograd import Variable

#from tensorboardX import SummaryWriter
import numpy as np
from .judge import is_number , get_module

MIN_SCALING_FACTOR = 1e-18
OT_DISCARD_PERCENT = 0.0001
OUT_CHANNEL_DIM = 0
IN_CHANNEL_DIM = 1
WEIGHT_POSTFIX = ".weight"
BIAS_POSTFIX = ".bias"
MIN_CHANNELS = 1


def load_pruned_model(model, pruned_weights, prefix='', load_pruned_weights=True, inplace=True):
    """load pruned weights to a unpruned model instance

    Arguments:
        model (pytorch model): the model instance
        pruned_weights (OrderedDict): pruned weights
        prefix (string optional): prefix (if has) of pruned weights
        load_pruned_weights (bool optional): load pruned weights to model according to the ICLR 2019 paper:
            "Rethinking the Value of Network Pruning", without finetuning, the model may achieve comparable or even
            better results
        inplace (bool, optional): if return a copy of the model

    Returns:
        a model instance with pruned structure (and weights if load_pruned_weights==True)
    """
    
    def _dirty_fix(module, param_name, pruned_shape):
        module_param = getattr(module, param_name)
        # identify the dimension to prune
        pruned_dim = 0
        for original_size, pruned_size in zip(module_param.shape, pruned_shape):
            if original_size != pruned_size:
                keep_indices = torch.LongTensor(range(pruned_size)).to(module_param.data.device)
                module_param.data = module_param.data.index_select(pruned_dim, keep_indices)
  
                # modify number of features/channels
                if param_name == "weight":
                    if isinstance(module, nn.modules.batchnorm._BatchNorm) or \
                            isinstance(module, nn.modules.instancenorm._InstanceNorm) or \
                            isinstance(module, nn.GroupNorm):
                        module.num_features = pruned_size
                    elif isinstance(module, nn.modules.conv._ConvNd):
                        if pruned_dim == OUT_CHANNEL_DIM:
                            module.out_channels = pruned_size
                        elif pruned_dim == IN_CHANNEL_DIM:
                            module.in_channels = pruned_size
                    elif isinstance(module, nn.Linear):
                        if pruned_dim == OUT_CHANNEL_DIM:
                            module.out_features = pruned_size
                        elif pruned_dim == IN_CHANNEL_DIM:
                            module.in_features = pruned_size
                    else:
                        pass
            pruned_dim += 1
    model_weight_names = model.state_dict().keys()
    pruned_weight_names = pruned_weights.keys()
    # check if module names match
    #assert set([prefix + _ for _ in model_weight_names]) == set(pruned_weight_names) , print (set([prefix + _ for _ in model_weight_names])  ,"\n\n\n", set(pruned_weight_names)) 
    
    #scratch:   ~    stem  
    #test :    stem  stem

    # inplace or return a new copy
    if not inplace:
        pruned_model = copy.deepcopy(model)
    else:
        pruned_model = model

    # update modules with mis-matched weight
    model_weights = pruned_model.state_dict()
    for model_weight_name in model_weight_names:
       # print(model_weight_name,":(",model_weights[model_weight_name].shape ,pruned_weights[prefix + model_weight_name].shape,")")
        if model_weights[model_weight_name].shape != pruned_weights[prefix + model_weight_name].shape:
            # print("   ",model_weight_name," ",prefix + model_weight_name)
            *container_names, module_name, param_name = model_weight_name.split('.')
            container = model
            for container_name in container_names:
                container = container._modules[container_name]
            module = container._modules[module_name]
            _dirty_fix(module, param_name, pruned_weights[prefix + model_weight_name].shape)

    # print(pruned_model.state_dict()['conf.3.weight'].shape ,pruned_weights['conf.3.weight'].shape)
    if load_pruned_weights:
        pruned_model.load_state_dict({k: v for k, v in pruned_weights.items()})
    return pruned_model


    

def rebuild(net,new_state_dict,load_pruned_weights=True):
    depth_wise_flag = []
    for k,v in net.state_dict().items():
        if 'weight' in k and len(v.shape)==4 and v.shape[0]==1:
            depth_wise_flag.append(  k[:-7]  )


    weights_m = new_state_dict
    from collections import OrderedDict
    new_state_dict = OrderedDict()
    for k, v in weights_m.items():
        head = k[:7]
        if head == 'module.':
            name = k[7:] # remove `module.`
        else:
            name = k
        new_state_dict[name] = v
    net =  load_pruned_model(net, new_state_dict,load_pruned_weights=load_pruned_weights) #load_pruned_weights = scratch flag
   
    

    for k,v in net.state_dict().items():
        if(torch.tensor(torch.tensor(v.shape).shape).item()) != 4:
            continue
        module_name = '.'.join(  k.split('.')[:-1]   )    
        param_name = k.split('.')[-1]
        container = get_module( net  , module_name)        
        if container.groups !=1:
            container.groups      = v.shape[OUT_CHANNEL_DIM]
            container.in_channels = v.shape[OUT_CHANNEL_DIM]
            container.out_channels  = v.shape[OUT_CHANNEL_DIM]

    return net

