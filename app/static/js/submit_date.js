(function() {
    var date_element = document.getElementById('date-picked'),
        form_calendar = document.forms['form-calendar'];

    form_calendar.onsubmit = function (event){
        event.preventDefault();
        if(date_element.value){
            form_calendar.submit();
        }
    }
})();
