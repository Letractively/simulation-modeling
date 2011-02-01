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

