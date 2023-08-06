def get_module(model,name):
    assert type(name) is str
    
    if name.endswith('.bias'):
        name = name[:-5]
    if name.endswith('.weight'):
        name = name[:-7]
    
    container_names = name.split('.')
    if hasattr( model, 'module'):
        container = model.module
    else:
        container = model
    for container_name in container_names:
        container = container._modules[container_name]
    return container
 

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False


def is_transposed(model,name):
    assert type(name) is str
    if name.endswith('.bias'):
        name = name[:-5]
    if name.endswith('.weight'):
        name = name[:-7]
       
    container_names = name.split('.')
    if hasattr( model, 'module'):
        container = model.module
    else:
        container = model
    for container_name in container_names:
        container = container._modules[container_name]
    
    if hasattr( container, 'transposed'  ):
        return container.transposed
    else:
        print("?",name)
        return False;
