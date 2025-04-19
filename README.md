# Project R-100 Telegram Bot

A market monitoring bot using Flask and Telegram.

## Setup

1. Set environment variables:
   - `BOT_TOKEN`: Your Telegram bot token
   - `TELEGRAM_ID`: Your Telegram user ID
   - `WEBSITE_URL`: Your Railway public app URL

2. Deploy via Railway or any hosting platform that supports Flask.

## Endpoint

- `/{BOT_TOKEN}` for receiving Telegram webhook events.