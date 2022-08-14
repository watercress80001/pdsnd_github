import time
import pandas as pd
import numpy as np
import sys
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

sorry = "Sorry, that isn't an option."

def redo_or_quit(prompt,list):
    """
    Prompts user to re-enter input if the previously entered input isn't in the provided list
    Loops indefinitely until the user enters valid input or elects not to continue (i.e. 
    decides not to try anymore).

    Returns:
        (str) actual text varies, depending on the prompt
    """
    try: 
        filter = input(prompt).lower()
        while filter not in list:
            print('\n',sorry)
            options = input("Would you like to continue [Yes/No]? ").lower()
            if options == 'no':
                quit()
            else:
                if options.lower() == 'yes':
                    filter = input(prompt).lower()
        else:
            return filter
    except:
        print('Sorry, there\'s an issue with your input.')

def get_filters(): 
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = None
    month = None
    day = None
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun','all']
    days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun','all']


    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city
    city_prompt = "Would you like to see data for Chicago, New York City, or Washington? "
    city = redo_or_quit(city_prompt,['chicago','new york','new york city','washington'])

    if city == 'new york':
        city = 'new york city'

    print("Gathering data for {}...".format(city.title()))

    # get user input for month (all, january, february, ... , june)
    month_prompt = "Which month: Jan, Feb, Mar, Apr, May, Jun or all?\nPlease type your choice as listed: "
    month = redo_or_quit(month_prompt,months)
    if month == 'all':
        print('Filtering for all months...')
    else:
        print('Filtering for {}...'.format(month.title()))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_prompt = "Which day - Mon, Tue, Wed, Thu, Fri, Sat, Sun or all?\n Please type the abbreviated day name: "
    day = redo_or_quit(day_prompt,days)
    if day == 'all':
        print('Filtering for all days...')
    else:
        print('Filtering for {}...'.format(day.title()))

    print('-'*40)
    return city, month, day #all lower()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
        top_month_all - variable indicating the most common month number (int)
        top_day_all - variable indicating the most common weekday (str)
    """
    df = pd.read_csv(CITY_DATA[city])

    #clean up dates and make month and day of week columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%a")
    top_month_all = df['month'].mode()[0] #int
    top_day_all = df['day_of_week'].mode()[0] #str

    #filter based on month or date
    if month not in ['all', None]:
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month)+1 #convert str to int
        df = pd.DataFrame(df[df['month']== month])

    if day not in ['all', None]:
        df = pd.DataFrame(df[df['day_of_week'] == day.title()])
    #return filtered dataset
    return df, top_month_all, top_day_all #dataframe, int, str


def time_stats(df, month, day, top_month_all, top_day_all): #reviewed
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating the most frequent travel times...\n')
    start_time = time.time()

    # display the most common month
    months = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun'}
    top_month = months[df['month'].mode()[0]]
    top_month_all = months[top_month_all] #convert int to str

    if month in ['all', None]:
        print('The most popular month for a ride is {}.'.format(top_month.title()))
    elif top_month.lower() == top_month_all.lower():
        print('The most popular month for a ride is the selected month, {}.'.format(top_month.title()))
    else:
        print('The selected month is {} but the most popular month for a ride is {}.'.format(top_month.title(),top_month_all.title()))

    # display the most common day of week
    top_day = df['day_of_week'].mode()[0]

    if day in ['all', None]:
        print('The most popular day for a ride is {}.'.format(top_day))
    elif top_day.lower() == top_day_all.lower():
        print('The most popular weekday for a ride is the selected day, {}.'.format(top_day.title()))
    else:
        print('The selected weekday is {} but the most popular day for a ride is {}.'.format(top_day,top_day_all))

    # display the most common start hour
    top_hour = df['Start Time'].dt.hour.mode()[0]
    print('The most popular hour to start a trip is {}.'.format(top_hour))

    # display the most common end hour
    top_end_hr = df['End Time'].dt.hour.mode()[0]
    print('The most common hour to end a trip is {}.'.format(top_end_hr))

    # display processing time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating the most popular stations/trips...\n')
    start_time = time.time()

    # display most commonly used start station
    top_start_station = df['Start Station'].mode()[0]
    print("The most popular start station is at {}.".format(top_start_station))

    # display most commonly used end station
    top_end_station = df['End Station'].mode()[0]
    print("The most popular ending station is at {}.".format(top_end_station))

    # display most frequent combination of start station and end station trip
    df['start_stop'] = df['Start Station']+' to '+df['End Station']
    print('The most popular start/end station combination is from {}.'.format(df['start_stop'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time. seconds converted to days, hours:min:seconds
    tot_duration_secs = float(df["Trip Duration"].sum())
    tot_duration = str(dt.timedelta(seconds = tot_duration_secs))
    print('Total time for all trips (days, hh:mm:ss) is {}.'.format(tot_duration.split(".")[0]))

    # display mean travel time. seconds converted to hours:min:seconds
    avg_duration_secs = df['Trip Duration'].mean()
    avg_duration = str(dt.timedelta(seconds = avg_duration_secs))
    print('The average time per trip (hh:mm:ss) is {}.'.format(avg_duration.split(".")[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating user stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("The breakdown of users by type is:\n",user_types.to_string())

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_type = df['Gender'].value_counts()
        print("\nThe breakdown of users by gender is:\n",gender_type.to_string())
    else:
        print("\nGender data wasn't recorded for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_yr = int(df['Birth Year'].min())
        recent_yr = int(df['Birth Year'].max())
        common_yr = int(df['Birth Year'].mode())
        current_yr = dt.date.today().year
        print("\nThe ealiest birth year in this city is {}, the most recent is {}, and the most common is {}.".format(earliest_yr,recent_yr,common_yr))
        print("This means riders range from {} to {} years old. The most common age is {}.".format(current_yr-earliest_yr, current_yr-recent_yr,current_yr-common_yr))
    else:
        print("Birth year data wasn't recorded for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def read_raw(city):
    """ Prints out the raw csv file, 5 lines at a time, for the user to review
       only the relevant city is printed. """

    prompt = 'Would you like to see the raw data? [Yes/No] '
    wanna_read = redo_or_quit(prompt,['yes','no'])

    while wanna_read.lower() == 'yes':
        bgin = 0
        ends = 5
        row_num = 1
        keep_going = 'yes'

        while keep_going.lower() == 'yes':
            with open(CITY_DATA[city]) as f:
                city_lines = f.readlines()
            if ends >= len(city_lines):
                for line in city_lines[bgin:]:
                    print(row_num,line.strip())
                    row_num += 1
                print('End of file reached.')
                continue
            else:
                for line in city_lines[bgin:ends]:
                    print(row_num,line.strip())
                    row_num += 1
            bgin = ends+1
            ends += 6
            prompt = 'Read the next 5 rows? [Yes/No] '
            keep_going = redo_or_quit(prompt,['yes','no'])
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df, top_month_all, top_day_all = load_data(city, month, day)

        time_stats(df, month, day, top_month_all, top_day_all)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        read_raw(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
        main()
