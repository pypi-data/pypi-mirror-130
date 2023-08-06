#from .arch import DDPG , EagleEye, Uniform, sensity_analysis
from .arch import Uniform , EagleEye
from .threshold import  get_mask_threshold
from ..utils.flops_counter import get_model_complexity_info
from ..utils.judge import is_transposed

from .utils import get_pruning_mask ,pruning_model_by_mask
import torch
import torch.nn as nn
from ..utils.rebuild import rebuild
import os 

__all__ = ['prune' ]

MIN_SCALING_FACTOR = 1e-18
OT_DISCARD_PERCENT = 0.0001
OUT_CHANNEL_DIM = 0
IN_CHANNEL_DIM = 1
WEIGHT_POSTFIX = ".weight"
BIAS_POSTFIX = ".bias"
MIN_CHANNELS = 1


def get_channel_numbers_arch(opt):
    """Get the Architecture of the pruned model by the method in the target flops.
    
    Args:
        model: the torch net to be pruned.
        method(str): the method of getting channel_config 
                ['DDPG' , 'EAgleEye', 'Uniform', 'seneity_analysis']
                1. sensity analysis method 
                2. uniform pruning
                3. DDPG
                4. EagleEye
        flops_ratio(float):  the flops target of the pruned model.
    Returns:
        channel_number_dict(dict): A dict of chennel numbers of every layer. Like { 'layer1.bn':2 , 'layer1.bn1':7 ,.....}
    """
    #定义agent
    #if method =='DDPG':
    #    agent = DDPG(opt)
    if opt.prune_method =='EagleEye':
        agent = EagleEye(opt)
    elif opt.prune_method =='Uniform':
        agent = Uniform(opt)
    #elif method =='Sensity_analysis':
    #    agent = Sensity_analysis(opt)
    agent.run()
   
    return agent.result

def  get_channel_numbers_threshold(opt):
    """Get the Architecture of the pruned model by the method in the threshold.
    
    Args:
        model: the torch net to be pruned.
        method(str): the method of getting channel_config 
                ['Order' , 'Ratio', 'OT']
        flops_ratio(float):  the flops target of the pruned model.
    Returns:
        channel_number_dict(dict): A dict of chennel numbers of every layer. Like { 'layer1.bn':2 , 'layer1.bn1':7 ,.....}
    """
    if opt.use_conv_statistics:
        pruned_names = opt.prec_layers
    else:
        pruned_names =  opt.norm_layer_names

    assert opt.prune_factor is not None, 'prune_factor is None!'
    channel_savenumber_dict_ = get_mask_threshold(opt.model, prune_factor = opt.prune_factor, criterion = opt.prune_criterion, pruned_names = pruned_names, threshold_method = opt.prune_method)
    
    channel_savenumber_dict = {}
    if opt.use_conv_statistics:
        for prec_name, norm_name in zip( opt.prec_layers , opt.norm_layer_names ):
            channel_savenumber_dict[ norm_name[0]   ] = channel_savenumber_dict_[ prec_name[0]  ]
    else:
        channel_savenumber_dict = channel_savenumber_dict_ 
    return  channel_savenumber_dict

def get_mask_model(opt):#接口函数
    """Get the pruning mask by the order algorithm(option).
    Args:
        model: the torch net to be pruned.
        opt: pruner config dict
    Returns:
        pruning_mask(dict): the pruning mask ,Like { 'layer1.bn':torch.Tensor([True,False,False,True,...]) , ....}
    """
    assert opt.prune_method in ['DDPG' , 'EagleEye', 'Uniform', 'Seneity_analysis', 'Order', 'Ratio', 'OT'], opt.prune_method + ' is not in  [\'DDPG\' , \'EagleEye\', \'Uniform\', \'seneity_analysis\', \'order\', \'ratio\', \'OT\'] '

    if opt.prune_method in ['DDPG' , 'EagleEye', 'Uniform', 'Seneity_analysis']:
        channel_savenumber_dict = get_channel_numbers_arch(opt)                    
    elif opt.prune_method in ['Order', 'Ratio', 'OT']:
        channel_savenumber_dict =  get_channel_numbers_threshold(opt)

    pruning_mask = get_pruning_mask(opt , channel_savenumber_dict )
    return pruning_mask
 

def prune( opt):
    #获取剪枝mask
    if opt.prune_mask is None:
        opt.prune_mask = get_mask_model(opt)

    #mask剪枝
    opt.model =  pruning_model_by_mask(  opt.model , opt.prune_mask  ,  opt.norm_layer_names,  opt.prec_layers,  opt.succ_layers)
    
    #update pruning state
    import copy
    opt.pruned = False
    opt.prunedmodel_flops ,opt.prunedmodel_params = get_model_complexity_info( copy.deepcopy(opt.model) , ( opt.input_shape ) , print_per_layer_stat=False )
    opt.real_prune_save_flops = opt.prunedmodel_flops /opt.flops
    
    #保存mask
    torch.save(opt.prune_mask , os.path.join( opt.workdir, opt.exp_name+'_'+ ( "%.2f" % opt.real_prune_save_flops) +'_flops.mask'))
    #保存权重
    torch.save(opt.model.state_dict() , os.path.join( opt.workdir, opt.exp_name+'_'+ ( "%.2f" % opt.real_prune_save_flops) +'_flops.pth'))


