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

function add_operation(buttonNode, child) {
    /* Добавление цеха */
    
    /* Fieldset */
    var fieldset = buttonNode.parentNode.parentNode;
    
    var index = 0;
    var children = fieldset.getElementsByTagName('div');
    for (i = 0; i < children.length; ++i) {
        if (children[i].className == 'row operation') {
            index++;
        }
    }
    
    /* Новый элемент */
    var child = document.createElement('div');
    with (child) {
        className = 'row operation';
        htmlName = 'operations.' + index;
        
        /* <label> */
        var label = document.createElement('label');
        label.innerHTML = 'Рабочий ' + (index + 1);
        
            /* Remove button */
            var remove = document.createElement('a');
            with (remove) {                
                href = '#';
                title = 'Удалить рабочего';
                onclick = 'remove_operation(this)';
            }
            
            var span = document.createElement('span');
            span.className = 'button remove left';
            remove.appendChild(span);
            
            label.appendChild(remove);
        
        appendChild(label);
        
        /* unit */
        var unit = document.createElement('span');
        with (unit) {
            className = 'unit';
            innerHTML = 'ч';
            htmlFor = htmlName;
        }
        appendChild(unit);
        
        /* <input> */
        input = document.createElement('input');
        with (input) {
            type = 'text';
            className = 'text';
            id = htmlName;
            name = htmlName;
        }
        appendChild(input);
    }
    
    fieldset.appendChild(child);
}

function remove_operation(button) {
    row = button.parentNode.parentNode;
    row.parentNode.removeChild(row);
}

/* FancyBox */
$(document).ready(function() {
    $("a#permalink").fancybox({
        'width'  : 180,
        'height' : 180
    });
})


