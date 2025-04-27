
import streamlit as st
import pandas as pd
import re

# إعداد الصفحة
st.set_page_config(page_title="AccTables – Smart Transaction Classifier", layout="centered")

st.title("📘 AccTables – Smart Accounting Assistant")

# اختيار نوع الجدول
table_option = st.selectbox("📊 Choose the type of accounting table you want to generate:", ["Balance Sheet"])

if table_option == "Balance Sheet":
    st.markdown("You have selected **Balance Sheet**. Enter your transactions below.")

    # الكلمات المفتاحية حسب التصنيف
    asset_keywords = ["purchase", "purchases", "buy", "bought", "equipment", "furniture", "inventory", "vehicle", "land"]
    liability_keywords = ["loan", "borrowed", "payable", "debt"]
    equity_keywords = ["invested", "capital", "owner", "contribution", "invoice", "bill", "bills", "covered"]

    def classify_transaction(text):
        text = text.lower()
        if any(word in text for word in asset_keywords):
            debit = "Asset"
        elif any(word in text for word in liability_keywords):
            debit = "Liability"
        elif any(word in text for word in equity_keywords):
            debit = "Equity"
        else:
            debit = "Unknown"

        if "cash" in text or "paid" in text:
            credit = "Cash"
        elif "loan" in text or "borrowed" in text:
            credit = "Loan"
        elif "owner" in text or "capital" in text or "invested" in text:
            credit = "Owner's Equity"
        else:
            credit = "Unknown"

        return debit, credit

    def extract_amount(text):
        match = re.search(r'\d+(?:,\d{3})*(?:\.\d+)?', text)
        return float(match.group().replace(',', '')) if match else 0

    if "entries" not in st.session_state:
        st.session_state.entries = []

    text_input = st.text_input("✍️ Enter a transaction:")
    if st.button("➕ Analyze and Add") and text_input:
        debit, credit = classify_transaction(text_input)
        amount = extract_amount(text_input)
        st.session_state.entries.append({
            "Description": text_input,
            "Account": debit,
            "Type": "Debit",
            "Amount": amount
        })
        st.session_state.entries.append({
            "Description": text_input,
            "Account": credit,
            "Type": "Credit",
            "Amount": amount
        })
        st.success("✅ Transaction added and classified!")

    if st.session_state.entries:
        st.subheader("📋 Journal Entries")
        df = pd.DataFrame(st.session_state.entries)
        st.dataframe(df)

        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Journal')
        st.download_button("📤 Download as Excel", data=output.getvalue(), file_name="journal.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
