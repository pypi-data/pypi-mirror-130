import torch 
from  ..prune.importance  import   l2_norm

def display_layer(model, norm_layer_names,   sparsity_type = 'BN'):

    #loss_s_1=0
    #loss_s_2=0
    #loss_s_3=0
    #loss_s_4=0
    #loss_s_5=0
    #loss_s_6=0
    #loss_s_7=0
    #loss_s_8=0
    #loss_s_9=0
    #loss_s_10=0
    #loss_s_11=0
    #loss_s_12=0
    #loss_s_13=0
    loss_s = [0]*13
    sum_channel =0
    flag =0

    for norm_layer_name in norm_layer_names:
        *container_names, module_name = norm_layer_name.split('.')
        if hasattr(model,'module'):
            container = model.module
        else:
            container = model
        for container_name in container_names:
            container = container._modules[container_name]
        m = container._modules[module_name]
        if sparsity_type == 'lasso':#conv
            if m.transposed:
                source = l2_norm( m.weight.data , axis = 1)
            else :
                source = l2_norm( m.weight.data , axis = 0)
            for i in range(13):
                loss_s[i] += torch.sum( torch.tensor(source).lt(0.1**(i))).item()

        else :# BN
            if flag==0 and  m.weight.data.shape[0]<100 :
            #if norm_layer_name == 'layer1.7.bn1':
                print("\nbn_weight:\n",m.weight.data)
                if hasattr(m.weight, 'grad') :
                    if hasattr(m.weight.grad, 'data'):
                        print("\nbn_grad:\n",m.weight.grad.data)
                flag =1
            for i in range(13):
                loss_s[i] += torch.sum(m.weight.data.abs().lt(0.1**(i))).item()

        sum_channel += m.weight.data.shape[0]
     
    for i in range(13):
        loss_s[i] /=  sum_channel 

    print('________________________')
    print('|scores   |Proportion   |')
    for i in range(13):
        print('|<1e-%-2d   |%.8f   |'%(i,loss_s[i]))
    print('￣￣￣￣￣￣￣￣￣￣￣￣')
    

    for i in range(13):
        print("\r %f"% loss_s[i] ,end="")
        print(loss_s[i])   



def update_layer(model, norm_layer_names, factor=1e-4, scaler = False , mask_dict =None,regular_method='L1'):
    """sparsity the model by adding the sparsity Regularization grad
    Arguments:
        model (pytorch model): the model instance
        norm_layer_names (easypruner.): sparse layer names
        factor(float): the sparsity factor
        ngpu(boolen): needed in getting module by name
        mask_dict(dict): needed in mask sparsity
        regular_method(str): the regular method 
    step:
         1. get BNlayers by the norm_layer_names
         2. get the sparsity grad
         3. mutil the mask
    Returns:
        None
        the result return by
        opt.norm_layer_names 
        opt.prec_layers     
        opt.succ_layers

        a model instance with pruned structure (and weights if load_pruned_weights==True)
    """    
    if scaler :
        factor = factor * 65535
    
    for norm_layer_name in norm_layer_names:
        #get BNlayers by the norm_layer_names
        *container_names, module_name = norm_layer_name.split('.')
        if hasattr(model,'module') :
            container = model.module
        else:
            container = model
        
        for container_name in container_names:
            container = container._modules[container_name]
        m = container._modules[module_name]

        if mask_dict is not None:
            if type(mask_dict) is dict:
                if norm_layer_name not in mask_dict.keys():
                    continue
                mask = mask_dict[norm_layer_name]
            elif type(mask_dict) is float:
                len_ = m.weight.data.shape[0]
                mask = torch.tensor( int(mask_dict*len_)*[0] + (len_ - int( mask_dict*len_))*[1]  ).bool().cuda()


        #get the sparsity grad
        if regular_method=='L1':
            add_grad = factor * torch.sign(m.weight.data) # L1
        elif regular_method=='L2':
            add_grad = factor * m.weight.data # L2
        elif regular_method=='group_lasso':

            assert isinstance(m, (nn.Conv2d, nn.Conv3d, nn.ConvTranspose2d))
            if m.transposed:
                add_grad = m.weight.data * ((m.weight.data ** 2).sum(dim=(1, 2, 3), keepdim=True) ** (-0.5))  #  
            else:
                add_grad = m.weight.data * ((m.weight.data ** 2).sum(dim=(0, 2, 3), keepdim=True) ** (-0.5))  #              
        
        if  mask is not None :
            if regular_method=='group_lasso':
                assert len(mask.shape) == 4
            #mask = ~mask # mask the saved index   
            #add_grad = add_grad.mul(mask.float())
            add_grad[ mask.cuda() ] = 0 

        m.weight.grad.data.add_( add_grad )



def update_layer_grad_decay(model, norm_layer_names, optimizer = None, lr = None, 
                    scaler = False, mask_dict = None, epoch=0, epoch_decay = 0, iters =0):
                    
    """sparsity the model by adding the sparsity Regularization grad
    Arguments:
        model (pytorch model): the model instance
        norm_layer_names (easypruner.): sparse layer names
        optimizer: get the lr
        lr: one element or [lr_weight , lr_bias] . #we can use optimizer replace lr
        scaler(bool): if 
        mask_dict(dict): needed in mask sparsity
        epoch(int): Current epoch
        epoch_decay(int): the epochs when weight decay to zero
        iters(int): iters of one epoch
    step:
         1. get BNlayers by the norm_layer_names
         2. get the sparsity grad
         3. mutil the mask
    Returns:
        None
        the result return by
        opt.norm_layer_names 
        opt.prec_layers     
        opt.succ_layers

        a model instance with pruned structure (and weights if load_pruned_weights==True)
    """ 
    assert optimizer is not None or lr is not None
    if lr is not None:
        assert isinstance(lr,list)
        assert len(lr)>0 
        if len(lr)==1:
            lr.append(lr[0])
  
    assert mask_dict is not None ,"mask_dict needed"
    assert iters > 0
    assert epoch_decay >0
    factor = iters *(    epoch_decay  - epoch   )
    if epoch >=  (  epoch_decay  -2   )  :
        factor = 2*iters
    grad_decay = epoch/(  epoch_decay -20    )
    if grad_decay >=1.0:
        grad_decay=1.0
    
    s = 65535 if scaler else 1
   

    for norm_layer_name in norm_layer_names:
        #get BNlayers by the norm_layer_names
        *container_names, module_name = norm_layer_name.split('.')
        if hasattr(model,'module') :
            container = model.module
        else:
            container = model
        
        for container_name in container_names:
            container = container._modules[container_name]
        m = container._modules[module_name]
        
        if type(mask_dict) is dict:
            if norm_layer_name not in mask_dict.keys():
                continue
            mask = mask_dict[norm_layer_name]
        elif type(mask_dict) is float:
            len_ = m.weight.data.shape[0]
            mask = torch.tensor( int(mask_dict*len_)*[0] + (len_ - int( mask_dict*len_))*[1]  ).bool().cuda()


        w_l1 = []
        b_l1= []
        if optimizer is not None:
            lr = []
            flag =False
            for param_groups in optimizer.param_groups :
                for  param in param_groups['params']:
                    if m.weight is param:
                        lr.append(param_groups['lr'])
                        flag = True
                        break
                if flag:
                    break
            flag = False
            for param_groups in optimizer.param_groups :
                for param in param_groups['params']:
                    if m.bias is param:
                        lr.append(param_groups['lr'])
                        flag = True
                        break
                if flag:
                    break 


        for i in   range(m.weight.data.shape[0]):
            w_l1.append(   s*m.weight.data[i].item() / (lr[0] *factor )    )
            b_l1.append(   s*m.bias.data[i].item() / (lr[1] * factor )      )

        w_l1 = torch.tensor(w_l1).cuda()
        b_l1 = torch.tensor(b_l1).cuda()

        add_grad_w = w_l1
        add_grad_b = b_l1

        add_grad_w[mask.cuda()]=0
        add_grad_b[mask.cuda()]=0

        add_grad_w[~mask.cuda()]-= m.weight.grad.data[  ~mask.cuda() ] * grad_decay
        add_grad_b[~mask.cuda()]-= m.bias.grad.data[  ~mask.cuda() ]  * grad_decay
        #add_grad[0: int(add_grad.shape[0]/2)]=0
        if lr[0] !=0:
            m.weight.grad.data.add_( add_grad_w  )
        if lr[1] !=0:
            m.bias.grad.data.add_( add_grad_b  )
