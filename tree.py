# -*- coding: utf-8 -*-

'Процедуры для работы с деревьями'

def recursive_map(f, *trees):
    'Несимметричный рекурсивный map'
    
    fallback = 0
    
    if not trees:
        return {}
    
    tree = trees[0]
    
    if type(tree) == dict: # Ветка
        output = {}
        
        for key, value in tree.items():
            output[key] = recursive_map(f, *(tree.get(key, None) if hasattr(tree, 'get') else fallback for tree in trees)) 
        return output
    
    if type(tree) in (list, tuple):
        output = []
        
        for index, value in enumerate(tree):
             output.append(recursive_map(f, *(tree[index] if len(tree) > index else fallback for tree in trees)))
         
        return output
    
    # Лист
    return f(*trees)

