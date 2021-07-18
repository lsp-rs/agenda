(function() {
    var date_element = document.getElementById('date'),
        time_element = document.getElementById('time');
        form_scheduling = document.forms['form-scheduling'];

    form_scheduling.onsubmit = function (event){
        event.preventDefault();
        date_element.value = unmask_date(date_element);
        time_element.value = unmask_time(time_element);
        form_scheduling.submit();
    }
})();
