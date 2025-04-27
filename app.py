
import streamlit as st
import pandas as pd
import re

# إعداد الصفحة
st.set_page_config(page_title="AccTables – Smart Accounting Tables", layout="centered")

st.title("📘 AccTables – Smart Accounting Assistant")

# اختيار نوع الجدول
table_option = st.selectbox("📊 Choose the type of accounting table you want to generate:", ["Balance Sheet", "Income Statement"])

# كلمات رئيسية
asset_keywords = ["purchase", "purchases", "buy", "bought", "equipment", "furniture", "inventory", "vehicle", "land"]
liability_keywords = ["loan", "borrowed", "payable", "debt"]
equity_keywords = ["invested", "capital", "owner", "contribution", "invoice", "bill", "bills", "covered"]
revenue_keywords = ["sales", "revenue", "earned", "income", "service"]
expense_keywords = ["rent", "expense", "salary", "wages", "utilities", "electricity", "supplies", "advertising"]

# تحديد نوع الحساب
def classify_account(text, for_income_statement=False):
    text = text.lower()
    if for_income_statement:
        if any(word in text for word in revenue_keywords):
            return "Revenue"
        elif any(word in text for word in expense_keywords):
            return "Expense"
        else:
            return "Unknown"
    else:
        if any(word in text for word in asset_keywords):
            return "Asset"
        elif any(word in text for word in liability_keywords):
            return "Liability"
        elif any(word in text for word in equity_keywords):
            return "Equity"
        else:
            return "Unknown"

# استخراج المبلغ
def extract_amount(text):
    match = re.search(r'\d+(?:,\d{3})*(?:\.\d+)?', text)
    return float(match.group().replace(',', '')) if match else 0

if "entries" not in st.session_state:
    st.session_state.entries = []

text_input = st.text_input("✍️ Enter a transaction:")
if st.button("➕ Analyze and Add") and text_input:
    if table_option == "Balance Sheet":
        debit = classify_account(text_input)
        credit = "Cash" if "cash" in text_input or "paid" in text_input else "Unknown"
        amount = extract_amount(text_input)
        st.session_state.entries.append({
            "Table": table_option,
            "Description": text_input,
            "Account": debit,
            "Type": "Debit",
            "Amount": amount
        })
        st.session_state.entries.append({
            "Table": table_option,
            "Description": text_input,
            "Account": credit,
            "Type": "Credit",
            "Amount": amount
        })

    elif table_option == "Income Statement":
        account = classify_account(text_input, for_income_statement=True)
        amount = extract_amount(text_input)
        if account != "Unknown":
            st.session_state.entries.append({
                "Table": table_option,
                "Description": text_input,
                "Account": account,
                "Type": "Revenue" if account == "Revenue" else "Expense",
                "Amount": amount
            })
        else:
            st.warning("Could not classify the entry. Please try a different phrasing.")

    st.success("✅ Transaction added and classified!")

if st.session_state.entries:
    st.subheader("📋 Entries")
    df = pd.DataFrame(st.session_state.entries)
    filtered_df = df[df["Table"] == table_option]
    st.dataframe(filtered_df)

    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        filtered_df.to_excel(writer, index=False, sheet_name=table_option.replace(" ", "_"))
    st.download_button("📤 Download as Excel", data=output.getvalue(), file_name=f"{table_option.lower().replace(' ', '_')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
