import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    """
    print('Created by Mike')
    print('Hello! Let\'s explore some US bikeshare data!\n')
    city = ''
    print('Choose which city to filter by: Chicago, New York City, Washington\n')
    while city not in CITY_DATA:
        city = input('Input: ').lower()
        if city not in CITY_DATA:
            print('Check input please. Input is not case sensitive.\n')
    print('Sucess, filtering data. You are filtering by: {}\n'.format(city).title())

    print('What month would you like to filter by: January, February, March, April, May, June, All \n')
    month = ''
    avail_months = {'january' : 0, 'february' : 1, 'march' : 2, 'april' : 3, 'may' : 4, 'june' : 5, 'all' : 6}
    month = input('Filter by month: ').lower()
    while month not in avail_months:
        print('Please type full month name, capitalization does not matter\n')
        month = input('Filter by month: January, February, March, April, May, June, All: ').lower().strip()
        '\n'
    if month in avail_months:
        print('Sucess, filtering by {}.\n'.format(month))
    day = ''
    avail_days = {'monday' : 0, 'tuesday' : 1, 'wednesday' : 2, 'thursday' : 3, 'friday' : 4,'saturday' : 5, 'sunday' : 6, 'all' : 7}
    while day not in avail_days:
        print('Please type full day name, capitilzation does not matter\n')
        day = input('Input day of week to filter by: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, All: ').lower()
    print('-'*40+ '\n\n')
    print('Filtering data by city: {}, month: {}, day: {}.\n\n'.format(city, month, day))
    print('-'*40+ '\n')
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
    df = pd.read_csv('{}.csv'.format(city).lower().replace(' ','_'))

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    else:
        df
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        df = df[df['day'] == day]
    else:
        df

    print('\n')
    print('Data header below\n')
    print(df.head())
    print('\n' + '-'*40)
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months = {1 : 'January', 2 : 'February', 3 : 'March', 4 : 'April', 5 : 'May', 6 : 'June'}

    """display the most common month if not filtered by month"""
    if month == 'all':
        most_common_month = df['month'].mode()[0]

        count_most_common_month = df['month'].value_counts().max()
        print('The month with the most uses was {} with a total of {}.'.format(months[most_common_month], count_most_common_month))
    else:
        print('Most common month stats will not show since the data is filtered by month')


    """display the most common day of week"""
    days = {0: 'monday', 1 : 'tuesday', 2 : 'wednesday', 3 : 'thursday', 4 : 'friday', 5 : 'saturday', 6 : 'sunday'}
    if day == 'all':

        most_common_day = df['day'].mode()[0]

        count_most_common_day = df['day'].value_counts().max()
        print('The day with the most uses was {} with a total of {}.\n'.format(days[most_common_day], count_most_common_day))
    else:
        print('Most common day stats will not show since the data is filtered by day.\n')

    """display the most common start hour"""
    df['start hour'] = df['Start Time'].dt.hour
    pop_start_hour = df['start hour'].mode()[0]
    print('The most popular hour of the day to start a rental was {} on the 24 hour clock.\n'.format(pop_start_hour))

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    """display most commonly used start station"""
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common start location is {}.\n'.format(most_common_start_station))


    """TO DO: display most commonly used end station"""
    most_common_end_station = df['End Station'].mode()[0]
    print('The most common end location is {}.\n'.format(most_common_end_station))

    """display most frequent combination of start station and end station trip"""
    df['start_end'] = df['Start Station'].str.cat(df['End Station'], sep=' and ending at ')
    start_end = df['start_end'].mode()[0]
    print('The most common route start and ending combination is Starting at {}.\n\n'.format(start_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    """display total travel time"""
    total_trip = df['Trip Duration'].sum()

    years = total_trip // 31536000
    months = (total_trip % 31536000) // 2628000
    weeks = ((total_trip % 31536000) % 2628000) // 604800
    days = (((total_trip % 31536000) % 2628000) % 604800) // 86400
    hours = ((((total_trip % 31536000) % 2628000) % 604800) % 86400) // 3600
    mins = (((((total_trip % 31536000) % 2628000) % 604800) % 86400) % 3600) // 60
    secs = (((((total_trip % 31536000) % 2628000) % 604800) % 86400) % 3600) % 60
    print('Total trip time is {} secs.\n{} years {} months {} week(s) {} days {} hours {} mins {} secounds.\n'.format(total_trip, years, months, weeks, days, hours, mins, secs))

    """display mean travel time"""
    mean_travel = df['Trip Duration'].mean()
    print('The average travel time was {} seconds.\n{} mins {} seconds\n\n'.format(mean_travel, mean_travel // 60, mean_travel % 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    """Display counts of user types"""
    user_type = df['User Type'].value_counts()
    print('Breakout of users by type below:\n')
    print(user_type)
    print('\n\n')


    """Display counts of gender"""
    if city == 'washington':
        print('No user stats of this type (gender or age).')
    else:
        print('Breakout of gender below:\n')
        gender = df['Gender'].value_counts()
        print(gender)


        """Display earliest, most recent, and most common year of birth"""
        oldest_user = df['Birth Year'].min()
        youngest_user = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()

        print('\n\n The earliest birthday among the users was {}, the most recent birth year is was {}, and the most common birth year was {}.\n'.format(oldest_user, youngest_user, common_birth))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Display 5 rows of data at a time"""
    responses = ['yes', 'no']
    view = 0
    response = input('Would you like to see the first 5 lines of the data?\n Input (yes or no): ').lower()
    while response not in  responses:
        print('Check response.')
        response = input('Would you like to see the first 5 lines of the data?\n Input (yes or no): ').lower()
    if response == 'yes':
        print(df.head())
    while response == 'yes':
        response = input('Would you like to see the next 5 lines of the data?\n Input (yes or no): ').lower()
        view += 5
        print(df[view : view +5])
        if response != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
