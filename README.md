# `getter`

> Get and put users (scraping) to the target **group/channel** efficiently, correctly and safety.

<p align="center">
    <a href="https://github.com/kastaid/getter/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/workflow/status/kastaid/getter/CI?logo=github&label=CI" /></a>
    <a href="https://app.codacy.com/gh/kastaid/getter/dashboard"><img alt="Codacy grade" src="https://img.shields.io/codacy/grade/2f86ed8f8534424c8d4cdaa197dc5ce2?logo=codacy" /></a>
    <a href="https://github.com/kastaid/getter/blob/main/LICENSE"><img alt="LICENSE" src="https://img.shields.io/github/license/kastaid/getter" /></a>
    <a href="https://t.me/kastaid"><img alt="Telegram" src="https://img.shields.io/badge/kastaid-blue?logo=telegram" /></a>
    <br>
    <a href="https://github.com/kastaid/getter/issues"><img alt="Issues" src="https://img.shields.io/github/issues/kastaid/getter?logo=github" /></a>
    <a href="https://github.com/kastaid/getter/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/kastaid/getter?logo=github" /></a>
    <a href="https://github.com/kastaid/getter/network/members"><img alt="Forks" src="https://img.shields.io/github/forks/kastaid/getter?logo=github" /></a>
    <a href="https://github.com/kastaid/getter/graphs/contributors"><img alt="Contributors" src="https://img.shields.io/github/contributors/kastaid/getter?logo=github" /></a>
</p>

```
#include <std/disclaimer.h>
/*
*    Your Telegram account may get banned.
*    We are not responsible for any improper use of this bot
*    This bot is intended for the purpose of scraping members,
*    as well as efficiently to get members correctly.
*    You ended up spamming groups, getting reported left and right,
*    and you ended up in a Finale Battle with Telegram and at the end
*    Telegram Team deleted your account?
*    And after that, then you pointed your fingers at us
*    for getting your acoount deleted?
*    I will be rolling on the floor laughing at you.
*/
```

## Table of Contents

<details>
<summary>Details</summary>

- [Requirements](#requirements)
  - [STRING_SESSION](#string_session)
  - [Run locally](#run-locally)
  - [Heroku](#heroku)
- [Credits](#credits)
- [Contributing](#contributing)
- [License](#license)

</details>

## Requirements

- Python 3.9.x
- Linux (Recommend Debian/Ubuntu)
- Telegram Account (API_ID and API_HASH)

### STRING_SESSION

Generate `STRING_SESSION` using [replit.com](https://replit.com/@notudope/strgen) or [@strgen_bot](https://t.me/strgen_bot) or `python3 session.py`

### Run locally

```sh
# Production
pip3 install -r requirements.txt
python3 -m getter

# Development
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
python3 -m run --watch
```

More commands `python3 -m run -h`

### Deploy

To deploy please visit our channel at [@kastaid](https://t.me/kastaid).

## Credits

* [RaphielGang](https://github.com/RaphielGang) - Telegram-Paperplane
* [BianSepang](https://github.com/BianSepang) - WeebProject
* [userbotindo](https://github.com/userbotindo) - Userbot Indonesia Community
* [TeamUltroid](https://github.com/TeamUltroid) - Team Ultroid
* [mrismanaziz](https://github.com/mrismanaziz) - Man-Userbot

and [everyone](https://github.com/kastaid/getter/graphs/contributors) 🦄

## Contributing

If you would like to help out with some code, check the [details](https://github.com/kastaid/getter/blob/main/docs/CONTRIBUTING.md).

## License

This project is licensed under the [GNU Affero General Public License](https://github.com/kastaid/getter/blob/main/LICENSE) v3.0.
