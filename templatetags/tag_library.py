from django import template
import datetime as dt
dtt = dt.datetime
import jpholiday
from blog.models import Shift, User, Post
from dateutil.relativedelta import relativedelta
register = template.Library()

@register.filter(name="w_name")
def w_change(w):
   w_name = '(' + w[0] + ')'

   return w_name

@register.filter(name="jpholiday")
def jpholiday_judge(day):
   val = jpholiday.is_holiday(day)

   return val

@register.filter(name="count")
def count(objects):
    int = objects.count()

    return int

@register.filter(name="editable")
def editable_count(object,arg):
    int = object.filter(published=arg).count()

    return int

@register.filter(name="shift_all")
def shift_all(user):
    shift_list = Shift.objects.filter(name=user).order_by('-date')

    return shift_list

@register.filter(name="post_all")
def post_all(user):
    post_list = Post.objects.filter(name=user).order_by('-date')

    return post_list

@register.filter(name="three_months")
def three_months_ago(object):
    startdate = dt.date.today() + relativedelta(months=-2)
    post_qs = object.filter(date__gte=startdate)

    return post_qs

@register.filter(name="date_filter")
def date_range_filter(object,args):
    if  len(args) == 21:
        startdate = args.split(',')[0]
        enddate = args.split(',')[1]
        post_qs = object.filter(date__range=[startdate,enddate])
        return post_qs
    else:
        return object

@register.filter(name="day_my_post")
def day_my_post(object,arg):
    if Post.objects.filter(date=object,name=arg).exists():
        qs = Post.objects.filter(date=object,name=arg)
        return qs
    else:
        return False

@register.filter(name="day_my_shift")
def day_my_shift(object,arg):
    if Shift.objects.filter(date=object,name=arg).exists():
        qs = Shift.objects.filter(date=object,name=arg)
        return qs
    else:
        return False

@register.filter(name="day_admin_shift")
def day_admin_shift(object):
    if Shift.objects.filter(date=object).exists():
        qs_list = Shift.objects.filter(date=object)
        return qs_list
    else:
        return False

@register.filter(name="day_shift_help")
def day_shift_help(object):
    help = User.objects.get(username=244)
    if Shift.objects.filter(date=object,name=help).exists():
        return True
    else:
        return False

@register.filter(name="date_comparison")
def date_comparison(time,day):
    now = dtt.now()
    now_time = dt.time(hour=now.hour, minute=now.minute)
    today = dt.date.today()
    if day < today:
        return True
    elif day == today:
        if not time <= dt.time(hour=5):
            if time <= now_time:
                return True
    else:
        return False

def time_count(start,end):
    start_time = dtt.combine(dt.date(2000, 1, 1), start)
    end_time = dtt.combine(dt.date(2000, 1, 1), end)
    if end_time < start_time:
        if end <= dt.time(hour=5):
            end_time = dtt.combine(dt.date(2000, 1, 2), end)
    else:
        if start <= dt.time(hour=5) and end <= dt.time(hour=5):
            start_time = dtt.combine(dt.date(2000, 1, 2), start)
            end_time = dtt.combine(dt.date(2000, 1, 2), end)
    night_time = dtt.combine(dt.date(2000, 1, 1), dt.time(hour=22))

    if end_time >= night_time:
        if start_time < night_time:
            end_time_night = end_time - night_time
            time_list = [end_time - start_time,end_time_night]
            work_time = [[int(str(time).split(':')[0]),
                int(str(time).split(':')[1])] for time in time_list]
            return work_time
        else:
            time_list = [end_time - start_time,end_time - start_time]
            work_time = [[int(str(time).split(':')[0]),
                int(str(time).split(':')[1])] for time in time_list]
            return work_time
    else:
        time = [end_time - start_time]
        time_list = str(time[0]).split(':')
        work_time = [int(time_list[0]),int(time_list[1])]
        return work_time

def minute_count(start,end):
    start_min = int(str(start).split(':')[0])*60 + int(str(start).split(':')[1])
    end_min = int(str(end).split(':')[0])*60 + int(str(end).split(':')[1])
    count_min = end_min - start_min
    count = [count_min//60,count_min%60]
    return count

@register.filter(name="work_time")
def work_time(object):
    start_time = object.start_time
    end_time = object.end_time
    rest_time = object.time
    night_time = dt.time(hour=22)
    count = time_count(object.start_time,object.end_time)
    if isinstance(count[0], list):
        work_time = count[0]
    else:
        work_time = count
    work_count = minute_count(rest_time,dt.time(
            hour=work_time[0],minute=work_time[1]))
    time = str(work_count[0])+'時間'+str(work_count[1])+'分'
    return time

@register.filter(name="work_time_sum")
def work_time(object_list):
    time_hour_sum = 0
    time_minutes_sum = 0
    night_hour_sum = 0
    night_minutes_sum = 0
    over_hour_sum = 0
    over_minutes_sum = 0
    for object in object_list:
        start_time = object.start_time
        end_time = object.end_time
        rest_time = object.time
        night_time = dt.time(hour=22)
        if end_time >= night_time or end_time <= dt.time(hour=5):
            time_list = time_count(start_time,end_time)
            time_list_new = minute_count(rest_time,dt.time(
                    hour=time_list[0][0],minute=time_list[0][1]))
            time_hour_sum += time_list_new[0]
            time_minutes_sum += time_list_new[1]
            night_hour_sum += time_list[1][0]
            night_minutes_sum += time_list[1][1]
            if time_list_new[0] >= 8:
                over_hour_sum += time_list_new[0] - 8
                over_minutes_sum += time_list_new[1]
        else:
            time_list = time_count(start_time,end_time)
            time_list_new = minute_count(rest_time,dt.time(
                    hour=time_list[0],minute=time_list[1]))
            time_hour_sum += time_list_new[0]
            time_minutes_sum += time_list_new[1]
            if time_list_new[0] >= 8:
                over_hour_sum += time_list_new[0] - 8
                over_minutes_sum += time_list_new[1]
    time_sum = (str(time_hour_sum + time_minutes_sum//60)+'時間'+
                str(time_minutes_sum%60)+'分')
    night_sum = (str(night_hour_sum + night_minutes_sum//60)+'時間'+
                str(night_minutes_sum%60)+'分')
    over_sum = (str(over_hour_sum + over_minutes_sum//60)+'時間'+
                str(over_minutes_sum%60)+'分')
    sum_list = [time_sum,night_sum,over_sum]

    return sum_list
