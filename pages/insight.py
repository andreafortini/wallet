import streamlit as st
from src import plots

st.subheader("📈 Analisi e Andamento del Portafoglio")

tab1, tab2, tab3 = st.tabs(["📊 Composizione", "📉 Evoluzione", "📌 Riepilogo"])

with tab1:
    st.markdown("### Riepilogo del Portafoglio")
    summary = plots.summary_info()
    if summary:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 Valore Totale", f"{summary['total_value']} €")
        col2.metric("💸 Spesa Totale", f"{summary['net_spent']} €")
        col3.metric("📈 Guadagno/Perdita", f"{summary['profit']} €")
        col4.metric("📊 Variazione %", f"{summary['percent']} %")
    else:
        st.info("Dati insufficienti per calcolare il riepilogo.")

with tab2:
    st.markdown("### Soldi Spesi vs Valore del Portafoglio")
    fig = plots.portfolio_evolution_chart()
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Dati insufficienti per mostrare l'evoluzione.")

with tab3:
    st.markdown("### Composizione del Portafoglio")
    fig = plots.portfolio_composition_pie()
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Dati insufficienti per generare il grafico.")
