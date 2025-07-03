import streamlit as st

from src import data_loader, data_logic

st.set_page_config(page_title="Portfolio Manager", layout="wide")

st.title("💼 Portfolio Manager")

tab1, tab2, tab3 = st.tabs(
    ["📥 Insert Order", "🏷️ Securities Details", "📊 Securities History"]
)

with tab1:
    st.subheader("Insert new order")
    with st.form("order_form", clear_on_submit=True):
        isin = st.multiselect("ISIN", options=data_logic.get_isin(), max_selections=1)

        col1, col2 = st.columns(2)
        with col1:
            quantity = st.number_input("Quantity", step=1.0)
            date = st.date_input("Date")
        with col2:
            price = st.number_input("Price", step=0.01)
            operation = st.selectbox("Operation type", ["Buy", "Sell"])

        submitted = st.form_submit_button("Save order")
        if submitted:
            data_loader.save_order(
                data_logic.get_ticker_from_isin(isin),
                isin,
                quantity,
                price,
                date,
                operation,
            )
            st.success("Order saved!")

    st.markdown("### 📄 Order History")
    st.dataframe(data_loader.load_orders())

with tab2:
    st.subheader("Insert/Change Security Detail")
    with st.form("security_form", clear_on_submit=True):
        ticker = st.text_input("Security Ticker")
        isin = st.text_input("Security ISIN")
        fullname = st.text_input("Full Name")
        category = st.selectbox("Category", ["Stock", "Bond"])
        submitted = st.form_submit_button("Save Detail")
        if submitted:
            data_loader.save_security(ticker, isin, fullname, category)
            st.success("Security detail saved!")

    st.markdown("### 🧾 Security List")
    st.dataframe(data_loader.load_securities())

with tab3:
    st.subheader("Insert an Historic Value")
    with st.form("price_form", clear_on_submit=True):
        isin = st.multiselect("ISIN", options=data_logic.get_isin(), max_selections=1)
        price = st.number_input("Value", step=0.01)
        date = st.date_input("Date")
        submitted = st.form_submit_button("Save value")
        if submitted:
            data_loader.save_price(
                data_logic.get_ticker_from_isin(isin), isin, price, date
            )
            st.success("Value saved!")

    st.markdown("### 📈 Price History")
    st.dataframe(data_loader.load_prices())
