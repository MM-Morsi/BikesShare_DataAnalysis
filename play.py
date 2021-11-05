import time
import pandas as pd
import numpy as np
import datetime

# explorations
# import the three files
chicago = pd.read_csv('./chicago.csv')
newyork = pd.read_csv('./new_york_city.csv')
washington = pd.read_csv('./washington.csv')

weekdays = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}

def getDay(text):
    day_num = int(text.split("-")[2]);
    month_num = int (text.split("-")[1]);
    year = int (text.split("-")[0]);
    day_num = datetime.date(year, month_num, day_num).weekday()
    return weekdays[day_num]

def getMonth(text):
    month_num = text.split("-")[1];
    datetime_object = datetime.datetime.strptime(month_num, "%m")
    month_name = datetime_object.strftime("%B")
    return month_name;

def getStartHour(text):
    text = int (text.split(":")[0]);
    return text

def getData(df, Month, Day):
    if(Month == "all" and Day == "all"):
        return df;
    elif(Month == "all"):
        df = df[df['day']==Day];
        # get days 
        return df;
    elif(Day == "all"):
        df = df[df['month']==Month];
        # get Month
        return df;
    else:
        df = df[df['day']==Day];
        df = df[df['month']==Month];
        # wants spesific day and month 
        return df;

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Loading the df
    path = ""
    if(city == "washington" or city == "chicago"):
        path = "./" + city + ".csv";
    elif(city == "new york city"):
        path = "./" + "new_york_city" + ".csv";
    df = pd.read_csv(path);
    # Adding day and month columns to df
    df_split = df['Start Time'].str.split(' ', expand=True);
    df_series = df_split[0].apply(getDay);
    df = df.assign(day = df_series);
    df_series = df_split[0].apply(getMonth);
    df = df.assign(month = df_series);
    # add a seperate column for start hour - 
    df_split = df['Start Time'].str.split(' ', expand=True);
    df_series = df_split[1].apply(getStartHour)
    df = df.assign(start_hour = df_series)
    # combination of start and end stations - travel time
    df = df.assign(combination = df['Start Station'] + " - " + df['End Station'])
    # return the data in data frame 
    df = getData(df, month, day);
    return df

test = load_data("chicago", "June", "all")
# print(test['End Station'].mode())
# print("most commonly used start station is:", test['Start Station'].value_counts().idxmax())

# display most commonly used end station
# print("most commonly used end station is:", test['End Station'].value_counts().idxmax())
# print("most frequent combination of start station and end station trip is:", test['combination'].value_counts().idxmax())
# print(load_data("chicago", "June", "Saturday"))
# print(load_data("new york city", "all", "all"))

print(test.columns)
# print("Number of males is: ", test['Gender'].value_counts()[0])
# print(test['start_hour'].value_counts().idxmax())
# print(test['Trip Duration'].sum())
# print(test['Trip Duration'].mean())
# print(test['Gender'].value_counts()[0])
# if('Gender' in test.columns):
#     print("Number of males is: ", test['Gender'].value_counts()[0])
#     print("Number of males is: ", test['Gender'].value_counts()[1])
print(test['Birth Year'].min())
print(test['Birth Year'].max())
print(test['Birth Year'].value_counts().idxmax())

