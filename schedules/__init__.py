import math
from datetime import date
import schedule
from threading import Thread
from time import sleep

from playsound import sound

def atan(i):
    return math.atan(i)
def acos(i):
    return math.acos(i)
def sin(i):
    return math.sin(i)
def cos(i):
    return math.cos(i)
def tan(i):
    return math.tan(i)
def asin(i):
    return math.asin(i)
def floor(i):
    return math.floor(i)
def  degToRad( degree):
    return ((3.1415926 / 180) * degree)
# convert Radian to Degree
def radToDeg( radian):
    return (radian * (180 / 3.1415926));
# make sure a value is between 0 and 360
def moreLess360( value):
  while (value > 360 or value < 0):
    if (value > 360):
        value -= 360
    elif (value < 0):
        value += 360
  return value
def moreLess24(value):
  while (value > 24 or value < 0):
    if (value > 24):
        value -= 24
    elif (value < 0):
        value += 24
  return value


def doubleToHrMin(number):
    d=[]
    hour_ = floor(moreLess24(number))
    minutes_ = floor(moreLess24(number - hour_) * 60)
    d.append(hour_)
    d.append(minutes_)
    return d

def calcPrayerTimes(year,month,day,longitude,latitude,timeZone,fajrTwilight,ishaTwilight):
    prayer_time=[]
    D1 = (367 * year) - ((year + int((month + 9) / 12)) * 7 / 4) + ((int(275 * month / 9)) + day - 730531.5)
    L = 280.461 + 0.9856474 * D1
    L = moreLess360(L)
    M = 357.528 + (0.9856003) * D1
    M = moreLess360(M)
    Lambda = L + 1.915 * sin(degToRad(M)) + 0.02 * sin(degToRad(2 * M))
    Lambda = moreLess360(Lambda)
    Obliquity = 23.439 - 0.0000004 * D1
    Alpha = radToDeg(atan((cos(degToRad(Obliquity)) * tan(degToRad(Lambda)))))
    Alpha = moreLess360(Alpha)
    Alpha = Alpha - (360 * int(Alpha / 360))
    Alpha = Alpha + 90 * (floor(Lambda / 90) - floor(Alpha / 90))
    ST = 100.46 + 0.985647352 * D1
    Dec = radToDeg(asin(sin(degToRad(Obliquity)) * sin(degToRad(Lambda))))
    Durinal_Arc = radToDeg(acos((sin(degToRad(-0.8333)) - sin(degToRad(Dec)) * sin(degToRad(latitude))) / (cos(degToRad(Dec)) * cos(degToRad(latitude)))))
    Noon = Alpha - ST
    Noon = moreLess360(Noon)
    UT_Noon = Noon - longitude

    # // 2) ZuhrTime[Localnoon]
    zuhrTime1 = UT_Noon / 15 + timeZone
    Asr_Alt = radToDeg(atan(2 + tan(degToRad(latitude - Dec))))
    Asr_Arc = radToDeg(acos((sin(degToRad(90 - Asr_Alt)) - sin(degToRad(Dec)) * sin(degToRad(latitude))) / (cos(degToRad(Dec)) * cos(degToRad(latitude)))))
    Asr_Arc = Asr_Arc / 15
     # 3) Asr Time
    asrTime1 = zuhrTime1 + Asr_Arc-1
    # // 1) Shorouq Time
    sunRiseTime1 = zuhrTime1 - (Durinal_Arc / (15))
    # // 4) MaghribTime
    maghribTime1 = zuhrTime1 + (Durinal_Arc / (15))
    Esha_Arc = radToDeg(acos((sin(degToRad(ishaTwilight)) - sin(degToRad(Dec)) * sin(degToRad(latitude))) / (cos(degToRad(Dec)) * cos(degToRad(latitude)))))
    # // 5) IshaTime
    ishaTime1 = zuhrTime1 + (Esha_Arc / 15)
    # // 0) FajrTime
    Fajr_Arc = radToDeg(acos((sin(degToRad(fajrTwilight)) - sin(degToRad(Dec)) * sin(degToRad(latitude))) / (cos(degToRad(Dec)) * cos(degToRad(latitude)))))
    fajrTime1 = zuhrTime1 - (Fajr_Arc / 15)

    prayer_time.append(fajrTime1)
    prayer_time.append(sunRiseTime1)
    prayer_time.append(zuhrTime1)
    prayer_time.append(asrTime1)
    prayer_time.append(maghribTime1)
    prayer_time.append(ishaTime1)
    return prayer_time

class Schedules():
    fajrTwilight = -18.5
    ishaTwilight = -17.35

    def __init__(self,l,lng,tz):
        currdate = date.today()
        self.prayer_times = dict()

        calculated = calcPrayerTimes(year=currdate.day,month=currdate.month,day=currdate.day,
                            longitude=lng,latitude=l,timeZone=tz,
                            fajrTwilight=self.fajrTwilight,ishaTwilight=self.ishaTwilight)
      
        # Fajr SunRise Zuhar Asr Maghrib Isha
        names = ["Fajr","Zuhar","Asr","Maghrib","Isha"]

        # remove sunrise
        calculated.pop(1)

        for i in range(len(calculated)):
            self.prayer_times[names[i]] = doubleToHrMin(calculated[i])

    def playAzan(self):
        sound.play("sound/azan.mp3", True)

    def run_schedule(self):
        while True:
            schedule.run_pending()
            sleep(1)

    def schedule_prayers(self):
        for k in self.prayer_times.keys():
            hh = f"{self.prayer_times[k][0]}"
            mm = f"{self.prayer_times[k][1]}"

            if len(hh) == 1:
                hh = '0' + hh
            if len(mm) == 1:
                mm = '0' + mm
          
            schedule.every().day.at(hh+":"+mm).do(self.playAzan)
        schedule.every().day.at("21:36").do(self.playAzan)
        t = Thread(target=self.run_schedule, daemon=True)
        t.start()
