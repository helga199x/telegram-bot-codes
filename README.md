# Project Name
## Telegram Bot for Door Access Codes Management

# Description
This project implements a Telegram bot using Python that allows users to manage and retrieve door access codes stored in a SQLite database. Users can interact with the bot to add, retrieve, and delete access codes associated with specific addresses.

# Features
Adding Access Codes: Admin users can add new door access codes for specific addresses via commands or inline keyboard buttons.

Retrieving Access Codes: Users can retrieve door access codes for a given address through inline keyboard options.

Deleting Access Codes: Admin users can delete existing access codes associated with specific addresses.

--- 

# Requirements
Python 3.x
telebot library (Telegram Bot API wrapper)
sqlite3 (SQLite database management)
Any other dependencies specific to your project
Installation
Clone the repository:

bash
Copy code
```
git clone https://github.com/yourusername/telegram-door-access-bot.git
cd telegram-door-access-bot
```
Install dependencies:

bash
Copy code
```
pip install -r requirements.txt
```
Set up SQLite database:

Make sure bot_database.db is created with necessary tables (house_codes table with columns address, house_number, code).
Update configurations:

Replace YOUR_TELEGRAM_BOT_TOKEN in bot.py with your actual Telegram bot token.
Modify any other configuration settings as required.
Usage
- Run the bot:

bash
Copy code
python bot.py
The bot will start and listen for incoming messages and callback queries from Telegram users.

- Interact with the bot:

Use commands `/start to` begin interaction and `/add_address <address> <code>` to add a new access code.
Use inline keyboard options to retrieve or manage access codes associated with addresses.
License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author
Volha Shemshur
GitHub: helga99x

## Acknowledgements
```
brew install python-pip
pip3 install telebot
pip3 install pytelegrambotapi
pip3 install python-telegram-bot
pip3 install telegram
pip3 install opencage
```
