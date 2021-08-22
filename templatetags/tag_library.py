from django import template
import datetime
import jpholiday
from dateutil.relativedelta import relativedelta
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
    startdate = datetime.date.today() + relativedelta(months=-2)
    post_qs = object.filter(date__gte=startdate)

    return post_qs
