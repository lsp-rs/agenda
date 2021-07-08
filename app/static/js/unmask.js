function unmask_phone(element) {
    var maskOptions = {
        mask: '(00) 00000-0000'
    };
    var mask = IMask(element, maskOptions);
    return mask.unmaskedValue;
}