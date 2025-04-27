import streamlit as st
import pandas as pd
import re

# إعداد الصفحة
st.set_page_config(page_title="AccTables – Smart Accounting Assistant", layout="centered")

# عنوان المشروع
st.title("📊 AccTables – Smart Accounting Assistant")

# شرح مختصر
st.markdown("""
Welcome to AccTables – your smart assistant for building accounting tables.

Write a simple transaction like:  
`Purchased furniture for 10,000 AED`  
`Took a bank loan of 15,000`  
`Owner invested 5,000 AED`

The system will detect whether it's an **Asset**, **Liability**, or **Equity**.
""")

# تصنيف المعاملة
def classify_transaction(text):
    text = text.lower()
    if any(word in text for word in ["purchase", "equipment", "furniture", "asset", "bought"]):
        return "Asset"
    elif any(word in text for word in ["loan", "payable", "borrowed", "debt"]):
        return "Liability"
    elif any(word in text for word in ["capital", "invested", "owner"]):
        return "Equity"
    else:
        return "Unknown"

# استخراج المبلغ
def extract_amount(text):
    match = re.search(r'\d+(?:,\d{3})*(?:\.\d+)?', text)
    return float(match.group().replace(',', '')) if match else 0

# حفظ البيانات المؤقتة
if 'transactions' not in st.session_state:
    st.session_state.transactions = []

# حقل الإدخال
transaction = st.text_input("✍️ Enter your transaction below:")

# زر الإضافة
if st.button("➕ Add Transaction") and transaction:
    category = classify_transaction(transaction)
    amount = extract_amount(transaction)
    st.session_state.transactions.append({
        "Description": transaction,
        "Category": category,
        "Amount": amount
    })

# عرض الجدول الحالي
if st.session_state.transactions:
    df = pd.DataFrame(st.session_state.transactions)
    st.subheader("📋 Transactions Recorded")
    st.dataframe(df)