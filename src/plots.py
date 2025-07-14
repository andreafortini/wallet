"""Graph functions"""

import plotly.express as px
import plotly.graph_objects as go

from src import data_logic


def portfolio_composition_pie():
    df = data_logic.get_current_portfolio_composition()
    if df.empty:
        return None

    # Sort by total value in descending order for plotting
    df_sorted = df.sort_values('Valore_Totale', ascending=False)
    
    # Calculate total value and percentages
    total_value = df_sorted['Valore_Totale'].sum()
    percentages = (df_sorted['Valore_Totale'] / total_value * 100).round(2)
    
    # Create labels with ticker, percentage, and value
    labels = [
        f"{ticker}<br>{pct}%<br>€{val:,.0f}" 
        for ticker, pct, val in zip(
            df_sorted['Ticker'], percentages, df_sorted['Valore_Totale']
        )
    ]
    
    fig = go.Figure(data=[
        go.Pie(
            labels=df_sorted['Ticker'],
            values=df_sorted['Valore_Totale'],
            text=labels,
            textinfo='text',
            textposition='inside',
            textfont=dict(size=14, color='white'),
            hovertemplate=(
                '<b>%{label}</b><br>' +
                'Valore: €%{value:,.0f}<br>' +
                'Percentuale: %{percent}<br>'
            ),
            customdata=df_sorted[['Quantità', 'Prezzo_Attuale']].values,
            hole=0.3,
            marker=dict(
                colors=px.colors.qualitative.Vivid,
                line=dict(color='white', width=2)
            ),
            showlegend=True
        )
    ])
    
    fig.update_layout(
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.01,
            font=dict(size=16)
        ),
        width=800,
        height=600,
        margin=dict(l=50, r=150, t=100, b=50),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # Central annotation
    fig.add_annotation(
        text=f"<b>Totale</b><br>€{total_value:,.0f}",
        x=0.5, y=0.5,
        font_size=16,
        showarrow=False,
        bgcolor="white",
        borderwidth=1
    )
    
    return fig


def portfolio_evolution_chart():
    df = data_logic.get_portfolio_evolution()
    if df.empty:
        return None

    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df["Data"],
        y=df["Soldi Spesi"],
        mode='lines+markers',
        line=dict(shape='hv', color='#e74c3c', width=2),
        marker=dict(size=6, color='#e74c3c'),
        name='Soldi Spesi',
        hovertemplate='<b>Soldi Spesi</b><br>Data: %{x}<br>Valore: €%{y:,.2f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=df["Data"],
        y=df["Valore Portafoglio"],
        mode='lines+markers',
        line=dict(color='#2ecc71', width=2),
        marker=dict(size=6, color='#2ecc71'),
        name='Valore Portafoglio',
        hovertemplate='<b>Valore Portafoglio</b><br>Data: %{x}<br>Valore: €%{y:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title='Data',
        yaxis_title='Valore (€)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified',
        plot_bgcolor='white',
        width=900,
        height=500
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    return fig


def summary_info():
    return data_logic.get_summary_metrics()
