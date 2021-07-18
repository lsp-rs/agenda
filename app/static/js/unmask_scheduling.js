function unmask_date(element) {
    var maskOptions = {
        mask: '00/00/0000'
    };
    var mask = IMask(element, maskOptions);
    return mask.unmaskedValue;
}

function unmask_time(element) {
    var maskOptions = {
        mask: '00:00'
    };
    var mask = IMask(element, maskOptions);
    return mask.unmaskedValue;
}