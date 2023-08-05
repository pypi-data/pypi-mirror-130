# Munibot España / Catalunya

Two friendly Twitter bots built with [Munibot](https://github.com/amercader/munibot) that tweet aerial pictures of Spain's [municipalities](https://en.wikipedia.org/wiki/Municipalities_of_Spain).

One of the bot tweets municipalities of Spain at [@munibot_es](twitter.com/munibot_es) and the other just the Catalan ones at [@munibot_cat](twitter.com/munibot_cat).

## Install and setup

Install it with pip:

```
pip install munibot-es
```

And follow the instructions on [Munibot's documentation](https://github.com/amercader/munibot#usage) regarding configuration and setup.

This particular bot requires the backend SQLite database with municipalities data, which you can download from this repo (`data` folder).


This should be referenced in the `[profile:es]` and `[profile:cat]` sections of your `munibot.ini` file:

```
[profile:es]
twitter_key=CHANGE_ME
twitter_secret=CHANGE_ME
db_path=/path/to/data/munis_esp.sqlite

[profile:ca]
twitter_key=CHANGE_ME
twitter_secret=CHANGE_ME
db_path=/path/to/data/munis_esp.sqlite
```

## License

[MIT](/amercader/munibot/blob/master/LICENSE.txt)
