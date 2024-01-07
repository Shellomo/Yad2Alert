# Yad2Alert

## Overview
**Yad2Alert** is a tool designed to send automatic alerts to Telegram channels when new advertisements are posted on Yad2. It allows users to configure specific URLs to monitor and specify the destination Telegram channel for alerts.

<img src="Screen-Recording.gif" width="200" height="300" alt="Description of the GIF">


### Features
- **Automated Alerts**: Sends notifications to Telegram channels about new ads.
- **Customizable**: Users can configure which URLs to scan and where to send alerts.
- **Detailed Alerts**: Notifications include pictures (if available), name, description, price, and a direct link to the ad on Yad2.

## Configuration
The tool uses a `jobs.json` file for configuration. Each job in the file includes:

- `name`: Identifier for the job (e.g., "BedForNir"). This is just a label and doesn't affect functionality.
- `pages_to_scan`: Number of pages to scan for each URL.
- `url`: An array of URLs to scan. At least one URL is required. Refer to the "How to generate a good URL" section for guidance.
- `enabled`: A flag to enable or disable the job.
- `alert_on_price_change`: Option to enable or disable alerts when there is a price change.
- `telegram_channel`: The negative number representing the Telegram channel ID. See "How to get Telegram channel ID" for details.

## Prerequisites
- Telegram account
- AWS account

## Setup Instructions

### Telegram Keys
1. **API_ID and API_HASH**: Create an app on Telegram and obtain your API ID and API hash. [Follow these instructions](https://core.telegram.org/api/obtaining_api_id).
2. **BOT_API**: 
   - Use @BotFather on Telegram to create a new bot.
   - Name your bot (e.g., `yad2_alert_bot`).
   - The bot token you receive will be your `BOT_API`.


### How to Get Telegram Channel ID?
1. Create a Telegram channel.
2. Add your bot to the channel as an admin.
3. Use @username_to_id_bot on Telegram to find out the channel's ID.
4. Enter this ID in the `telegram_channel` field of the relevant job in `jobs.json`.

### How to Generate a Good URL?
1. Visit Yad2 and apply all relevant filters to your search.
2. Optionally, add free text to refine your search.
3. Click on 'Search'.
4. Copy the URL from the browser's address bar and paste it into the `url` field of the relevant job in `jobs.json`.


### Setup on AWS
1. Create an S3 bucket, name like `yad2alert` is ok.
2. copy the `jobs.json` file, edit it as required, and upload it to the S3 bucket.