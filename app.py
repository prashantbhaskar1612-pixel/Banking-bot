import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from mistralai.client import MistralClient

load_dotenv()

app = Flask(__name__)
CORS(app)

# ChatMessage class for API
class ChatMessage:
    def __init__(self, role, content):
        self.role = role
        self.content = content

    def dict(self):
        return {"role": self.role, "content": self.content}

load_dotenv()

app = Flask(__name__)
CORS(app)

class BankingBot:
    def __init__(self):
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY not found in .env file")

        self.client = MistralClient(api_key=api_key)
        self.model = "mistral-large-latest"
        self.accounts = {
            "user123": {
                "balance": 5000.00,
                "transactions": [
                    {"type": "deposit", "amount": 5000, "date": "2024-01-01"},
                    {"type": "purchase", "amount": -150, "date": "2024-01-10"},
                    {"type": "deposit", "amount": 1000, "date": "2024-01-12"}
                ]
            }
        }
        self.conversation_history = []
        self.system_prompt = """You are a helpful banking assistant bot. You help users with:
- Checking account balance
- Making transfers
- Viewing transaction history
- Account information

Current account data:
- Account ID: user123
- Balance: ${balance}
- Recent transactions: {transactions}

Be friendly and professional. Keep responses concise. If asked for sensitive operations, confirm with the user."""

    def get_account_info(self, account_id="user123"):
        """Get account information"""
        if account_id in self.accounts:
            return self.accounts[account_id]
        return None

    def check_balance(self, account_id="user123"):
        """Check account balance"""
        account = self.get_account_info(account_id)
        if account:
            return account["balance"]
        return None

    def transfer_funds(self, amount, recipient_account="default", account_id="user123"):
        """Simulate fund transfer"""
        account = self.get_account_info(account_id)
        if account and account["balance"] >= amount:
            account["balance"] -= amount
            account["transactions"].append({
                "type": "transfer",
                "amount": -amount,
                "recipient": recipient_account,
                "date": "2024-01-15"
            })
            return {"success": True, "new_balance": account["balance"]}
        return {"success": False, "error": "Insufficient funds"}

    def get_transactions(self, account_id="user123"):
        """Get transaction history"""
        account = self.get_account_info(account_id)
        if account:
            return account["transactions"]
        return []

    def chat(self, user_message):
        """Send message to Mistral and get response"""
        transactions = self.get_transactions()

        system_prompt = self.system_prompt.format(
            balance=self.check_balance(),
            transactions=", ".join([f"{t['type']}: ${t['amount']}" for t in transactions[-3:]])
        )

        self.conversation_history.append(
            ChatMessage(role="user", content=user_message)
        )

        response = self.client.chat(
            model=self.model,
            messages=[
                ChatMessage(role="system", content=system_prompt),
                *self.conversation_history
            ],
            temperature=0.7,
            max_tokens=500
        )

        assistant_message = response.choices[0].message.content
        self.conversation_history.append(
            ChatMessage(role="assistant", content=assistant_message)
        )

        return assistant_message

# Initialize bot
try:
    bot = BankingBot()
except ValueError as e:
    print(f"Error: {e}")
    bot = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    if not bot:
        return jsonify({"error": "Bot not initialized. Check MISTRAL_API_KEY in .env"}), 500

    data = request.get_json()
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        response = bot.chat(user_message)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/balance', methods=['GET'])
def balance():
    if not bot:
        return jsonify({"error": "Bot not initialized"}), 500

    balance = bot.check_balance()
    return jsonify({"balance": balance})

@app.route('/api/transactions', methods=['GET'])
def transactions():
    if not bot:
        return jsonify({"error": "Bot not initialized"}), 500

    trans = bot.get_transactions()
    return jsonify({"transactions": trans})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
