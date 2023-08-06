import os
from  .prune_algorithm import prune_finetune ,sparsity_prune_finetune, prune_op
from  .prune.importance import l1_norm,   l2_norm, geometry_median
from .utils.flops_counter import get_model_complexity_info
from .utils.judge import get_module 
import torch 

from .utils.get_prune_layer import get_prune_layers

class config(object):
    def __init__(self,exp_name, algorithm):
        #通用部分
        self.model = None #模型
        self.args = None #训练测试的参数
        self.train = None #train()函数              #### train(net,args)     return  None
        self.sparsity = None #sparsity()函数        #### sparsity(net,args)  return  None
        self.eval = None #eval()函数                #### eval(net,args)      return  acc_top1
        self.dataloader_train = None 
        self.dataloader_eval  = None  
        self.input_shape = None    #input_shape   (3,256,256)
        self.add_layer_need = True
        self.norm_layer_names = [] #(list)norm_layer_names:[ [namea] , [nameb] , [namec,named,..],..]
        self.prec_layers = []      #(dict)prec_layers { [name_a]:[name1] ,....[name_c,name_d]:[name_b,name_b,name_b1]      }
        self.succ_layers = []      #(dict)succ_layers { [name_a]:[name11],....[name_c,name_d];[name_b,name_b2,name_b3] } 
        self.prune_stride_2 = True  # 是否剪枝 stride为2的卷积层
        self.exp_name =exp_name  
        self.algorithm = algorithm #prune_algorithm_name
        self.workdir ='./workdir/'+exp_name
        if not os.path.exists(self.workdir) :
            os.makedirs(self.workdir)
        #pruning state
        self.pruned = False
        self.prunedmodel_flops = None
        self.prunedmodel_params = None
        self.real_prune_save_flops =None  
        #剪枝  
        self.prune_save_flops  = None    #save_flops float
        self.prune_factor  = None    # 阈值剪枝方法通道剪枝率
        self.prune_criterion   = None    #criterion()   importance函数
        self.axis = 1
        self.prune_mask = None   #剪枝算法
        if self.algorithm in ['Ratio','DDPG' , 'Order','EagleEye', 'Uniform', 'seneity_analysis']:
            self.prune_method  = self.algorithm  #剪枝mask
        else:
            self.prune_method = None 
        self.use_conv_statistics  = False # 默认False使用BN作为 importance
        self.dense_task = None
        #EagleEye
        self.EagleEye_search_nums= 1000
        self.EagleEye_max_rate = 0.7
        self.EagleEye_min_rate = 0.0
        self.Adaptive_BN = None 
        #稀疏部分
        self.sparsity_factor = 0   #稀疏因子
        self.sparsity_method = None#稀疏方法
        self.sparsity_mask = None  #None 是全局稀疏，mask限定稀疏范围
        self.sparsity_layernames =  []
 
        #finetune部分
        self.fientune_methhod = None #finetune算法
        #onnx_file 
        self.onnx_file = None

    def init(self):
        
        #get_prune_layers
        if len(self.norm_layer_names)==0  or len(self.prec_layers)==0  or  len(self.succ_layers)==0  :
            get_prune_layers(self)
        #get_importance
        if self.prune_criterion in ['L1' , 'l1' ]:
            self.prune_criterion = l1_norm
        elif self.prune_criterion in ['L2' , 'l2' ]:
            self.prune_criterion = l2_norm
        elif self.prune_criterion in ['FPGM' ]:
            self.prune_criterion = geometry_median

        #get_flops,params
        import copy  
        self.flops , self.params =   get_model_complexity_info( self.model , ( self.input_shape ) , print_per_layer_stat=False )

        #pruned_state
        self.pruned = False

        #pruned_mask
        if self.prune_mask:
            self.prune_mask = torch.load(self.prune_mask)
       
        #merge depthwise
        def get_index(name , name_list ):
            for index,  names  in enumerate( name_list ):
                if name in names:
                    return index 
        prec_layers_ = []
        norm_layer_names_ = []
        succ_layers_ = []
        continue_index = []
        for index,  conv_succlist in enumerate(self.succ_layers ):
            if index in continue_index:
                continue
            prec_layer = self.prec_layers[index].copy()
            norm_layer_name = self.norm_layer_names[index].copy()
            succ_layer = self.succ_layers[index].copy()
            for conv_name in conv_succlist :
                container = get_module(self.model , conv_name)
                if not  hasattr(container, 'groups') :
                    print(  conv_name ,"continue"  )
                    continue
                assert  hasattr(container, 'groups')
                assert  hasattr(container, 'out_channels')
                if container.groups ==container.out_channels:
                    index_ = get_index( conv_name , self.prec_layers )
                    #import pdb;pdb.set_trace()
                    continue_index.append( index_ )
                    prec_layer += self.prec_layers[index_]
                    norm_layer_name += self.norm_layer_names[index_]
                    succ_layer +=  self.succ_layers[index_]
            prec_layers_.append( prec_layer )
            norm_layer_names_.append( norm_layer_name )
            succ_layers_.append( succ_layer  )
                 
        self.prec_layers = prec_layers_
        self.norm_layer_names = norm_layer_names_
        self.succ_layers = succ_layers_
        
        #stride =2
        prec_layers_ = []
        norm_layer_names_ = []
        succ_layers_ = []
        if not self.prune_stride_2 :
            for index,convlist in enumerate( self.prec_layers ):
                flag = False
                for conv_name in convlist:
                    container = get_module(self.model , conv_name)
                    assert  hasattr(container, 'stride')
                    if container.stride==(2,2):
                        flag = True
                        break
                if flag:
                    continue
                else:
                    prec_layers_.append( self.prec_layers[index] )
                    norm_layer_names_.append(self.norm_layer_names[index])
                    succ_layers_.append( self.succ_layers[index])
            
            self.prec_layers = prec_layers_ 
            self.norm_layer_names = norm_layer_names_ 
            self.succ_layers = succ_layers_ 
        
        # groups != out_chanel 
        prec_layers_ = []
        norm_layer_names_ = []
        succ_layers_ = []
        for index,  conv_preclist  in enumerate(self.prec_layers ):
            flag = True
            conv_succlist = self.succ_layers[index]
            for conv_name in conv_succlist + conv_preclist:
                container = get_module(self.model , conv_name)
                if not  hasattr(container, 'groups') :
                    print(  conv_name ,"continue"  )
                    continue
                assert  hasattr(container, 'groups')
                assert  hasattr(container, 'out_channels')
                if container.groups !=1 and container.groups !=container.out_channels:
                    flag = False
                    print("Warning!!!!  groups != out_channels not support!!!!")
                    break
            if flag:
                prec_layers_.append( self.prec_layers[index] )
                norm_layer_names_.append(self.norm_layer_names[index])
                succ_layers_.append( self.succ_layers[index])
        self.prec_layers = prec_layers_ 
        self.norm_layer_names = norm_layer_names_ 
        self.succ_layers = succ_layers_ 
   

        print("BN",self.norm_layer_names)
        print("prec_conv",self.prec_layers)
        print("succ_conv",self.succ_layers)

        #sparisty
        for i in self.norm_layer_names:
            self.sparsity_layernames += i






        

    def prune_algorithm(self):
        if self.algorithm in ['Uniform', 'EagleEye']:
            prune_finetune(self)
        elif self.algorithm in ['netslim', 'maskl1']:
            sparsity_prune_finetune(self)

    def  prune_algorithm_onlyprune(self):
        if self.algorithm in ['Uniform', 'Ratio',  'Order']:
            prune_op(self)



   
