# -*- coding: utf-8 -*-

'Процедуры для работы с деревьями'

def from_materialized_path(leaves):
    'Превращение списка листьев в дерево'
    
    # Результирующее дерево
    tree = {}
    for path, value in leaves.items(): # Добавление узла value по пути path
        # Текущая ветка
        branch = tree
        
        tokens = path.split('.')
        for i, token in enumerate(tokens):
            if not token:
                raise ValueError(u'Узел дерева не имеет имени.')
            
            if type(branch) != dict:
                raise ValueError(u'Части дерева противоречат друг другу.')
            
            else:
                if token not in branch:
                    # Если ветки нет
                    if i == len(tokens) - 1: # Если это - лист
                        branch[token] = value
                        break
                    else: # Или если ветка
                        branch[token] = {}
                
                branch = branch[token]
    
    return tree

def recursive_map(f, *trees):
    'Несимметричный рекурсивный map'
    
    if not trees:
        return {}
    
    tree = trees[0]
    
    if type(tree) == dict: # Ветка
        output = {}
        
        for key, value in tree.items():
            output[key] = recursive_map(f, *(tree.get(key, None) if hasattr(tree, 'get') else None for tree in trees))
        
        return output
    
    if type(tree) in (list, tuple):
        output = []
        
        for index, value in enumerate(tree):
             output.append(recursive_map(f, *(tree[index] if len(tree) > index else None for tree in trees)))
         
        return output
    
    # Лист
    return f(*trees)

