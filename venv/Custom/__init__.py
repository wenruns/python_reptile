# 实现类似于switch的功能
def switch(case, options:dict):
    option = options.get(case, options.get('default'))
    if hasattr(option,'__call__'):
        return option()
    else:
        return option





