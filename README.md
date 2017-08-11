[![Stories in Ready](https://badge.waffle.io/mikaeilorfanian/timetracker.png?label=ready&title=Ready)](https://waffle.io/mikaeilorfanian/timetracker?utm_source=badge)
[![Build Status](https://travis-ci.org/mikaeilorfanian/timetracker.svg?branch=master)](https://travis-ci.org/mikaeilorfanian/timetracker)
[![Coverage Status](https://coveralls.io/repos/github/mikaeilorfanian/timetracker/badge.svg?branch=master)](https://coveralls.io/github/mikaeilorfanian/timetracker?branch=master)
# Get a Grip On Your Time!
`timetracker` is a simple application that lets you
* Track the time you spend doing different activities during the day
* Generate reports that show you how you've spent your time

## Why Track Time?
Before you can improve anything, you need to be aware of how things are right now. `timetracker` reports help you become aware of how you're spending your time. Try it for at least one day and you'll be amazed by the results.

## How to Use It
#### How to Install It?
First, install `timetracker` on your machine. Note that you need to have Python 3.5 or 3.6 installed along with `pip`.
Second, install `timetracker` using `pip` like this   
```
pip install git+https://github.com/mikaeilorfanian/timetracker.git
```
Tip: I recommend that you create a new virtual env and install `timetracker` in that env.   
Note: `timetracker` is not on `pypi` yet! Please install it using the instructions above.   
#### Get Started Tracking Your Time!
Now, you can start tracking your time by writing this command in the terminal:   
```
timetrack working
```
This command will start tracking time for "working". You can use any other name instead of "working" like "napping", "chatting", "break", etc.
Note: `timetracker` doesn't spell check the activity you ask it to track.   
When you stop "working" and start taking a break issue this command in the terminal   
```
timetrack break
``` 
This will stop tracking your "working" time and start tracking your "break" time.   
After issuing the `timetrack <activity>` command you'll see a summary of how much time you've spent on <activity> that day.
As you can see, by issuing `timetrack <activity>` you're always tracking your time. So, a typical day of using `timetracker` would look like this:
- `timetrack breakfast`
- `timetrack shower`
- `timetrack commute`
- `timetrack chatting`
- `timetrack working`
- `timetrack break`
- `timetrack working`
- `timetrack lunch`
- ...

There's also an option to stop tracking time:
```
timetrack stop
```
`stop` is a reserved keyword, so this command will NOT start tracking a "stop" activity. It will just stop tracking the last activity.

#### Learn How You Spend Your Time
After you install `timetracker` you get another command called `timereport`. This command gives you insights on *how* you've spent your time. Here's how you can use it:
Time you've spent on <activity> today
`timereport --activity working` --> report on time spent working today
Time you've spent on <activity> the last X days
`timereport --activity working --days 3` --> report on time spent working during the last 3 days
## Goals For This Project
#### Non-technical Goals
We want to design `timetracker` so that:
* you can easily track your time
* you can easily see how you've spent your time
* you can use `timetracker` on multiple devices
#### Technical Goals
`timetracker` is made using strict TDD and Clean Code guidelines as stated in Uncle Bob's Clean Code video series. If you've watched those videos, you may have noticed that although Python is rarely mentioned by Uncle Bob he promises that his guidelines are applicable to all object-oriented programming languages.   
This project is an experiment to see how those guidelines apply to software development using Python. As Uncle Bob suggests, some of his guidelines should be modified when using dynamic languages and I'm interested in knowing exactly which of them, why, and to consider if there's a need for Clean Code for Python.   
Finally, I'm planning to report on my findings. If you'd like me to let you know when my analysis is ready, please email me at `mokt@outlook.com` and specify that you're interested in the results.
## Roadmap
First, I'd like to finish the client side of `timetracker` which allows users to track time and generate reports on their local machine.   
Then, I'd like to do the server side of `timetracker` which will allow users to track time and generate reports on multiple devices using the terminal or a web application.   
The goal is to have user settings and activity history synced across all devices so that the user moves from one device to another without noticing that they're actually using different version of `timetracker`.
For more details, check out our Kanban board [here](https://waffle.io/mikaeilorfanian/timetracker).

## Contributing
Fork the repo. Clone the forked repo to your machine. Read [this](https://help.github.com/articles/configuring-a-remote-for-a-fork/) and [this](https://help.github.com/articles/syncing-a-fork/) to understand why forking and then cloning is a good idea.   
Create and activate a fresh virtual env. Install dependencies using `pip -r requirements.txt`. Run the tests by running this command in the shell: `python ./scripts/run_tests.py`.    
If you'd like to contribute to the project in any capacity (user, project manager, marketing specialist, developer, etc.) then email me at `mokt@outlook.com`.
