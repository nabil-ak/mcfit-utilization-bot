<img src="https://upload.wikimedia.org/wikipedia/commons/3/3b/Logo_McFIT_GmbH.jpg" alt="icon" width="128" hight="128"/>


# Mcfit-Utilization-Bot

This discord bot will show you the current utilization of your gym.
You will need your McFIT login credentials to use their API.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirement frameworks.

```bash
pip install -r requirements.txt
```
## Settings
1. Change the ```EMAIL```, ```PASSWORD``` to your **login credentials**
2. Set the right ```ID``` of your GYM. The ID is behind the studio in the url of the gym (https://my.mcfit.com/studio/**cnNnLWdyb3VwOjE0MTQwNDgzMjA=**) **DONT FORGET THE EQUAL CHARACTER**
3. Create and set the ```token``` of your discord bot.

```env
EMAIL = ENTER_EMAIL
PASSWORD = ENTER_PASSWORD
STUDIO = THE_ID_OF_YOUR_STUDIO
DISCORD_BOT_TOKEN = THE_TOKEN_OF_YOUR_DISCORD_BOT
```
## Usage
1. Create a token for your discord bot in the discord developer dashboard.
2. Change your .env file with your own data.
3. Run the bot with ```python3 bot.py```.
4. Use the ```/util```command to get the current utilization of your gym.


## Example
<img src="https://i.imgur.com/2mABMjF.png" alt="icon" width="265" hight="265"/>


## License
[MIT](https://choosealicense.com/licenses/mit/)