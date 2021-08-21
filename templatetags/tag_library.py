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
  
