function distribution_switch(selector) {
    /* Смена типа распределения в поле формы типа distribution */

    basename = selector.name.replace(/type$/, '')
    var central     = document.getElementById(basename + 'central').style;
    var range_first = document.getElementById(basename + 'range-first').style;
    var range_last  = document.getElementById(basename + 'range-last').style;

    if (selector.value == 'equal') {
        central.display = 'none';
        range_first.display = '';
        range_last.display = '';
    } else {
        central.display = '';
        range_first.display = 'none';
        range_last.display = 'none';
    }
}

function insert_operation(button) {
    /* Добавление нового цеха в модели производственной фирмы */
    
    var footer = button.parentNode.parentNode;
    var index  = footer.rowIndex;
    var table  = footer.parentNode.parentNode;
    
    /* Заголовок */
    var th = document.createElement('th');
    th.setAttribute('class', 'label');
    th.innerHTML = 'Цех ' + (index - 4);
    
    /* Ячейка */
    var td = document.createElement('td');
    
    /* Поле ввода */
    input = document.createElement('input');
    input.setAttribute('type', 'text');
    input.setAttribute('class', 'text');
    
    var id = 'operations.' + (index - 5);
    input.setAttribute('id', id);
    input.setAttribute('name', id);
    td.appendChild(input);
    
    /* Единица измерения */
    unit = document.createElement('span');
    unit.setAttribute('class', 'unit');
    unit.innerHTML = 'ч';
    td.appendChild(unit);
    
    /* Добавляем */
    var tr = table.insertRow(index);
    tr.appendChild(th); tr.appendChild(td);
}

