# PAYMAN DEV CHALLENGE- AUTO INVENTORY RESTOCK AGENT

🌐 **Live App**: https://auto-restock-agent.streamlit.app/

---

## 🤖 AI-Powered Auto Restock Agent for Sellers

This is a **Streamlit-based smart inventory agent** that uses:

- 📉 Live inventory check from uploaded CSV
- 🧠 AI-powered restock decisions
- 💸 Seamless vendor payments using **[Payman.ai](https://payman.ai)** (test rails)
- 🧾 Automatic logging with stop-loss tracking

---

## 🚀 Features

- 🧵 Detects items with low stock levels
- 🧮 Calculates required quantities and total cost
- 🧾 Creates payees automatically via Payman if not present
- 💸 Sends test payments using **natural language prompt**
- 📒 Logs purchases with stop loss in `restock_log.csv`

---

## 🧠 How It Works

1. Upload your inventory CSV (with `Item`, `Quantity`, `Threshold`, `Unit_Cost`)
2. The app filters items below their threshold
3. For each such item:
   - Creates the payee if not already added
   - Calculates how many units to restock and total cost
   - Sends the payment via Payman SDK
   - Logs the transaction with a safety stop-loss price

---

## 📂 Folder Structure
auto-restock-agent/
├── app.py # Main Streamlit application
├── fashion_inventory.csv # Sample input file
├── restock_log.csv # Auto-generated log file
├── requirements.txt # Python dependencies
└── README.md # This file

---

## 📦 Sample Inventory File

Create a file named `fashion_inventory.csv` like below:

| Item            | Quantity | Threshold | Unit_Cost |
|-----------------|----------|-----------|-----------|
| Gold Necklace   | 2        | 10        | 150       |
| Leather Jacket  | 5        | 10        | 120       |
| Denim Jeans     | 6        | 12        | 60        |
| Silk Scarf      | 3        | 10        | 35        |
| Running Shoes   | 4        | 8         | 80        |
| Woolen Sweater  | 5        | 10        | 70        |
| Handbag         | 1        | 6         | 90        |

---

## 🛠️ Technologies Used

| Component        | Tool / API                |
|------------------|---------------------------|
| UI & UX          | Streamlit                 |
| Payments         | Payman SDK (Natural Lang) |
| Data Handling    | Pandas                    |
| Deployment       | Streamlit Cloud           |

---

## 💻 Local Installation

git clone https://github.com/yourusername/auto-restock-agent
cd auto-restock-agent
pip install -r requirements.txt
streamlit run app.py

---
## 🔐 Payman Credentials

Paste these directly in your `app.py` file:

```python
from payman_sdk.client import PaymanClient

client = PaymanClient.withClientCredentials({
    "client_id": "your-client-id-here",
    "client_secret": "your-client-secret-here"
})
