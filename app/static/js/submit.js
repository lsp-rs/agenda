(function() {
    var element_phone = document.getElementById('phone'),
        element_birthday = document.getElementById('birthday'),
        form_account_create = document.forms['form-account-create'];

    form_account_create.onsubmit = function (event){
        event.preventDefault();
        element_phone.value = unmask_phone(element_phone);
        form_account_create.submit();
    }
})();
