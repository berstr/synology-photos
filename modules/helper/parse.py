import os
import re
from datetime import datetime #, timezone
import pytz

def parse_filename(pathname):
    basename = os.path.basename(pathname)
    p='^([0-9]{4,4})\-([0-9][0-9])\-([0-9][0-9])\-([0-9][0-9])([0-9][0-9])\-([0-9]{4,4})\.(.*)$'
    m = re.match(p,basename)
    if m == None:
        temp = basename.split('.')
        result = {  
                'result':'invalid item filename: {} - allowed: YYYY-MM-DD-hhmm-ssxx.<ext>  (with x being a number 0-9)'.format(pathname),
                'filename':pathname,
                'extension':temp[1]
        }
    else:
        #filename=m.group(0)
        year = m.group(1)
        month=m.group(2)
        day=m.group(3)
        hour=m.group(4)
        minute=m.group(5)
        second = m.group(6)[:2]
        index=m.group(6)[:2]
        extension=m.group(7)
        date = "{}-{}-{} {}:{}:{}".format(year,month,day,hour,minute,second)
        #time = datetime.strptime("{}-{}-{} {}-{}-{}".format(year,month,day,hour,minute,seconds), "%Y-%m-%d %H-%M-%S")
        #utc = pytz.UTC
        #time = time.astimezone(utc)
        #timestamp = int(datetime.timestamp(time))
        #result = {'result':'ok', 'filename':pathname, 'time':timestamp, 'year':year, 'month':month,'day':day,'hour':hour,'minute':minute,'seconds':seconds,'index':index,'extension':extension}
        result = {'result':'ok', 'filename':pathname, 'date':date, 'year':year, 'month':month,'day':day,'hour':hour,'minute':minute,'second':second,'index':index,'extension':extension}
    return result

    