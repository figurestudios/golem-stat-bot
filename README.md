# golem-stat-bot
This is an example project on how stats.golem.network API can be utilized. It scrapes Reddit posts, and replies if specific keywords/commands are found.

## Setup
Ensure that the Python version is higher than the dependencies require. Generally a newer version should do.

Get configurations from [Reddit](https://www.reddit.com/prefs/apps) & swap them out in the [config.json](https://github.com/figurestudios/golem-stat-bot/blob/main/config.json) file.

Run `python3 program`. This should be done everytime you want to scrape the newly created posts. Consider using [this](https://github.com/figurestudios/golem-stat-bot/blob/main/repeat.sh) shell script & launch it with `nohup repeat` incase you want to repeat it every 10 minutes.
