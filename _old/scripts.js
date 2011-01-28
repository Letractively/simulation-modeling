/**
 * Created by IntelliJ IDEA.
 * User: altaisoft
 * Date: 12.01.2011
 * Time: 0:54:38
 * To change this template use File | Settings | File Templates.
 */

function distribution_switch(selector) {
    /* Смена типа распределения в поле формы типа distribution */

    var equal_controls = document.getElementById(selector.name.replace(/type$/, 'equal'));
    var all_controls = document.getElementById(selector.name.replace(/type$/, 'all'));

    if (selector.value == 'equal') {
        equal_controls.style.display = '';
        all_controls.style.display = 'none';
    } else {
        equal_controls.style.display = 'none';
        all_controls.style.display = '';
    }
}

function set_infinity(id) {
    /* Запись символа ∞ в поле с заданным id */

    var field = document.getElementById(id);
    field.value = 'inf'; // '∞';
}