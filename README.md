# 🏦 Banking Bot

A conversational banking assistant powered by Mistral Large AI. Built with Flask and featuring a beautiful web interface.

## Features

✨ **AI-Powered Banking Assistant**
- Real-time chat with Mistral Large AI
- Check account balance
- View transaction history
- Simulate fund transfers
- Conversation memory

🎨 **Beautiful Web Interface**
- Modern, responsive UI
- Real-time balance updates
- Typing indicators
- Message animations
- Mobile-friendly design

## Prerequisites

- Python 3.8+
- Mistral API Key (get one at [mistral.ai](https://mistral.ai))

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/prashantbhaskar1612-pixel/banking-bot.git
cd banking-bot
```

### 2. Create virtual environment
```bash
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

Edit `.env` and add your Mistral API key:
```
MISTRAL_API_KEY=your_api_key_here
```

**⚠️ Important:** Never commit `.env` file with real API keys!

## Usage

### Run the web server
```bash
python app.py
```

Open your browser and navigate to:
```
http://localhost:5000
```

### Try these commands
- "What's my balance?"
- "Show my recent transactions"
- "Transfer $100 to John"
- "Tell me about my account"

## Project Structure

```
banking-bot/
├── app.py                 # Flask web server
├── banking_bot.py        # Command-line bot version
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── templates/
    └── index.html        # Web UI
```

## API Endpoints

- `GET /` - Main web interface
- `POST /api/chat` - Send message to bot
- `GET /api/balance` - Get account balance
- `GET /api/transactions` - Get transaction history

## Security

- API keys are stored in `.env` (not tracked by git)
- Use environment variables for sensitive data
- `.env` is in `.gitignore`

## Environment Variables

```
MISTRAL_API_KEY=your_mistral_api_key_here
```

## License

MIT License - feel free to use this project

## Author

Prashant Bhaskar - [GitHub](https://github.com/prashantbhaskar1612-pixel)

---

**Note:** This is a demo application. For production use, implement proper authentication, database persistence, and security measures.
