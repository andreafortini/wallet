"""Graph functions"""

import plotly.express as px
from src import data_logic


def portfolio_composition_pie():
    df = data_logic.get_current_portfolio_composition()
    if df.empty:
        return None

    fig = px.pie(
        df,
        names="Ticker",
        values="Quantità",
        title="Composizione Attuale del Portafoglio",
    )
    return fig


def portfolio_evolution_chart():
    df = data_logic.get_portfolio_evolution()
    if df.empty:
        return None

    fig = px.line(
        df,
        x="Data",
        y=["Soldi Spesi", "Valore Portafoglio"],
        title="Evoluzione del Portafoglio vs Soldi Spesi",
    )
    return fig


def summary_info():
    return data_logic.get_summary_metrics()
