(function() {
    var phone_element = document.getElementById('phone'),
        birthday_element = document.getElementById('birthday');
    
    console.log('health')
    
    var phone_mask_options = {
        mask: '(00) 00000-0000'
    };
    
    var birthday_mask_options = {
        mask: '00/00/0000'
    };

    var phone_mask = IMask(phone_element, phone_mask_options)
    var birthday_mask = IMask(birthday_element, birthday_mask_options)
})();