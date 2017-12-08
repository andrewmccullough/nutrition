import sqlite3, os, time, functions, sys, datetime
from connect import *
from functions import width as width, today as today

def setup (passback = False):
    global name

    os.system("clear")
    print("Welcome!")
    functions.bar (width)
    functions.thinking ()

    name = input("What's your first name? > ").strip()
    functions.bar (width)
    functions.thinking ()

    print("Hello, " + name + "!")
    functions.thinking ()

    print("I just need to get some information about you.")
    functions.bar (width)
    functions.thinking ()

    gender = None
    while gender not in ["male", "female"]:
        gender = input("What's your gender? > ").lower().strip()

        if gender in ["m", "man", "boy", "male"]:
            gender = "male"
        elif gender in ["w", "f", "woman", "girl", "female"]:
            gender = "female"
        else:
            print("I didn't get that. Can you rephrase it?")

    age = None
    while age == None:
        try:
            age = int(input("How old are you? > "))
        except ValueError:
            print("Please enter a number.")

    metric = None
    while metric not in [True, False]:
        metric = input("Do you want to use metric measurements? > ").lower().strip()

        if metric in ["yes", "y", "yeah"]:
            metric = True
        elif metric in ["no", "n", "nah"]:
            metric = False
        else:
            print("I didn't get that. Can you rephrase it?")

    functions.bar (width)

    height = None
    while height == None:

        if metric:
            try:
                print("Enter your height in centimeters.")
                height = int(input("> "))
            except ValueError:
                print("Please enter a number.")
        else:
            try:
                print("Enter your height in feet and inches, separated by a space.")
                print("e.g., 5 feet, 11 inches = 5 11")

                height = [ int(y) for y in input("> ").split() ]
                if height[0] not in list(range(4, 8)) or height[1] not in list(range(0, 12)):
                    height = None
                    print("Please enter your height in the proper format.")
                else:
                    height = height[0] * 12 + height[1]
            except ValueError:
                print("Please enter your height in the proper format.")

    functions.bar (width)
    weight = None
    while weight == None:

        if metric:
            try:
                print("Enter your weight in kilograms.")
                weight = int(input("> "))
            except ValueError:
                print("Please enter a number.")
        else:
            try:
                print("Enter your weight in pounds.")
                weight = int(input("> "))
            except ValueError:
                print("Please enter a number.")

    cur.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?)", [name, gender, age, metric, weight, height])
    conn.commit()
    functions.bar (width)
    functions.thinking ()
    print("Alright! Now we can get to work.")
    functions.bar (width)
    functions.thinking ()

    BMI, health = functions.BMIcalculator (metric, weight, height)

    print("Your BMI is " + str(round(BMI, 1)) + ". According to this metric, you are " + health + ".")
    functions.bar (width)
    functions.thinking ()

    print("You've finished setting up your profile. You won't have to do it again.")
    functions.thinking ()

    print("Let's get started!")
    functions.bar (width)
    functions.thinking (3)

    if passback:
        home ()

def home ():
    cur.execute("SELECT * FROM history WHERE date = ?", [today])
    entry = cur.fetchone()
    calories, protein = entry[1], entry[2]

    os.system("clear")

    functions.bar (width)

    print("Welcome, " + name + "!")
    print("You've eaten " + str(calories) + " calories and " + str(protein) + " grams of protein today.")

    functions.bar (width)

    print("What would you like to do?")

    # functions.bar (width)

    i = 0
    options = ["change profile", "add calories", "add protein", "calculate BMI"]
    for option in options:
        i += 1
        print(" (" + str(i) + ") " + option)
    print("  or [exit]")

    functions.bar (width)

    selection = input("> ").strip().lower()

    if selection in ["exit", "end", "quit"]:
        os.system("clear")
        sys.exit()
    else:
        try:
            selection = int(selection)
            if selection not in list(range(0, i + 1)):
                print("Please enter a valid number.")
                functions.thinking ()
                home ()
            else:
                if options[selection - 1] == "change profile":

                    functions.bar (width)
                    print("This will erase your existing profile.")
                    functions.bar (width)

                    confirm = input("Are you sure you wish to continue? > ").strip().lower()
                    if confirm in ["yes", "y", "yeah"]:
                        cur.execute("DELETE FROM user")
                        # conn.commit()
                        setup (True)
                    else:
                        home ()
                elif options[selection - 1] == "add calories":
                    functions.thinking ()
                    addcalories ()
                elif options[selection - 1] == "add protein":
                    functions.thinking ()
                    addprotein ()
                elif options[selection - 1] == "calculate BMI":
                    functions.thinking ()
                    calculateBMI ()
        except ValueError:
            print("Please enter a valid number.")
            functions.thinking ()
            home ()

def calculateBMI ():
    os.system("clear")

    cur.execute("SELECT metric, weight, height FROM user")
    entry = cur.fetchone()
    metric, weight, height = entry[0], entry[1], entry[2]

    BMI, health = functions.BMIcalculator (metric, weight, height)

    functions.bar (width)

    print("Your BMI is " + str(round(BMI, 1)) + ". According to this metric, you are " + health + ".")

    functions.bar (width)

    input("Press return to go home. > ")
    functions.thinking ()
    home ()

def addcalories ():
    os.system("clear")

    cur.execute("SELECT * FROM history WHERE date = ?", [today])
    entry = cur.fetchone()
    calories, protein = entry[1], entry[2]

    functions.bar (width)
    print("You've eaten " + str(calories) + " calories and " + str(protein) + " grams of protein today.")
    functions.bar (width)

    try:
        add = int(input("How many calories should be added? > "))
        cur.execute("UPDATE history SET calories = ? WHERE date = ?", [add + calories, today])
        conn.commit()
        functions.thinking ()
        home ()
    except ValueError:
        print("Please enter a valid number.")
        functions.thinking ()
        addcalories ()

def addprotein ():
    os.system("clear")

    cur.execute("SELECT * FROM history WHERE date = ?", [today])
    entry = cur.fetchone()
    calories, protein = entry[1], entry[2]

    functions.bar (width)
    print("You've eaten " + str(calories) + " calories and " + str(protein) + " grams of protein today.")
    functions.bar (width)

    try:
        add = int(input("How many grams of protein should be added? > "))
        cur.execute("UPDATE history SET protein = ? WHERE date = ?", [add + protein, today])
        conn.commit()
        functions.thinking ()
        home ()
    except ValueError:
        print("Please enter a valid number.")
        functions.thinking ()
        addprotein ()

name = functions.startup ()

if not name:
    setup ()
else:
    name = name[0]

cur.execute("SELECT * FROM history WHERE date = ?", [today])
entry = cur.fetchone()

if not entry:
    cur.execute("INSERT INTO history VALUES (?, 0, 0)", [today])
    conn.commit()

home ()
