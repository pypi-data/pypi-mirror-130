import os, sys
import torch.onnx
import functools
#no complete
NORM_LAYER_KEYWORDS = ["BatchNormalization","batch_norm", "group_norm", "instance_norm"]
CONV_LAYER_KEYWORDS = ["convolution", "addmm", "Conv"]  # does not support groups > 1 for conv
LINEAR_LAYER_KEYWORDS = ["Gemm",""] # "PRelu"
#PASS_KEYWORDS = ["Mul","relu", "leaky_relu", "sigmoid", "tanh","Relu",
#                 "pool", "pad", "dropout","MaxPool","Reshape","Concat","Unsqueeze","Gather","Shape","GlobalAveragePool",
#                 "view", ]  # and more .. does not support concat
PASS_KEYWORDS = ["Mul","relu", "PRelu", "Prelu","leaky_relu", "sigmoid", "tanh","Relu",
                 "pool", "pad", "Pad", "dropout","MaxPool","Reshape","Unsqueeze","Gather","Shape","GlobalAveragePool",
                 "view", "Resize","Dropout" ,"dropout","AveragePool"]  # and more .. does not support concat
ADD_KEYWORDS = ["Add" ]  #
UN_SUPPORTED_KEYWORDS = ["Concat", ]
#OTHER_OP_KEYWORDS = ["cat"]
#OTHER_PRIM_KEYWORDS = ["ListConstruct"]  # for cat
#NO_EFFECT_KEYWORDS = ["size", ]

#def process_prune_layers(opt):
 #   opt.model

def get_prune_layers(opt):
    """load pruned weights to a unpruned model instance

    Arguments:
        net (pytorch model): the cpu model instance
        opt (easypruner.): pruned weights
    step:
         1. get onnx file
         2. get graph, succ&prec relation by onnx file
         3. merge the passable layer
         3. get norm BN
         4. get Add operation 
         5. get connectate  operation
    Returns:
        None
        the result return by
        opt.norm_layer_names 
        opt.prec_layers     
        opt.succ_layers

        a model instance with pruned structure (and weights if load_pruned_weights==True)
    """
    net = opt.model 
    to_del = []
    def GetPydotGraph(
    graph,  # type: GraphProto
    name=None,  # type: Optional[Text]
    rankdir='LR',  # type: Text
    node_producer=None,  # type: Optional[_NodeProducer]
    embed_docstring=False,  # type: bool
    ):  # type: (...) -> pydot.Dot

        previous_layer = {}
        succeding_layer = {}
        blob_to_layer={}
       # import pdb;pdb.set_trace()
        for op_id, op in enumerate(graph.node):
            name = op_id;#op.name
            for output_name in op.output:
                if output_name in blob_to_layer:
                    print("error");
#                    import pdb;pdb.set_trace()
                blob_to_layer[output_name] = name;

            for input_name in op.input:
                if input_name not in blob_to_layer:
                    input_node = None
                    blob_to_layer[input_name] = None
                    #import pdb;pdb.set_trace()
                else:
                    input_layer = blob_to_layer[input_name]
                    if name in previous_layer:
                        previous_layer[name].append(input_layer)
                    else:
                        previous_layer[name] = [input_layer,]
                    if input_layer in succeding_layer:
                        succeding_layer[input_layer].append(name)
                    else:
                        succeding_layer[input_layer] = [name,]
        return previous_layer,succeding_layer

    def omit_pass(node_id,biao,org_dict, new_dict):
        if biao not in org_dict:
            return
        biao = org_dict[biao]
        for i in biao:
            if model.graph.node[i].op_type in PASS_KEYWORDS :
                omit_pass( node_id, i,org_dict,new_dict)
            elif model.graph.node[i].op_type in UN_SUPPORTED_KEYWORDS:
                #new_dict[node_id].append(-1000)
                to_del.append(node_id)
            else :
                if i not in new_dict[ node_id ]:
                    new_dict[ node_id ].append(i)
    def omit_pass_forward(node_id,biao,org_dict, new_dict):
        if biao not in org_dict:
            return
        biao = org_dict[biao]
        for i in biao:
            if model.graph.node[i].op_type in  ['shape','Shape'] :
                continue
            if model.graph.node[i].op_type in PASS_KEYWORDS :
                omit_pass_forward( node_id, i,org_dict,new_dict)
            elif model.graph.node[i].op_type in UN_SUPPORTED_KEYWORDS:
                to_del.append(node_id)
            #    new_dict[node_id].append(-1000)
            else :
                if i not in new_dict[ node_id ]:
                    new_dict[ node_id ].append(i)
    #1. get onnx file
    #import pdb;pdb.set_trace()
    if opt.onnx_file == None:
        if type(net.forward) is functools.partial: #for mmlab #opt.is_open_mmlab_codes:
            torch.onnx.export( net.cpu(), [torch.randn(1, *opt.input_shape, requires_grad=True)],  os.path.join( opt.workdir, opt.exp_name+'.onnx') ,verbose= False, opset_version=11, training= True, do_constant_folding=True)
        else:
            torch.onnx.export( net.cpu(), torch.randn(1, *opt.input_shape, requires_grad=True),  os.path.join( opt.workdir, opt.exp_name+'.onnx') ,verbose= False, opset_version=11, training= True, do_constant_folding=True)
        import onnx 
        model = onnx.load(os.path.join( opt.workdir, opt.exp_name+'.onnx'))
    else:
        import onnx 
        model = onnx.load(opt.onnx_file)
        print("load my onnx file")
        

    #2. get graph, succ&prec relation
    previous_layer,succeding_layer = GetPydotGraph(model.graph)

    ####################################################### get the layer name
    BN_layer = []
    for op_id, op in enumerate(model.graph.node):
        if op.op_type in NORM_LAYER_KEYWORDS:
            BN_layer.append(op_id)

    ADD_layer = []
    for op_id, op in enumerate(model.graph.node):
        if op.op_type in ADD_KEYWORDS:
            ADD_layer.append(op_id)

    CONV_layer = []
    for op_id, op in enumerate(model.graph.node):
        if op.op_type in CONV_LAYER_KEYWORDS:
            CONV_layer.append(op_id)
    ####################################################### merge the passable layer
#    import pdb;pdb.set_trace()
    prec_l = {}
    succ_l = {}
    for i in BN_layer + ADD_layer : #+ CONV_layer :
        prec_l[i] = []
        succ_l[i] = []
        omit_pass_forward(i, i, succeding_layer, succ_l)
        omit_pass(i, i, previous_layer,  prec_l)

#    to_del=[]
#    for key  in succ_l:
#        for j in succ_l[key]:
#            if j == -1000:
#                #del succ_l[key]
#                to_del.append(key)
#                #break
#    for key in to_del:
#        if key in succ_l:
#            del succ_l[key]
#        if key in prec_l:
#            del prec_l[key]
#        if key in BN_layer:
#            del BN_layer[key]
 
            
#    import pdb;pdb.set_trace()
    result_BN = []
    result_succ = []
    result_prec = []

    BN2add_layer =[]
    ######################################################## batch normal
    for i in BN_layer :
        if "Add" in [  model.graph.node[j].op_type   for j in succ_l[i]    ]:
            BN2add_layer.append(i)
            continue
        result_BN.append([i])
        result_succ.append(succ_l[i])
        result_prec.append(prec_l[i])

    ############################################################add
    add_bn_layer = []
    add_bn_succ = []
    add_bn_prec = []

    def add_get_root(node_id):
        if not( set(ADD_KEYWORDS)  & set(  model.graph.node[i].op_type   for i in prec_l[node_id]  )):
            return node_id
        for i in prec_l[node_id] :
            if model.graph.node[i].op_type in ADD_KEYWORDS:
                return add_get_root(i)

    def add_get_all(node_id,deal_list):
        deal_list.append(node_id)
        for i in succ_l[node_id]:
            if model.graph.node[i].op_type in ADD_KEYWORDS:
                add_get_all(i,deal_list)

    have_deal = []
    for i in ADD_layer:
        #judge
        if i in have_deal:
            continue
        #get all add layer
        Add_root = add_get_root(i)
        deal_list = []
        #print("root",Add_root)
        add_get_all(Add_root,deal_list)
        #print(deal_list)
        #get_bn_layer
        bn_layer = []
        for ii in deal_list:
            for j in prec_l[ii]:
                if model.graph.node[j].op_type in   NORM_LAYER_KEYWORDS :
                    bn_layer.append(j)
        #get_prec
        add_prec = []
        for ii in bn_layer:
            for j in prec_l[ii]:
                add_prec.append(j)


        #get_succ
        add_succ =set()
        for ii in bn_layer + deal_list:
            for j in succ_l[ii]:
                if model.graph.node[j].op_type not in  ADD_KEYWORDS:
                    add_succ.add(j)
       
        #dealed
        have_deal += deal_list
        add_bn_layer.append( bn_layer   )
        add_bn_succ.append(  list(add_succ)  )
        add_bn_prec.append(  add_prec  )




    #########################################################################deal all
    if opt.add_layer_need :
        result_BN   += add_bn_layer
        result_prec += add_bn_prec
        result_succ += add_bn_succ
    #import pdb;pdb.set_trace();
    """
    if opt.stride_2:
        for lid,i in enumerate(result_prec):
            for ele in i:
                node = model.graph.node[ele]
                for attribute in node.attribute:
                    if attribute.name == "strides":
                        strides = max(attribute.ints)
                        if strides > 1:
                            for bnele in result_BN[lid]:
                                to_del.append(bnele)
                            continue
    """
  
   # import pdb;pdb.set_trace()
    to_save_indexes = []
    for lid, layer in enumerate(result_BN):
        delete_flag = False;
        for node_id in layer:
            if node_id in to_del:
                delete_flag = True;
        if delete_flag:
            pass
        else:
            to_save_indexes.append(lid)


  #  import pdb;pdb.set_trace();
    result_BN = [result_BN[ele] for ele in to_save_indexes]
    result_prec = [result_prec[ele] for ele in to_save_indexes]
    result_succ = [result_succ[ele] for ele in to_save_indexes]

    # for to_del_id in to_del_indexes:
    #     del result_BN[to_del_id] 
    #     del result_prec[to_del_id]
        
        
    #     del result_succ[to_del_id]
    #import pdb;pdb.set_trace();

    result_BN_str     = []
    result_prec_str   = []
    result_succ_str   = []
    for i in range(len(result_BN)):
        list_=[]
        for j in result_BN[i]:
            weight_name = model.graph.node[j].input[1]
            group_name = '.'.join(weight_name.split('.')[:-1])
            list_.append(group_name)
            if group_name=="":
                #import pdb;pdb.set_trace()
                pass;
        result_BN_str.append(list_)
        
        list_=[]
        for j in result_prec[i]:
            if len( model.graph.node[j].input ) > 1:
                weight_name = model.graph.node[j].input[1]
                group_name = '.'.join(weight_name.split('.')[:-1])
                list_.append(group_name)
                if group_name=="":
                    #import pdb;pdb.set_trace()
                    pass;
        result_prec_str.append(list_)
        
        list_=[]
        for j in result_succ[i]:
            if len( model.graph.node[j].input ) > 1:
                #import pdb;pdb.set_trace()
                weight_name = model.graph.node[j].input[1]
                group_name = '.'.join(weight_name.split('.')[:-1])
                list_.append(group_name)
                if group_name=="":
                    #import pdb;pdb.set_trace()
                    pass;
        result_succ_str.append(list_)
#    import pdb;pdb.set_trace();
    opt.norm_layer_names =  result_BN_str
    opt.prec_layers      =  result_prec_str
    opt.succ_layers      =  result_succ_str  
    print()
    #import pdb;pdb.set_trace();
