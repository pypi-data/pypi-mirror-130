#import os 
#import core 
#import  prune 
#import regularize
#import scheme
#import utils 

from ..prune  import  prune
__all__ = ['prune_finetune' , 'sparsity_prune_finetune' , 'prune_op' ]

def prune_finetune(opt):
    prune(opt)
    if opt.Adaptive_BN is not None and opt.dataloader_train is not None:
        opt.Adaptive_BN(opt.model , opt.dataloader_train)
        opt.eval(opt.model , opt.args)
    opt.args.lr = 1e-3
    opt.args.state =  'finetune'
    opt.args.path = opt.workdir
    opt.train(opt.model , opt.args)
    
def sparsity_prune_finetune(opt):

    opt.args.state = 'sparsity'
    opt.args.EP_norm_layer_names = opt.sparsity_layernames
    opt.args.EP_sparsity_factor= opt.sparsity_factor  
    opt.args.EP_mask_dict = opt.sparsity_mask
    opt.args.EP_regular_method = opt.sparsity_method

    opt.train(opt.model , opt.args)
    prune(opt)
    opt.args.lr = 1e-3 

    opt.args.state =  'finetune'
    opt.train(opt.model , opt.args) 

def prune_op(opt):
    prune(opt)
    if opt.Adaptive_BN is not None and opt.dataloader_train is not None:
        opt.Adaptive_BN(opt.model , opt.dataloader_train)



