import torch
import torch.nn as nn
from ...utils.rebuild import rebuild
from ...utils.judge import is_transposed

__all__ = ["get_pruning_mask", "pruning_model_by_mask"]


def get_pruning_mask(opt ,channel_savenumber_dict ):
    #opt.model, opt.prune_criterion ,channel_number_dict ,  opt.norm_layer_names, opt.prec_layers ,  opt.use_conv_statistics
    model = opt.model 
    criterion = opt.prune_criterion 
    norm_layer_names = opt.norm_layer_names
    prec_layers = opt.prec_layers 
    use_conv_statistics = opt.use_conv_statistics
 
    if use_conv_statistics:
        channel_savenumber_dict_ = {}
        for norm_layer_name , prec_layer in zip( norm_layer_names , prec_layers ):
            channel_savenumber_dict_[ prec_layer[0]] = channel_savenumber_dict[  norm_layer_name[0]]
        pruning_mask_ = get_mask_layers_conv(model, criterion, channel_savenumber_dict_ , prec_layers  )
        pruning_mask = {}
        for norm_layer_name , prec_layer in zip( norm_layer_names , prec_layers ):
            pruning_mask[ norm_layer_name[0]] = pruning_mask_[ prec_layer[0]]
    else:
        pruning_mask = get_mask_layers(model, criterion, channel_savenumber_dict ,  norm_layer_names)
    return pruning_mask

    

def get_mask_layers_conv(model, criterion, channel_savenumber_dict , pruned_names ):
    pass
    """
    Binary search to find the appropriate pruning rate.
        self.result get the channel_savenumber_dict 
    """
    pruning_mask = {}
    weights  = model.state_dict()
    for lid, names in enumerate(pruned_names):
        name = names[0]
        save_number  =  channel_savenumber_dict[name]
        weight = weights[name + '.weight'] #residual connecation choose the first layer// stride=2 layer
        scores = []
        if  is_transposed( model , name ): 
            scores = criterion( weight , 1 )
        else:
            scores = criterion( weight , 0 )
        scores_ = scores.copy()
        scores_.sort(reverse=True)
        if save_number == len(scores):
            threshold = scores_[save_number-1]-1
        else:
            threshold = scores_[save_number]
        pruning_mask[name]  = (torch.tensor(scores) >threshold).bool()
        if pruning_mask[name].sum() ==0 :
            pruning_mask[name]  =( torch.tensor(scores) == scores[0]    ).bool()
    return pruning_mask
    

def get_mask_layers(model, criterion, channel_savenumber_dict , pruned_names  ):
    """Binary search to find the appropriate pruning rate.
        self.result get the channel_savenumber_dict 
    """

    pruning_mask = {}
    weights  = model.state_dict()
    for names in pruned_names:
        name = names[0]
        save_number  =  channel_savenumber_dict[name]
        weight = weights[name + '.weight'] #residual connecation choose the first layer// stride=2 layer
        scores = []
        if  'transpose' in name  or 'Transpose' in  name  : 
            scores = criterion( weight , 1 )
        else:
            scores = criterion( weight , 0 )
        scores_ = scores.copy()
        scores_.sort(reverse=True)
        if save_number == len(scores):
            threshold = scores_[save_number-1]-1
        else:
            threshold = scores_[save_number]
        pruning_mask[name]  = (torch.tensor(scores) >threshold).bool()
        if pruning_mask[name].sum() ==0:
            pruning_mask[name]  =( torch.tensor(scores) == scores[0]    ).bool()
    return pruning_mask



def pruning_model_by_mask( model , pruning_mask  , norm_layer_names, prec_layers, succ_layers):###暂时只能用BN剪枝
    """prune the model by the mask.
    Args:
        model: the torch net to be pruned.
        pruning mask :
    Returns:
        pruned model
    """
    
    WEIGHT_POSTFIX = '.weight'
    IN_CHANNEL_DIM = 1
    OUT_CHANNEL_DIM =0
    BIAS_POSTFIX = ".bias"
    MIN_CHANNELS = 2

    def group_weight_names(weight_names):
        grouped_names = {}
        for weight_name in weight_names:
            group_name = '.'.join(weight_name.split('.')[:-1])
            if group_name not in grouped_names:
                grouped_names[group_name] = [weight_name, ]
            else:
                grouped_names[group_name].append(weight_name)
        return grouped_names

    weights=model.state_dict()

    grouped_weight_names = group_weight_names(weights.keys())
 
    depthwise_mask={}
    norm_layer_names_ = norm_layer_names.copy()
 

    for id,norm_layer_name in enumerate(norm_layer_names):

        #norm_layer_name is list
        #取出mask
        prune_mask = pruning_mask[norm_layer_name[0]].byte()
        prune_indices = torch.nonzero(prune_mask).flatten()#nonzero得到数组中非零值的坐标


        for name in prec_layers[id]:
            if name in depthwise_mask.keys():
                prune_mask = depthwise_mask[name][1]
                prune_indices = depthwise_mask[name][0]
                break
        

        # 1. prune source normalization layer，先剪掉剪掉源层（BN）
        for name  in norm_layer_name:
            for weight_name in grouped_weight_names[name]:
                weights[weight_name] = weights[weight_name].masked_select(prune_mask)
        # 2. prune target succeeding conv/linear/... layers     剪掉源层（BN）后继层的（输入通道）
        for prune_layer_name in succ_layers[id]:   #遍历后继
            for weight_name in grouped_weight_names[prune_layer_name]: #遍历后继的各层(如bn层的 weights ，bias ，meaning ，var)
                if weight_name.endswith(WEIGHT_POSTFIX):#endswith以“.weight”结尾
                    transpose_flag = is_transposed(model,weight_name)
                    if (weights[weight_name].size(IN_CHANNEL_DIM) == 1):#deepwise卷积，剪枝掩码存入字典
                        depthwise_mask[prune_layer_name]=[prune_indices , prune_mask]
                        continue
                    if transpose_flag:#反卷积
                        if weights[weight_name].shape[  OUT_CHANNEL_DIM  ] != len( prune_mask  ):
                            #import pdb;pdb.set_trace()
                            factor_ = weights[weight_name].shape[  OUT_CHANNEL_DIM  ] // len( prune_mask  )
                            prune_mask_ = prune_mask.view(-1,1 )
                            prune_mask_ = prune_mask_.repeat( 1  , factor_ ).view(-1)
                            prune_indices_ = torch.nonzero(prune_mask_).flatten()
                            weights[weight_name] = weights[weight_name].index_select(OUT_CHANNEL_DIM, prune_indices_)#剪输入通道
                        else: 
                            weights[weight_name] = weights[weight_name].index_select(OUT_CHANNEL_DIM, prune_indices)#剪输入通道
                    else:#正常卷积
                        if weights[weight_name].shape[  IN_CHANNEL_DIM  ] != len( prune_mask  ):
                            #import pdb;pdb.set_trace()
                            factor_ = weights[weight_name].shape[  IN_CHANNEL_DIM  ] // len( prune_mask  )
                            prune_mask_ = prune_mask.view(-1,1 )
                            prune_mask_ = prune_mask_.repeat( 1  , factor_ ).view(-1)
                            prune_indices_ = torch.nonzero(prune_mask_).flatten()
                            weights[weight_name] = weights[weight_name].index_select(IN_CHANNEL_DIM, prune_indices_)#剪输入通道
                        else:
                            weights[weight_name] = weights[weight_name].index_select(IN_CHANNEL_DIM, prune_indices)#剪输入通道
                    
        # 3. prune target preceding conv/linear/... layers    #剪掉源层（BN）前继层的（输入通道）也就是该modules的卷积
        for prune_layer_name in prec_layers[id]: #同上
            for weight_name in grouped_weight_names[prune_layer_name]:#同上
                if weight_name.endswith(WEIGHT_POSTFIX):#endswith以“.weight”结尾
                    transpose_flag = is_transposed(model,weight_name)
                    if transpose_flag:#反卷积
                        weights[weight_name] = weights[weight_name].index_select(IN_CHANNEL_DIM, prune_indices)#剪输出通道
                    else:#正常卷积
                        weights[weight_name] = weights[weight_name].index_select(OUT_CHANNEL_DIM, prune_indices)#剪输出通道
                elif weight_name.endswith(BIAS_POSTFIX):#endswith以“.bias”结尾
                    weights[weight_name] = weights[weight_name].index_select(0, prune_indices)#剪输出通道

    pruned_model = rebuild(model, weights)
    return pruned_model
