import streamlit as st
import pandas as pd
import os
import time
from payman_sdk.client import PaymanClient
from payman_sdk.types import PaymanConfig

# === Setup Payman Client ===

config: PaymanConfig = {
    'client_id': "PAYMAN_CLIENT_ID",
    'client_secret': "PAYMAN_CLIENT_SECRET",
}
client = PaymanClient.with_credentials(config)

# === Log File Setup ===
LOG_FILE = "restock_log.csv"
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=["item", "qty", "unit_cost", "total", "wallet"]).to_csv(LOG_FILE, index=False)

def load_log():
    return pd.read_csv(LOG_FILE)

def save_log(df):
    df.to_csv(LOG_FILE, index=False)

# === Wallets ===
def get_wallet_names():
    return ["TSD Wallet 3", "Inventory", "TSD Wallet"]

# === Streamlit UI ===
st.set_page_config(page_title="🛍️ Auto Restock Inventory", layout="centered")
st.title("🛍️ Auto Restock Fashion Inventory")
st.markdown("""
Welcome to the **Auto Restock Agent** powered by [PaymanAI](https://paymanai.com) 💸  
This app helps fashion and jewelry sellers **automatically detect low-stock items** and trigger **TSD test payments** to restock vendors.
""")

# Wallet selection
wallet_names = get_wallet_names()
wallet_name = st.selectbox("💼 Select Wallet to Use for Payments", wallet_names)

# Upload inventory CSV
csv_file = st.file_uploader("📤 Upload Inventory CSV", type=["csv"])

if csv_file:
    df = pd.read_csv(csv_file)
    st.subheader("📦 Current Inventory")
    st.dataframe(df.style.format({"Unit_Cost": "₹{:.2f}"}))

    restock_items = []
    st.subheader("📋 Customize Restock Plan")

    for idx, row in df.iterrows():
        if row["Quantity"] < row["Threshold"]:
            item = row["Item"]
            default_qty = row["Threshold"] - row["Quantity"] + 5
            unit_cost = row["Unit_Cost"]

            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                include = st.checkbox(f"✅ Restock {item}", value=True, key=f"check_{item}")
            with col2:
                qty = st.number_input(f"Qty for {item}", min_value=1, value=default_qty, step=1, key=f"qty_{item}")
            with col3:
                st.markdown(f"**Unit Cost:** ₹{unit_cost}")

            if include:
                total = qty * unit_cost
                restock_items.append({
                    "item": item,
                    "qty": qty,
                    "unit_cost": unit_cost,
                    "total": total
                })

    if restock_items:
        restock_df = pd.DataFrame(restock_items)
        total_cost = restock_df["total"].sum()

        st.markdown("### 💰 Final Restock Summary")
        st.dataframe(restock_df.style.format({"unit_cost": "₹{:.2f}", "total": "₹{:.2f}"}))
        st.markdown(f"#### 🧾 **Total TSD to Pay:** ₹{round(total_cost, 2)}")
        st.markdown(f"💼 **Selected Wallet:** {wallet_name}")

        if st.button("✅ Trigger TSD Payments"):
            log_df = load_log()

            for item in restock_items:
                item_name = item["item"]
                amount = round(item["total"], 2)

                # Step 1: Create payee if not exists
                if item_name not in log_df["item"].values:
                    try:
                        st.info(f"⏳ Creating Payee: {item_name}")
                        create_response = client.ask(f"create {item_name} type test rails")
                        st.write(f"🧾 Payee Creation Response: {create_response}")
                        time.sleep(2)
                    except Exception as e:
                        st.error(f"❌ Payee creation failed for {item_name}: {e}")
                        continue

                # Step 2: Send Payment
                try:
                    payment_prompt = f"send {amount} TSD to {item_name} type test rails from {wallet_name}"
                    st.info(f"💸 Sending TSD: {payment_prompt}")
                    payment_response = client.ask(payment_prompt)
                    time.sleep(2)

                    # Step 3: Log payment
                    new_entry = {
                        "item": item["item"],
                        "qty": item["qty"],
                        "unit_cost": item["unit_cost"],
                        "total": item["total"],
                        "wallet": wallet_name
                    }
                    log_df = pd.concat([log_df, pd.DataFrame([new_entry])], ignore_index=True)
                    save_log(log_df)
                    st.success(f"✅ Paid ₹{amount} TSD for {item_name}")
                except Exception as e:
                    st.error(f"❌ Payment failed for {item_name}: {e}")
    else:
        st.info("✅ No items selected or all inventory is above threshold.")

    st.markdown("---")
    st.subheader("📒 Past Payment History")
    st.dataframe(load_log().style.format({"unit_cost": "₹{:.2f}", "total": "₹{:.2f}"}))

else:
    st.info("📎 Please upload a CSV file with inventory details.")
