import zoneinfo
from calendar import LocaleHTMLCalendar

import django.urls
from django.utils import timezone


class Calendar(LocaleHTMLCalendar):
    def __init__(self, request, queryset, locale, year=None, month=None):
        self.request = request
        self.queryset = queryset
        self.year = year
        self.month = month
        super().__init__(locale=locale)

    def formatday(self, day):
        day_events = []
        style = 'underline text-[#e8d461] hover:text-[#dec952]'
        user_timezone = None
        if 'django_timezone' in self.request.COOKIES.keys():
            user_timezone = zoneinfo.ZoneInfo(
                self.request.COOKIES['django_timezone']
            )
        for meeting in self.queryset:
            planned_date = timezone.localtime(
                meeting['planned_date'],
                timezone=user_timezone,
            )
            if planned_date.day == day:
                planned_date = planned_date.strftime('%H:%M')
                meeting_link = django.urls.reverse(
                    'meetings:detail', kwargs={'pk': meeting['id']}
                )
                day_events.append(
                    ''.join(
                        [
                            '<li><p class="text-white text-center">',
                            f'{planned_date}',
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
