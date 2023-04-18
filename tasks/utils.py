from calendar import HTMLCalendar

import django.urls
from django.utils import timezone


class Calendar(HTMLCalendar):
    def __init__(self, queryset, year=None, month=None):
        self.queryset = queryset
        self.year = year
        self.month = month
        super().__init__()

    def formatday(self, day):
        day_events = []
        style = 'underline text-blue-600 hover:text-blue-800'
        for meeting in self.queryset:
            planned_date = timezone.localtime(meeting['planned_date'])
            if planned_date.day == day:
                planned_date = planned_date.strftime('%H:%M')
                meeting_link = django.urls.reverse(
                    'meetings:detail', kwargs={'pk': meeting['id']}
                )
                day_events.append(
                    ''.join(
                        [
                            '<li>',
                            f'<p class="text-white text-center">{planned_date} ',
                            f'<a class="{style}" href="{meeting_link}">',
                            meeting['name'],
                            '</a></p></li>',
                        ]
                    )
                )
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
