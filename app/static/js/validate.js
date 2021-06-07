function validate_cpf(element_cpf) {
    var cpf = element_cpf.value,
        regex = RegExp('[0-9]{3}\\.[0-9]{3}\\.[0-9]{3}\\-[0-9]{2}');

    if (regex.test(cpf)) {
        success_class(element_cpf);
        return true;
    } else {
        fail_class(element_cpf);
        return false;
    }
}


function validate_check(element_checkbox) {
    var check = element_checkbox.checked;
    if (check) {
        success_class(element_checkbox);
        return true;
    } else {
        fail_class(element_checkbox);
        return false;
    }
}


function success_class(element) {
    element.classList.remove('is-invalid');
    element.classList.add('is-valid');
}


function fail_class(element) {
    element.classList.remove('is-valid');
    element.classList.add('is-invalid');
}
