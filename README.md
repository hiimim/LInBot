# LInBot
Increase your popularity on LinkedIn and rank #1 among your network.
## About
In May 2014 LinkedIn introduced a new feature, [How You Rank](https://www.linkedin.com/wvmx/profile/rankings), which will show the most-viewed profiles among one's company and greater network.

This bot will allow you to rank #1 by visiting thousands of profiles, who will visit you in return (around 2.5% of them according to my tests).
## Requirements
**Important:** make sure that you have your [Profile Viewing Setting](https://www.linkedin.com/settings/?trk=nav_account_sub_nav_settings) changed from 'Anonymous' to  'Public' so LinkedIn members can see that you have visited them and can visit your profile in return.

LInBot was developed under [Pyhton 2.7](https://www.python.org/downloads).

Before you can run the bot, you will need to install a few Python dependencies.

Note: Python 2.7.9 and later (on the python2 series), and Python 3.4 and later include pip by default, so you may have pip already. Otherwise, you can install [easy_install](https://pythonhosted.org/setuptools/easy_install.html) `sudo apt-get install python-setuptools` to install [pip](https://pypi.python.org/pypi/pip) `sudo easy_install pip`.

- [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4), for parsing html: `pip install BeautifulSoup4`
- [Selenium](http://www.seleniumhq.org/), for browser automation: `pip install Selenium`

## Configuration
Before you run the bot, edit the `config` file to add your account login informations (email and password). It's that simple!

## Run
Once you have installed the required dependencies and edited the `config` file, you can run the bot.

Make sure you are in the correct folder and run the following command: `python LInBot.py`
On Windows you can usually just double-click `bot.py` to start the bot, as long as you have Python installed correctly.

Then, after choosing your favorite browser (for better performances, the *light* versions disable the loading of javascript, css and images), the bot will start visiting profiles.

## Screenshot
The bot on my Raspberry Pi 2 B.

![screenshot](https://cloud.githubusercontent.com/assets/12429123/7690810/3aa22878-fdb7-11e4-8f5e-37793a96577a.png)

T: Number of profiles the bot tried to access;

V: Number of profiles the bot actually visited (profiles you can access: rank 3 or less);

Q: Number of profiles in queue.
