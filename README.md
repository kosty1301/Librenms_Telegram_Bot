# Librenms_Telegram_Bot
## Hey! I present to your attention a small telegram bot, for using the librenms monitoring system via the api interface

## Installation

bot requires [pythonv3.4+](https://www.python.org/) and [pip3](https://pypi.org/project/pip/) to run.
Install the dependencies and start the server.

```sh
mkdir librenms_bot && cd "$_"
git clone https://github.com/kosty1301/Librenms_Telegram_Bot.git
./install.sh  # chmod +x install.sh if you get "permission denied"
```
After finishing you can start the bot like this:
```sh
python3 ./main.py &
```
## How to use?
After starting the bot will try to connect to your librenms server in order to update the local database.
You will receive a record of this in the log file, then you can use these commands:
```sh
/start  #authorization
/add_device  # adding a device to track alarms
/device_list  # show a list of devices added to the tracking
/refresh_database  # refresh local database (￢_￢)
```
After adding the device to the tracked list,
you will receive notifications about violations in his work, as well as about restoration
The number of users and devices is not limited

## what's next?
So far, the bot is using the telegram api polling method,
I am planning to add a version with a webhook method.
I also plan to add the ability to use postgresql instead of sqlite..