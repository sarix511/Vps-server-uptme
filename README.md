# Telegram Bot + UptimeRobot Health Site

This project includes:
- A small Flask website (`/`)
- A health-check endpoint (`/health`) for UptimeRobot
- A Python Telegram bot with `/start` and `/help`
- A channel button in the welcome message

## Important
Opening the website does **not** start a new bot instance. The bot starts when the hosting service process starts. UptimeRobot only checks the health URL; it is not a hosting provider and does not guarantee 24/7 uptime. A host may sleep, restart, or restrict background polling. Use a host that permits a continuously running Telegram polling process, or deploy the bot as a persistent worker.

## Deploy on Render (if the selected plan supports your process)
1. Upload these files to a GitHub repository.
2. In Render, create a new **Web Service** connected to that repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:web --workers 1 --threads 4 --timeout 120`
5. Add environment variables:
   - `BOT_TOKEN` = your Telegram bot token from BotFather
   - `CHANNEL_URL` = your channel's public link, e.g. `https://t.me/your_channel`
   - `WELCOME_TEXT` = your desired welcome message (optional)
6. Deploy, then open `https://YOUR-SERVICE.onrender.com/health`. It should return JSON with `"status": "ok"`.

## UptimeRobot
1. Create an HTTP(s) monitor.
2. Monitor type: **HTTP(s)**
3. URL: `https://YOUR-SERVICE.onrender.com/health`
4. Choose an available monitoring interval and save.

UptimeRobot checks the web endpoint. It cannot prevent every host sleep/restart or make an unsupported free plan into guaranteed 24/7 hosting.

## Security
- Never put your bot token in source code or commit it to GitHub.
- If a token was shared publicly, revoke it via BotFather and generate a new one.
- Do not upload `.env` files or secrets.
