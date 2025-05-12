# DexScreener Telegram Bot

A simple Telegram bot that allows users to monitor transactions of a specific token from **DexScreener API**.  
Supports filtering by transaction type (buy/sell) and minimum transaction value in USD.

## ✅ Features
- Get the latest transactions for any token supported by DexScreener.
- Filter transactions by:
  - Type: Buy / Sell.
  - Minimum transaction amount in USD.
- Written in **Python 3.11+**.
- Easy integration as a standalone bot or as part of other systems.
- Uses **DexScreener API only** (no blockchain explorers like Etherscan used).

## 💻 Usage Example
1. **Set token address:**
   ```
   /settoken <token_address>
   ```
2. **Set transaction type (buy/sell):**
   ```
   /settype buy
   ```
3. **Set minimum USD filter (optional):**
   ```
   /setmin 1000
   ```
4. **Check filtered transactions:**
   ```
   /check
   ```

## 🚀 Setup Instructions

### Requirements:
- Python 3.11+
- Dependencies from `requirements.txt`

### Installation:
```bash
pip install -r requirements.txt
```

### Configuration:
Edit `config.py` and set your **Telegram bot token**.

### Run the bot:
```bash
python bot.py
```

## ⚙ Files structure
| File                 | Description                         |
|----------------------|-------------------------------------|
| bot.py                | Main Telegram bot logic            |
| dexscreener.py        | API client for DexScreener         |
| config.py             | Bot token config                   |
| requirements.txt      | Required Python libraries          |

## ℹ Notes
- This bot only uses **DexScreener API**, ensuring fast response and lightweight operation.
- Can be expanded to include more filters or integrate into larger projects.