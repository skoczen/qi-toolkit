from django import template
from django.conf import settings
register = template.Library()
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import date, timesince
import datetime

@register.filter
def clean_none(str):
    if str:
        return str
    else:
        return ""


@register.filter
def multiply(n1, n2):
    """Multiply by a value."""
    return n1*n2

@register.filter
def shorttime(str):
    """Shorten a timesince entry, to lop off a second unit of time."""
    last_comma = str.find(",")
    if last_comma == -1:
        return str
    else:
        return str[:last_comma]

@register.filter
def reasonabletime(time,time_units=False):
    """Take a time in hours, and return a nice string."""
    # print "time_units: %s" % (time_units)

    if time_units == False:
        if time < 1:
            timeval = int(time*60)
            plural_string = ""
            if timeval != 1:
                plural_string = _("s")
            return "%s %s%s" % (timeval, _("minute"), plural_string)
        elif time < 24:
            timeval = int(time)
            plural_string = ""
            if timeval != 1:
                plural_string = _("s")
            return "%s %s%s" % (timeval, _("hour"), plural_string)
        elif time < 24*7:
            timeval = int(time/24)
            plural_string = ""
            if timeval != 1:
                plural_string = _("s")
            return "%s %s%s" % (timeval, _("day"), plural_string)
        elif time < 24*7*365:
            timeval = int(time/(24*7))
            plural_string = ""
            if timeval != 1:
                plural_string = _("s")
            return "%s %s%s" % (timeval, _("week"), plural_string)
        else:
            timeval = int(time/(24*7*365))
            plural_string = ""
            if timeval != 1:
                plural_string = _("s")
            return "%s %s%s" % (timeval, _("year"), plural_string)
    elif time_units == None:
        # default to hours
        return "%s %s" % (round(time), _("hours"))

    else:
        # handle what we're given
        timeval = int(time)
        plural_string = ""
        if timeval != 1:
            plural_string = _("s")
        if time_units == 1:
            return "%s %s%s" % (int(time), _("minute"), plural_string)
        elif time_units == 2:
            return "%s %s%s" % (int(time), _("hour"), plural_string)
        elif time_units == 3:
            return "%s %s%s" % (int(time), _("day"), plural_string)
        elif time_units == 4:
            return "%s %s%s" % (int(time), _("week"), plural_string)
        elif time_units == 5:
            return "%s %s%s" % (int(time), _("year"), plural_string)


@register.filter
def pretty_timesince(this_date):
    if not hasattr(this_date,"hour"):
        this_date = datetime.datetime.combine(this_date,datetime.time())
    try:
        if datetime.datetime.now() - this_date < datetime.timedelta(minutes=1):
            return _("a few seconds ago")
        if this_date > datetime.datetime.now() - datetime.timedelta(days=14):
            return shorttime(timesince(this_date)) + _(" ago")
        else:
            return date(this_date)
    except:
        from qi_toolkit.helpers import print_exception
        print_exception()
        return date(this_date)

def _to_frac(x, maxdenom=10): 
    """ 
    Convert x to a common fraction. 
     
    Chooses the closest fraction to x with denominator <= maxdenom. 
    If x is closest to an integer, return that integer; otherwise, 
    return an (integer, numerator, denominator) tuple. 
    """ 
     
    assert x >= 0, "_to_frac only works on positive numbers." 
     
    intpart = int(x) 
    x -= intpart 
     
    bestfrac = 0,1 
    mindiff = x 
     
    for denom in range(1,maxdenom+1): 
        # for each denominator, there are two numerators to consider: 
        # the one below x and the one above x 
        for num in (int(x*denom), int(x*denom+1)): 
            diff = abs(float(num)/denom - x) 
             
            # compare using '<' rather than '<=' to ensure that the 
            # fraction with the smallest denominator is preferred 
            if diff < mindiff: 
                bestfrac = num, denom 
                mindiff = diff 
     
    if bestfrac[0] == 0: 
        return intpart 
    elif mindiff >= 1-x: 
        return intpart+1 
    else: 
        return intpart, bestfrac[0], bestfrac[1] 
 
 
_frac_entities = {(1,4): "&frac14;", (1,2): "&frac12;", (3,4): "&frac34;", 
    (1, 3): "&#x2153;", (2, 3): "&#x2154;", 
# browser support for fifths and sixths is incomplete, so we don't use them by default 
#   (1, 5): "&#x2155;", (2, 5): "&#x2156;", (3, 5): "&#x2157;", (4, 5): "&#x2158;", 
#   (1, 6): "&#x2159;", (5, 6): "&#x215A;", 
    (1, 8): "&#x215B;", (3, 8): "&#x215C;", (5, 8): "&#x215D;", (7, 8): "&#x215E;"} 
 
def html_fraction (number, maxdenom=10, useUnicode=True): 
    """ 
    Convert a float to a common fraction (or an integer if it is closer). 
     
    If the output is a fraction, the fraction part is wrapped in a span 
    with class "fraction" to enable styling of fractions. 
     
    If useUnicode is true, unicode entities will be used where available. 
    """ 
    try:
        number = float(number) 
        frac = _to_frac(abs(number), maxdenom) 
     
        if type(frac) == int: 
            string = str(frac) 
        else: 
            intpart, numerator, denominator = frac 
            if useUnicode and (numerator, denominator) in _frac_entities: 
                fracpart = _frac_entities[(numerator, denominator)] 
            else: 
                fracpart = (('<span class="fraction">' + 
                             '<span class="numerator">%i</span>&#x2044;' +  
                             '<span class="denominator">%i</span></span>') % 
                            (numerator,denominator)) 
            if intpart == 0: 
                string = fracpart 
            else: 
                string = str(intpart) + fracpart 
     
        if number < 0: 
            return '-'+string 
        else: 
            return string
    except:
        return ""
register.filter(html_fraction) 
 
def text_fraction (number, maxdenom=10): 
    """Convert a float to a common fraction (or integer if it is closer).""" 
     
    number = float(number) 
    frac = _to_frac(abs(number), maxdenom) 
     
    if type(frac) == int: 
        string = str(frac) 
    else: 
        intpart, numerator, denominator = frac 
        if intpart == 0: 
            string = '%i/%i' % frac[1:] 
        else: 
            string = '%i %i/%i' % frac 
     
    if number < 0: 
        return '-'+string 
    else: 
        return string 
register.filter(text_fraction)