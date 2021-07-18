(function() {
    var date_element = document.getElementById('date'),
        time_element = document.getElementById('time');
    
    console.log('health')
    
    var date_mask_options = {
        mask: '00/00/0000'
    };
    
    var time_mask_options = {
        mask: '00:00'
    };

    var date_mask = IMask(date_element, date_mask_options)
    var time_mask = IMask(time_element, time_mask_options)
})();