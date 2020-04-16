# Generate Calendar Sample Times

## Use case

Maybe you're writing a fuzz test that needs to perform some action at random time intervals and you need a set of
random dates within a specified interval. Perhaps you aren't sure when to buy a lottery ticket and want to leave
it up to chance (within specified parameters, of course).

This is for you.

## Usage

Set the following parameters, and then run the tool. The resulting time slices will be printed to `stdout` and
 you will get the option &mdash; `(y/n)` &mdash; to write the results to a file in a `/tmp/` directory
 in the specified directory.
 
 ![example run][example_run]

    OUT_RESULTS_FILE_PATH               - Path to write tmp file containing result output

    START_TIME                          - What datetime to start generating samples

    END_TIME                            - What datetime to stop generating samples

    TIME_SLICES_PER_DAY                 - How many time per day should we possibly create a sample

    ODDS_OF_SAMPLE_PER_SLICE            - The odds of generating a sample at each time slice

    WEEKEND_ODDS_OF_SAMPLE_PER_SLICE    - The odds of generating a sample at each weekend time slice

[example_run]: ./example_run.png