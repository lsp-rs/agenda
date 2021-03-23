function unmask(element) {
    var maskOptions = {
        mask: '000.000.000-00'
    };
    var mask = IMask(element, maskOptions);
    return mask.unmaskedValue;
}