import os, time, datetime
from connect import *

def startup ():
    cur.execute("CREATE TABLE IF NOT EXISTS user (name TEXT, gender TEXT, age INT, metric INT DEFAULT 0, weight INT, height INT)")
    cur.execute("CREATE TABLE IF NOT EXISTS history (date DATE, calories INT, protein INT)")

    cur.execute("SELECT name FROM user")
    name = cur.fetchone()

    return name

def window ():
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

    return int(cr[1]), int(cr[0])

def thinking (t = 1.5):
    print(" . ", end = "\r")
    time.sleep(t / 3)
    print(" .. ", end = "\r")
    time.sleep(t / 3)
    print(" ... ", end = "\r")
    time.sleep(t / 3)

def bar (width):
    print("=" * width)

def BMIcalculator (metric, weight, height):
    if metric:
        BMI = weight / (height / 100) ** 2
    else:
        BMI = weight / height ** 2 * 703

    if BMI < 18.5:
        health = "underweight"
    elif BMI >= 18.5 and BMI < 25:
        health = "healthy"
    elif BMI >= 25 and BMI < 30:
        health = "overweight"
    elif BMI >= 30:
        health = "obese"

    return BMI, health

width, height = window ()

now = datetime.datetime.today()
today = now.strftime("%Y-%m-%d")
