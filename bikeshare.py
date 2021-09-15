import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("ًWould you like to see data for chicago, new york city, or washington?\n").lower()
        if city not in CITY_DATA.keys():
            print('Please enter correct city name!')
        else:
            # city name is correct exists in CITY_DATA
            break
    
    # user select which to filter by
    filter_by_list = ['month', 'day', 'both', 'none']
    while True:
        filter_by = input("Would you like to filter the data by month, day, both, or not at all? Type \"none\" for no time filter.\n").lower()
        if filter_by not in filter_by_list:
            print('please enter correct filter!')
        else:
            #correct filter
            break

    if filter_by == 'month':
        day = 'none'
        # TO DO: get user input for month (all, January, February, March, April, May, or June)
        while True:
            month = input("Which month? January, February, March, April, May, or June or all?\n").lower()
            if month not in months:
                print('Please enter correct month!')
            else:
                break
    elif filter_by == 'day':
        month = 'none'
        # TO DO: get user input for day of week (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday)
        while True:
            day = input("Which day? (monday, tuesday, wednesday, thursday, friday, saturday, sunday) or all? \n").lower()
            if day not in days:
                print('Please enter correct day!')
            else:
                break
    elif filter_by == 'both':
        # TO DO: get user input for month (all, January, February, March, April, May, June)
        while True:
            month = input("Which month? January, February, March, April, May, or June or all?\n").lower()
            if month not in months:
                print('Please enter correct month!')
            else:
                break
        # TO DO: get user input for day of week (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday)
        while True:
            day = input("Which day? (monday, tuesday, wednesday, thursday, friday, saturday, sunday) or all? \n").lower()
            if day not in days:
                print('Please enter correct day!')
            else:
                break
    elif filter_by == 'none':
        month = 'all'
        day = 'all'
        
    # display the first five rows of data
    while True:
        display_head = input('Would you like to display the first five rows of data? yes/no \n').lower()
        if display_head not in ['yes', 'no']:
            print('Please enter yes or no!')
        else:
            break

    print('-'*40)
    return city, month, day, display_head


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
    # read the correct dataset according to city in the dictionary
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    #extract hour
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if (month != 'all') & (month != 'none'):
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if (day != 'all') & (day != 'none'): 
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def display_rows(df, display_head):
    """display first five rows in df."""
    if display_head == 'yes':
        pd.set_option('display.max_columns', None) # to show all columns
        print('The first five rows:\n')
        print(df.head(5))
    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('\nThe Most Common Month is: {}'.format(common_month))

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('\nThe Most Common Month is: {}'.format(common_day))

    # TO DO: display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('\nThe Most Common Hour is: {}'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('\nThe Most Common start station is: {}'.format(common_start_station))

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('\nThe Most Common end station is: {}'.format(common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    common_combine_station = df.groupby(['Start Station', 'End Station'])['Trip Duration'].count().idxmax()
    print('\nThe Most Common combined station (Trip) is: {} to {}'.format(common_combine_station[0], common_combine_station[1]))
    
    #another way for common combined station
    common_combine_station = (df['Start Station'] + '-' + df['End Station']).mode()[0]
    print('\nThe Most Common combined station (Trip) is: {}'.format(common_combine_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nThe Total Trip Duration is: {} seconds'.format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nThe Mean Trip Duration is: {} seconds'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('counts of user types:\n', df['User Type'].value_counts())
    
    # no Gender column in washington
    if 'Gender' in df.columns:
        # TO DO: Display counts of gender
        print('counts of gender:\n', df['Gender'].value_counts())
        
    # no birth year in washington
    if 'Birth Year' in df.columns:
        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_birthyear = df['Birth Year'].min()
        print('\nThe earliest year of birth is: {}'.format(earliest_birthyear))

        recent_birthyear = df['Birth Year'].max()
        print('\nThe most recent year of birth is: {}'.format(recent_birthyear))

        common_birthyear = df['Birth Year'].mode()[0]
        print('\nThe most common year of birth is: {}'.format(common_birthyear))
        
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day, display_head = get_filters()
        df = load_data(city, month, day)
        display_rows(df, display_head)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
