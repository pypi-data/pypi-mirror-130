import logging
import numpy as np
import torch 
#from ..common import get_logger
#from ..core import Registry, GraphWrapper

__all__ = ["l1_norm", "l2_norm","geometry_median"]

#_logger = get_logger(__name__, level=logging.INFO)

#CRITERION = Registry('criterion')





#@CRITERION.register
def l1_norm(weights, axis = 0):
    """Compute l1-norm scores of parameter on given axis.
    This function return a list of parameters' l1-norm scores on given axis.

    Each element of list is a tuple with format (name, axis, score) in which 'name' is parameter's name
    and 'axis' is the axis reducing on and `score` is a np.array storing the l1-norm of strucure on `axis`.
    
    Args:
        weights(): A group of parameters. the wights of BN layers / conv layers / deconv layers
        axis(int): axis is the axis of calculating scores. BN layers
        L1 :   Σabs(all)
    Returns:
       list: A list of tuple l1-norm on given axis.
    """
    assert axis < len(weights.shape)
    scores = []
    
    for i in range(weights.shape[axis]):
        weight =  (weights.index_select(axis, torch.tensor([i])).abs()).sum()
        scores.append(weight.item())

    return scores






#@CRITERION.register
def l2_norm(weights, axis = 0):
    """Compute l1-norm scores of parameter on given axis.
    This function return a list of parameters' l2-norm scores on given axis.

    Each element of list is a tuple with format (name, axis, score) in which 'name' is parameter's name
    and 'axis' is the axis reducing on and `score` is a np.array storing the l2-norm of strucure on `axis`.
    
    Args:
        weights(): A group of parameters. the wights of BN layers / conv layers / deconv layers
        axis(int): axis is the axis of calculating scores. BN layers
        L2 :   sqrt（Σ all**2 ）
    Returns:
       list: A list of tuple l1-norm on given axis.
    """
    assert axis < len(weights.shape)

    scores = []
    
    for i in range(weights.shape[axis]):
        weight =  (weights.index_select(axis, torch.tensor([i])).pow(2)).sum()
        weight = weight.sqrt()
        scores.append(weight.item())

    return scores





#@CRITERION.register
def geometry_median(weights, axis = 0 ):
    assert axis < len(weights.shape)
    
    scores = []
    dim_che = list(range(len(weights.shape)))
    dim_che[axis] = 0
    dim_che[0] = axis

    def get_distance_sum(weights, index, axis):
        weights_ = weights.clone()
        selected_filter = weights_.index_select(axis, torch.tensor([i])).permute(dim_che).reshape(1,-1).repeat( weights_.shape[axis] ,1 )
        weights_ = weights_.permute(dim_che).reshape(weights_.shape[axis] ,-1 )
        x = weights_ - selected_filter
        x = (x*x).sum(1).sqrt()
        return x.sum()

    dist_sum_list = []
    for i in range(weights.shape[axis]):
        score = get_distance_sum(weights, i, axis)
        scores.append(score)

    return scores




