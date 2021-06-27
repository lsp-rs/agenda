const picked = document.querySelector('#date-picked');

const calendar = new HelloWeek({
    langFolder: "static/js/langs/",
    selector: '#calendar',
    lang: 'pt-BR',
    disabledDaysOfWeek: [0],
    disablePastDays: true,
    todayHighlight: false,
    daysHighlight: [
        {
            days: ['2021-06-24'],
            backgroundColor: '#5bc8ff',
        },
        {
            days: ['2021-06-28'],
            backgroundColor: '#f08080',
        },
        {
            days: ['2021-06-30'],
            backgroundColor: '#ffca59',
        },
        {
            days: ['2021-07-22'],
            backgroundColor: '#ffca59',
        },
        {
            days: ['2021-07-17'],
            backgroundColor: '#f08080',
        },
    ],
    onSelect: () => {
        document.getElementById('calendar').scrollIntoView();
        picked.innerHTML = new Date(calendar.lastSelectedDay).toLocaleDateString('pt-BR', {timeZone: 'UTC'});
        // console.log(new Date(calendar.lastSelectedDay).toLocaleDateString('pt-BR', {timeZone: 'UTC'}));
        // console.log(calendar.getDays()); //Forma com erro.
    },
});
