from django import template
import datetime
import jpholiday
register = template.Library()

@register.filter(name="jpholiday")
def jpholiday_judge(day):
   val = jpholiday.is_holiday(day)

   return val

@register.filter(name="editable")
def editable_count(object,arg):
    int = object.filter(published=arg).count()

    return int

@register.filter(name="three_months")
def three_months_ago(object):
    startdate = datetime.date(datetime.date.today().year,
                datetime.date.today().month- 3, 1)
    enddate = datetime.date.today()
    post_qs = object.filter(date__range=[startdate, enddate])

    return post_qs
