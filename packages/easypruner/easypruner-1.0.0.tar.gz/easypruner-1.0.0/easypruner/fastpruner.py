from datetime import datetime
from . import   config



def fastpruner(net,prune_factor=0.5,input_dim = [3,416,416],method = 'Ratio', onnx_file=None):
    if method == 'Uniform':
        fastuniform(net,prune_factor ,input_dim,onnx_file)
    elif method == 'Ratio':
        fastratio(net,prune_factor,input_dim,onnx_file)
    elif method == 'Order':
        fastorder(net,prune_factor,input_dim,onnx_file)
    else:
        print("please check the format of methods.[Uniform, Ratio, order]")


def fastuniform(net,flops_saved=0.5,input_dim = [3,224,224],onnx_file=None):
    opt = config('tmp','Uniform' )
    opt.add_layer_need = False
    opt.concat_layer_need = False
    opt.model = net
    opt.onnx_file = onnx_file
    opt.use_conv_statistics = True
    #opt.prune_stride_2 = False
    opt.input_shape= (3 ,  input_dim[1], input_dim[2]  )     #input_shape   (3,256,256)
    #prune
    opt.prune_save_flops  = flops_saved    #save_flops float
    opt.prune_criterion   = 'L1'    #criterion()   importance函数
    opt.init()
    opt.prune_algorithm_onlyprune()

def fastratio(net,channel_saved=0.5,input_dim = [3,224,224],onnx_file=None):
    opt = config('tmp','Ratio' )
    opt.algorithm = 'Ratio'
    opt.add_layer_need = False
    opt.concat_layer_need = False
    opt.model = net
    opt.input_shape = (3 ,  input_dim[1], input_dim[2] )     #input_shape   (3,256,256)
    #prune
    opt.prune_criterion   = 'L1'    #criterion()   importance函数
    opt.prune_factor =channel_saved
    opt.onnx_file = onnx_file
    opt.use_conv_statistics = True
    opt.prune_stride_2  = False
    opt.init()
    opt.prune_algorithm_onlyprune()



def fastorder(net, threshold=0.5,input_dim = [3,224,224],onnx_file=None):
    opt = config('tmp','Order' )
    opt.algorithm = 'Order'
    opt.add_layer_need = False
    opt.concat_layer_need = False
    opt.model = net
    opt.onnx_file = onnx_file
    opt.use_conv_statistics = False
    opt.prune_stride_2  = True
    opt.input_shape = (3 ,  input_dim[1], input_dim[2] )     #input_shape   (3,256,256)
    #prune
    opt.prune_criterion   = 'L1'    #criterion()   importance函数
    opt.prune_factor = threshold
    opt.init()
    opt.prune_algorithm_onlyprune()



def getprunelayer(net,flops_saved=0,input_dim = [3,224,224],onnx_file=None):
    opt = config('tmp','tmp' )
    opt.add_layer_need = False
    opt.concat_layer_need = False
    opt.prune_stride_2 = True
    opt.model = net
    opt.onnx_file = onnx_file
    opt.input_shape= (3 ,  input_dim[1], input_dim[2]  )     #input_shape   (3,256,256)
    opt.prune_save_flops  = flops_saved    #save_flops float
    opt.prune_criterion   = 'L1'    #criterion()   importance函数
    opt.init()
    return  opt.sparsity_layernames


