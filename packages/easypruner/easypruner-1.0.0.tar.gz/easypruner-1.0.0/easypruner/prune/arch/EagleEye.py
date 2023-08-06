from ...utils.flops_counter import get_model_complexity_info
import torch
import torch.nn as nn
from ..utils import get_mask_layers, pruning_model_by_mask
import os
import numpy as np
import collections
import copy
import os.path
class EagleEye(object):
    def __init__(self, opt):
        #assert 输入参数是否有问题
        self.model = opt.model
        self.input_shape = opt.input_shape
        self.flops , self.parameter = get_model_complexity_info ( self.model , ( opt.input_shape ) , print_per_layer_stat=False )
        self.flag = 'flops'
        self.criterion = opt.prune_criterion
        self.save_flops = opt.prune_save_flops
        self.norm_layer_names = opt.norm_layer_names
        self.prec_layers = opt.prec_layers
        self.succ_layers = opt.succ_layers
        self.max_rate = opt.EagleEye_max_rate     
        self.min_rate = opt.EagleEye_min_rate       
        self.eval = opt.eval
        self.Adaptive_BN = opt.Adaptive_BN
        self.eval_args = opt.args
        self.weight = opt.model.state_dict()
        ###### create the search txt
        self.search_result_path = os.path.join( opt.workdir, opt.exp_name+ '_'+str(self.save_flops)+'flops.txt')
        self.serach_file= None 
        self.search_nums = opt.EagleEye_search_nums
    
        ##run完后结果存在这里
        self.result = {}
    
        ##Adaptive_BN
        self.dataloader_train = opt.dataloader_train

        self.channel_numbers = {}
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
        ################################################################################################################################# process the file
        #write the  layername in order
        if not os.path.isfile( self.search_result_path):
            self.serach_file= open( self.search_result_path , "w")
            for names  in self.norm_layer_names:
                self.serach_file.write("{}".format(names[0]) )
                for i in names[1:]:
                    self.serach_file.write(",{}".format(i) )
                self.serach_file.write(" ")
            self.serach_file.write("\n")
            self.serach_file.close() 
        self.serach_file= open( self.search_result_path , "r")
        lines = self.serach_file.readlines()  # 读取所有行
        len_results = len(lines)
        channel_number_dict = collections.OrderedDict()
        names_ = [  [j  for j in i.split(',')]    for i in lines[0].split( )] 
        assert set( [ i[0]  for i in names_] ) ==set( [ i[0]  for i in self.norm_layer_names] ) , "the layernames in file dont match the self.norm_layer_names"
        self.norm_layer_names = names_ 
        self.serach_file.close()
        ############################################################################################################################## pruning process
        while(len_results < 1+self.search_nums ):
            #########################search pruning strategy 
            channel_config = np.random.rand(len(self.norm_layer_names))
            channel_config = channel_config * self.max_rate
            channel_config = channel_config + self.min_rate
            channel_config = np.ones(len(self.norm_layer_names)) - channel_config
            pruning_strategy =channel_config.tolist() 
            #############################pruning model and judge the flop
            channel_savenumber_dict = {}
            for name, ratio  in zip(self.norm_layer_names , pruning_strategy):
                channel_savenumber_dict[name[0]] = int(ratio *self.channel_numbers[ name[0] ])
            #import pdb;pdb.set_trace()
            #print(pruning_strategy)
            net = copy.deepcopy(self.model)
            pruning_mask = get_mask_layers(self.model, self.criterion, channel_savenumber_dict ,self.norm_layer_names )
            try:
                net = pruning_model_by_mask( net  , pruning_mask , self.norm_layer_names , self.prec_layers , self.succ_layers)
            except:
                del net
                continue
            flops_pruned , parameter_pruned  =  get_model_complexity_info(net, ( self.input_shape ) , print_per_layer_stat=False )
            if self.flag == 'flops':
                flops_ = flops_pruned  / self.flops * 100
                print('flops:',flops_)
                if abs(flops_ - self.save_flops * 100) > 1:
                    del net 
                    continue
            elif self.flag == 'params':
                param_ = parameter_pruned  / self.parameter * 100
                print('param:',param_)
                if abs(param_ - self.save_flops * 100) > 1:
                    del net 
                    continue
            #########################################Adaptive BN
            self.Adaptive_BN(net,  self.need_dict)
            #########################################Test and record the pruning results
            strategy_score = self.eval(net,  self.need_dict)
            self.serach_file= open( self.search_result_path , "a+")
            self.serach_file.write("{} {} {} ".format(strategy_score, flops_ , param_))
            for item in pruning_strategy:
                self.serach_file.write("{} ".format(str(item)))
            self.serach_file.write("\n")
            self.serach_file.close()
            print("Eval Score:{}".format(strategy_score))

            # the result of searching add one
            del net  
            len_results +=1
        
        ####################################################################################################### Complete the search and select the best results
        self.get_best()


    #def Adaptive_BN(self, net , batchs =100,dataloader_train):
    #     from torch.autograd import Variable
    #     net.train()
    #     with torch.no_grad():
    #         for batch_index, (images, labels) in enumerate(self.dataloader_train ):
    #                 images = Variable(images)
    #                 _ = net(images)
    #                 if batch_index > batchs :
    #                     break
         
    
    def get_best(self):
        self.serach_file= open( self.search_result_path , "r")
        lines = self.serach_file.readlines()[1:]
        best_acc = 0.000000000
        best_index = 0
        for index, strings  in enumerate(lines):
            acc =  float(strings.strip().split()[0])
            if best_acc < acc :
                best_index = index
                best_acc = acc
        print('pruning_strategy_id:',best_index,'\npruning_strategy:',lines[best_index])
        pruning_strategy = [ float(i) for i in lines[best_index].split() ]
        channel_savenumber_dict = {}
        for name, ratio  in zip(self.norm_layer_names , pruning_strategy[2:]):
                channel_savenumber_dict[name[0]] = int( ratio * self.channel_numbers[ name[0] ])
        self.result = channel_savenumber_dict
        self.serach_file.close()
























