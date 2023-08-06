from ...utils.flops_counter import get_model_complexity_info
import torch
import torch.nn as nn
from ..utils import get_pruning_mask, pruning_model_by_mask


class Uniform(object):
    def __init__(self, opt):
        #assert 输入参数是否有问题
        #
        self.model = opt.model
        self.input_shape = opt.input_shape
        import copy
        self.flops , self.parameter = get_model_complexity_info ( copy.deepcopy(self.model) , ( opt.input_shape ) , print_per_layer_stat=False )
        self.criterion = opt.prune_criterion
        self.save_flops = opt.prune_save_flops
        self.norm_layer_names = opt.norm_layer_names
        self.prec_layers = opt.prec_layers
        self.succ_layers = opt.succ_layers
        #self.source = {}
        self.weight = opt.model.state_dict()
        self.result = {}#run完后结果存在这里
        self.channel_numbers = {}
        self.opt = opt
        #for node_list in norm_layer_names:  ##获取
        #    weight  = []
        #    for i in node_list：
        #        weight.append(self.weights[i])
        #    self.source[name] = self.criterion(weight[name]))
        for node_list in self.norm_layer_names:
            self.channel_numbers[node_list[0]] = len(self.weight[node_list[0]+'.weight'])

    def run(self):
        """Get the pruning mask by the chennel_number_dict and importance criterion.
            
            Args:
                model: the torch net to be pruned.
                channel_number_dict(dict): the chennel_number_dict get by the fun{get_channel_numbers}
                criterion(str):  the importance criterion.
                        ['L1','L2','FPGM']
            Returns:
                pruning_mask(dict): the pruning mask,Like { 'layer1.bn':torch.Tensor([True,False,False,True,...]) , ....}
        """
        def equal_(a,b):
            return abs(a-b) <1e-5
        #读取outdir结果 uniform不用
        #resume uniform不用
        #二分选择合适的flops
        ll = 0.01
        rr = 0.99
        exit_flops = 0
        exit_flag  = 0
        while True:
            #import pdb;pdb.set_trace()
            mid = (ll+rr)/2
            #准备mask
            channel_savenumber_dict = {}
            for name  in self.norm_layer_names:          
                channel_savenumber_dict[ name[0] ] = int(mid * self.channel_numbers[name[0]] )
            
            pruning_mask = get_pruning_mask(self.opt , channel_savenumber_dict  )
           
            #prune net
            import copy
            net = copy.deepcopy(self.model)
            net = pruning_model_by_mask(net, pruning_mask, self.norm_layer_names, self.prec_layers, self.succ_layers)
            flops_pruned , _  =  get_model_complexity_info(copy.deepcopy(net), ( self.input_shape ) , print_per_layer_stat=False )
            #test pruned_net flops
            flops_ = flops_pruned  / self.flops * 100
            print('flops:',flops_)
            assert not equal_(flops_ , 100.0) and not equal_(flops_, 100.0) , 'flops_ error, exit binary search cycle'
            if abs(flops_ - self.save_flops * 100) < 1:
                self.result = channel_savenumber_dict
                break
            elif flops_ < self.save_flops * 100  :
                del net 
                ll = mid
            else:
                del net 
                rr = mid
            print("ll:",ll, ", rr:",rr,  ", mid:",mid, ", flops:", flops_)
            if exit_flops != flops_:
                exit_flops = flops_
                exit_flag = 0
            else:
                exit_flag +=1
                if exit_flag ==2:
                    print('warning !!!  Pruning Hyperparameters are not suitable.')
                    exit()

