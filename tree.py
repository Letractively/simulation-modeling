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
        for token in tokens[:-1]:
            if type(branch) != dict:
                raise ValueError(u'Части дерева противоречат друг другу.')
            
            else:
                # Создаём ветку, если её нет
                if token not in branch:
                    branch[token] = {}
                
                # Переходим в неё
                branch = branch[token]
            
        # Узел
        token = tokens[-1]
        branch[token] = value
    
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
    
    else: # Лист
        return f(*trees)

