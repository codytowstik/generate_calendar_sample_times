#!/usr/bin/env python3

# Generate time samples at specified interval and probability.

# OUT_RESULTS_FILE_PATH     - Path to write tmp file containing result output

# START_TIME                - What datetime to start generating samples

# END_TIME                  - What datetime to stop generating samples

# TIME_SLICES_PER_DAY       - How many time per day should we possibly create a sample

# ODDS_OF_SAMPLE_PER_SLICE  - The odds of generating a sample at each time slice

# WEEKEND_ODDS_OF_SAMPLE_PER_SLICE - The odds of generating a sample at each weekend time slice

# Example:
#   I want an average of 1 sample per day, with a decent variance of samples per day
#   .. so I want 10 slices per day, at odds of 0.1 per slice
#   .. so every (24/10) ~= 2.4 hours I will have a 10% chance of generating a sample

import datetime
from enum import IntEnum
import random
import os

### Constants


class Month(IntEnum):
    JAN = 1,
    FEB = 2,
    MAR = 3,
    APR = 4,
    MAY = 5,
    JUN = 6,
    JUL = 7
    AUG = 8,
    SEP = 9,
    OCT = 10,
    NOV = 11,
    DEC = 12


### Settings

OUT_RESULTS_FOLDER_PATH = '/path/to/write'

# [start, end)

START_TIME = datetime.datetime(2017, Month.JUL, 3)

END_TIME = datetime.datetime(2019, Month.FEB, 5)

TIME_SLICES_PER_DAY = 24

ODDS_OF_SAMPLE_PER_SLICE = 0.03

WEEKEND_ODDS_OF_SAMPLE_PER_SLICE = 0.01

############################

# create initial temp dir for generated files
tmp_path = os.path.join(OUT_RESULTS_FOLDER_PATH, 'tmp_generated')

if not os.path.exists(tmp_path):
    os.mkdir(tmp_path)

# time between each slice
slice_hours_delta = 24 / TIME_SLICES_PER_DAY

# tracking vars
samples_per_day = []

total_sample_count = 0

total_days = (END_TIME - START_TIME).days

# generate sample days

def generate_sample_days():

    total_slices_so_far = 0

    for days_since_start in range(0, total_days):
        samples_today = []

        for time_slice in range(0, TIME_SLICES_PER_DAY):
            total_slices_so_far += 1

            # calculate what current slices datetime is

            time_since_start = slice_hours_delta * total_slices_so_far

            time_delta_hours_since_start = datetime.timedelta(hours=time_since_start)

            slice_time = START_TIME + time_delta_hours_since_start

            is_weekend = slice_time.isoweekday() >= 6

            odds_of_sample = WEEKEND_ODDS_OF_SAMPLE_PER_SLICE if is_weekend else ODDS_OF_SAMPLE_PER_SLICE

            # if we generate a sample at this slice, track it so we can display results later
            if odds_of_sample > random.random():
                global total_sample_count

                total_sample_count += 1



                samples_today.append(slice_time)

        # add the sample times we generated for this day to the tracking dictionary

        samples_per_day.append(samples_today)

def print_sample_count_calendar():
    start_day_of_week = calculate_start_date_day_of_week()

    # there are 7 days in a week, Sunday is what the GitHub calendar starts the week at
    # if we start on a wednesday (3) but we want to start printing at Sunday, add 4 days (Wed -> Thurs -> Fri -> Sat -> Sun)

    start_print_fix = 7 - start_day_of_week
    end_print_fix = start_print_fix + 7

    iteration_count = 0

    # since we print every Sunday on the same line, and every Monday on the same line (etc...)
    # we will iterate through all the Sundays first

    for day_of_week_number in range(start_print_fix, end_print_fix):
        start_print_index = day_of_week_number % 7

        # print gaps in the calendar
        if iteration_count < start_day_of_week:
            print("{0:>3s}".format(' '), end=' ')

        iteration_count += 1

        for day_to_print in range(start_print_index, total_days, 7):
            current_day_sample_count = len(samples_per_day[day_to_print])

            print("{0:>3d}".format(current_day_sample_count), end=' ')

        # start new line
        print()



# calculate which day of the week we are starting at so we can print a calendar (Monday = 1 ... Sunday = 7)
def calculate_start_date_day_of_week():
    global START_TIME

    # get start_date day of week, Sunday is 7 .. but we wan't to start on Sunday
    day_of_week_number = START_TIME.isoweekday()

    return day_of_week_number

def write_samples():
    out_file_path = os.path.join(tmp_path, str(datetime.datetime.now()))

    out_file = open(out_file_path, 'w')

    for samples_this_day in samples_per_day:
        for sample_times in samples_this_day:
            write_line = str(sample_times) + '\n'
            out_file.write(write_line)


# begin execute

generate_sample_days()

print_sample_count_calendar()

# calculate average number of samples per day, and inform
average_samples_per_day = total_sample_count / total_days

print("Total days: %d" % total_days)
print("Total samples: %d" % total_days)
print("Average samples per day: % 5.2f" % average_samples_per_day)

write_results = input('Write sample calendar? (y/n)\n')

if write_results == 'y':
    write_samples()
