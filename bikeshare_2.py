import time
import datetime
import pandas as pd
from pandas.tseries.offsets import DateOffset
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
Months = set(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
Month_dict = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}
Days = set(['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
weekdays = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}

def getMonth(text):
    month_num = text.split("-")[1];
    datetime_object = datetime.datetime.strptime(month_num, "%m")
    month_name = datetime_object.strftime("%B")
    return month_name;

def getDay(text):
    day_num = int(text.split("-")[2]);
    month_num = int (text.split("-")[1]);
    year = int (text.split("-")[0]);
    day_num = datetime.date(year, month_num, day_num).weekday()
    return weekdays[day_num]

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


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!');
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    looping = True
    city = ""
    print("Please enter the city you wish to explore: chicago, new york city, washington")

    while(looping):
        # print("in while")
        city = input()
        if(city == "chicago" or city == "new york city" or city == "washington"):
            looping = False
        else:
            print("Please enter one of the three cities")
            looping = True

    
    # get user input for month (all, january, february, ... , june)
    print("Do you wish to enter a month? enter yes or no please")
    month_fetch = input()
    if(month_fetch == "yes"):
        looping = True
        month = ""
        print("Please enter the month name in the format: Januray - February ... etc. ")
        while(looping):
            # print("in while")
            month = input()
            if(month in Months):
                looping = False
            else:
                print("Please enter a valid month name")
                looping = True
    else:
        month = "all"

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print("Do you wish to enter a day? enter yes or no please")
    day_fetch = input()
    if(day_fetch == "yes"):
        looping = True
        day = ""
        print("Please enter the day name in the format: Saturday - Sunday ... etc. ")
        while(looping):
            # print("in while")
            day = input()
            if(day in Days):
                looping = False
            else:
                print("Please enter a valid day name")
                looping = True
    else:
        day = "all"
    print('-'*40)
    return city, month, day

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

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("most common month is ", df['month'].value_counts().idxmax())

    # display the most common day of week
    print("most common day of week is ", df['day'].value_counts().idxmax())

    # display the most common start hour
    print("most common start hour is ", df['start_hour'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("most commonly used start station is ", df['Start Station'].value_counts().idxmax())
    
    # display most commonly used end station
    print("most commonly used end station is ", df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    print("most frequent combination of start station and end station trip is ", df['combination'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("total travel time is: ", df['Trip Duration'].sum())

    # display mean travel time
    print("mean travel time is: ", df['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Number of Subscribers is: ", df['User Type'].value_counts()[0])
    print("Number of Customers is: ", df['User Type'].value_counts()[1])

    # Display counts of gender
    if('Gender' in df.columns):
        print("Number of males is: ", df['Gender'].value_counts()[0])
        print("Number of males is: ", df['Gender'].value_counts()[1])

    # Display earliest, most recent, and most common year of birth
    if('Birth Year' in df.columns):
        print("The earliest year of birth is: ", df['Birth Year'].min())
        print("The most recent year of birth is: ", df['Birth Year'].max())
        print("The most common year of birth is: ", df['Birth Year'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()    #done
        df = load_data(city, month, day)    #done

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
