const picked = document.querySelector('#date-picked');

COLORS = {
    "low" : '#5bc8ff',
    "medium" : '#ffca59',
    "high" : '#f08080'
}

var color_days = [],
    levels_values = document.getElementById("levels").value,
    context = JSON.parse(levels_values);


for (k in context){
    color_days.push(
        {
            days: [context[k][0]],
            backgroundColor: COLORS[context[k][1]],
        }
    )
}

const calendar = new HelloWeek({
    langFolder: "static/js/langs/",
    selector: '#calendar',
    lang: 'pt-BR',
    disabledDaysOfWeek: [0],
    disablePastDays: true,
    todayHighlight: false,
    daysHighlight: color_days,
    onSelect: () => {
        document.getElementById('calendar').scrollIntoView();
        picked.value = new Date(calendar.lastSelectedDay).toLocaleDateString('pt-BR', {timeZone: 'UTC'});
    },
});
