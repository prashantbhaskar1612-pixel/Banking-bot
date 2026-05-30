import os
from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_message import ChatMessage

load_dotenv()

class BankingBot:
    def __init__(self):
        api_key = os.getenv(" VgjMaOhcbAC94eweOCSdlYr6rhs1Br9Q
")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY not found in .env file")

        self.client = MistralClient(api_key=api_key)
        self.model = "mistral-large-latest"
        self.accounts = {
            "user123": {
                "balance": 5000.00,
                "transactions": [
                    {"type": "deposit", "amount": 5000, "date": "2024-01-01"}
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

Be friendly and professional. If asked for sensitive operations, confirm with the user."""

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
        account = self.get_account_info()
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

    def run(self):
        """Run the bot in interactive mode"""
        print("🏦 Banking Bot Started")
        print("Type 'quit' to exit\n")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "quit":
                print("Thank you for using Banking Bot. Goodbye!")
                break
            if not user_input:
                continue

            response = self.chat(user_input)
            print(f"Bot: {response}\n")

if __name__ == "__main__":
    bot = BankingBot()
    bot.run()
