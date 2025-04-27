
import streamlit as st
import pandas as pd
import re

# إعداد الصفحة
st.set_page_config(page_title="AccTables – Smart Transaction Classifier", layout="centered")

st.title("📘 AccTables – Smart Accounting Assistant")

st.markdown("""
Type your transaction below using simple natural language.  
The system will auto-classify the transaction, determine debit and credit accounts, and show the journal entry.
""")

# الكلمات المفتاحية حسب التصنيف
asset_keywords = ["purchase", "purchases", "buy", "bought", "equipment", "furniture", "inventory", "vehicle", "land"]
liability_keywords = ["loan", "borrowed", "payable", "debt"]
equity_keywords = ["invested", "capital", "owner", "contribution"]

# تحليل الجملة لتحديد نوع الحسابات
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

    # نفترض أن الدفع نقدًا إلا إذا وُجد شيء ثاني
    if "cash" in text or "paid" in text:
        credit = "Cash"
    elif "loan" in text or "borrowed" in text:
        credit = "Loan"
    elif "owner" in text or "capital" in text or "invested" in text:
        credit = "Owner's Equity"
    else:
        credit = "Unknown"

    return debit, credit

# استخراج المبلغ من النص
def extract_amount(text):
    match = re.search(r'\d+(?:,\d{3})*(?:\.\d+)?', text)
    return float(match.group().replace(',', '')) if match else 0

# تخزين القيد
if "entries" not in st.session_state:
    st.session_state.entries = []

# إدخال المستخدم
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

# عرض القيود
if st.session_state.entries:
    st.subheader("📋 Journal Entries")
    df = pd.DataFrame(st.session_state.entries)
    st.dataframe(df)

    # تنزيل الملف
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Journal')
    st.download_button("📤 Download as Excel", data=output.getvalue(), file_name="journal.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
