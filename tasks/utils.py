from calendar import HTMLCalendar


class Calendar(HTMLCalendar):
    def __init__(self, queryset, year=None, month=None):
        self.queryset = queryset
        self.year = year
        self.month = month
        super().__init__()

    def formatday(self, day):
        meetings_per_day = self.queryset.filter(planned_date__day=day)
        day_events = []
        for meeting in meetings_per_day:
            day_events.append(f'<li>{meeting.get_html_paragraph}</li>')
        if day != 0:
            return (
                f'<td><span class="date">{day}</span><ul>'
                + ''.join(day_events)
                + '</ul></td>'
            )
        return '<td></td>'

    def formatweek(self, week):
        week_meetings = []
        for day in week:
            week_meetings.append(self.formatday(day[0]))
        return '<tr>' + ''.join(week_meetings) + '</tr>'

    def formatmonth(self, with_year=True):
        month_name = self.formatmonthname(
            self.year,
            self.month,
            withyear=with_year,
        )
        calendar = f'{month_name}\n{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            calendar += f'{self.formatweek(week)}\n'
        return calendar
