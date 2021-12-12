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
## what's next?
So far, the bot is using the telegram api polling method,
I am planning to add a version with a webhook method.
I also plan to add the ability to use postgresql instead of sqlite..
