import numpy
import torch
from ...utils.judge import is_transposed 
__all__ = [  'OT_threshold'   ]
MIN_SCALING_FACTOR = 1e-18
OT_DISCARD_PERCENT = 0.0001
OUT_CHANNEL_DIM = 0
IN_CHANNEL_DIM = 1
WEIGHT_POSTFIX = ".weight"
BIAS_POSTFIX = ".bias"
MIN_CHANNELS = 1
OT_DISCARD_PERCENT = 1e-4
def OT_threshold(x, percent=OT_DISCARD_PERCENT):
    x_np = numpy.array(x)
    x_np[x_np < MIN_SCALING_FACTOR] = MIN_SCALING_FACTOR
    x_sorted = numpy.sort(x_np)
    #print("\n max:",x_sorted[-1])
    #print("\n",torch.from_numpy(x_sorted))
    if x_sorted[-1] <1e-3 :# no bigger peak, all channels have been sparsed , prune all
        th = 1
    elif x_sorted[-1] < x_sorted[0]*20  and x_sorted[-1] > 1e-3 :   #no smaller peak, all the channels are important,none will be pruned
        th = 0
    else:
        x2 = x_sorted**2
        Z = x2.sum()
        energy_loss = 0
        for i in range(x2.size):
            energy_loss += x2[i]
            if energy_loss / Z > percent:
                break
        th = (x_sorted[i-1] + x_sorted[i]) / 2 if i > 0 else 0
    return th


def get_mask_threshold(model, prune_factor , criterion , pruned_names, threshold_method = 'Order' ):
    """Get the pruning mask by criterion and method of threshold selecting.
    
    Args:
        model: the torch net to be pruned.
        prune_factor(float): the factor needed by threshold_mold
        criterion(str):  the importance criterion.
                   ['L1','L2','FPGM']
        threshold_method(str): method of threshold selecting.
                   ['order' , 'ratio' ,'OT']
                    1. order: direct order the threshold
                    2. ratio: getting threshold by channel saved ratio and global ranking channel 
                    3. OT: Optimal threshold method

    Returns:
        pruning_mask(dict): the pruning mask ,Like { 'layer1.bn':torch.Tensor([True,False,False,True,...]) , ....}
    """


  
    weights  = model.state_dict()
    scores_dict = {}
    for names in pruned_names :
        if  is_transposed(model, names[0]):
            scores_dict[names[0]] = criterion(weights[names[0]+WEIGHT_POSTFIX] , IN_CHANNEL_DIM )
        else :
            scores_dict[names[0]] = criterion(weights[names[0]+WEIGHT_POSTFIX] , OUT_CHANNEL_DIM )

    if threshold_method == 'Ratio':
        saved_numbers_dict = ratio_threshold_prune(  scores_dict,  prune_factor , criterion  )
    elif threshold_method == 'Order':
        saved_numbers_dict = order_threshold_prune( scores_dict , prune_factor , criterion )
    elif threshold_method == 'OT':
        saved_numbers_dict = ot_threshold_prune( scores_dict , prune_factor , criterion  )
    return saved_numbers_dict


def  ratio_threshold_prune( scores_dict, prune_factor , criterion  ):
    saved_numbers_dict = {}
    scores_list = []
    for name in scores_dict:
        scores_list += scores_dict[name]
    save_number = int( prune_factor * len( scores_list ))
    scores_list.sort(reverse=True)
    threshold =  scores_list[save_number]

    for name in scores_dict:
        scores = scores_dict[name]
        saved_numbers_dict[name] = (torch.tensor(scores) >threshold).sum()

    return saved_numbers_dict


def  order_threshold_prune( scores_dict, prune_factor , criterion  ):
    threshold = prune_factor
    saved_numbers_dict = {}
    for name in scores_dict:
        scores = scores_dict[name]
        saved_numbers_dict[name] = (torch.tensor(scores) >threshold).sum()
 
    return saved_numbers_dict  

def  ot_threshold_prune( scores_dict, prune_factor , criterion ):
    saved_numbers_dict = {}

    for name in scores_dict:
        scores = scores_dict[name]
        threshold = OT_threshold(scores.copy() , prune_factor)
        saved_numbers_dict[name] = (torch.tensor(scores) >threshold).sum()

    return saved_numbers_dict




