"""
Utility functions for the US funds analysis web application.
"""

# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def config_menu_footer() -> None:
    """
    Hides the Streamlit menu and replaces footer.
    """
    app_style = """
        <style>
            #MainMenu {
              visibility: hidden;
            }
            footer {
                visibility: hidden;
            }
            footer:before {
            content:"Copyright © 2024 Carla Teixeira Coutinho";
            visibility: visible;
            display: block;
            position: relative;
            text-align: center;
            }
        </style>
    """

    st.markdown(app_style, unsafe_allow_html=True)


def get_delta(df: pd.DataFrame, key: str) -> str:
    """
    Calculates the real percentage difference between the first two values for a given key in a Pandas DataFrame.

    Parameters:
        df (pandas.DataFrame): DataFrame containing financial data.
        key (str): The key for which to calculate the percentage difference.

    Returns:
        str: A string representation of the percentage difference with a percent sign at the end.
    """
    if key not in df.columns:
        return f"Key '{key}' not found in DataFrame columns."

    if len(df) < 2:
        return "DataFrame must contain at least two rows."

    val1 = df[key][1]
    val2 = df[key][0]

    # Handle cases where either value is negative or zero
    if val1 <= 0 or val2 <= 0:
        delta = (val2 - val1) / abs(val1) * 100
    else:
        delta = (val2 - val1) / val1 * 100

    # Round to two decimal places and return the result
    return f"{delta:.2f}%"


def empty_lines(n: int) -> None:
    """
    Inserts empty lines to separate content.

    Parameters:
        n (int): The number of empty lines to insert.
    """
    for _ in range(n):
        st.write("")


def generate_card(text: str) -> None:
    """
    Generates a styled card with a title and icon.

    Parameters:
        text (str): The title text for the card.
    """
    st.markdown(
        f"""
        <div style='border: 1px solid #e6e6e6; border-radius: 5px; padding: 10px; display: flex; justify-content: center; align-items: center'>
            <i class='fas fa-chart-line' style='font-size: 24px; color: #0072C6; margin-right: 10px'></i>
            <h3 style='text-align: center'>{text}</h3>
        </div>
         """,
        unsafe_allow_html=True,
    )


def generate_investment_profile(
    fund_long_name,
    fund_category,
    total_net_assets,
    inception_date,
    fund_family,
    currency,
    exchange_name,
    exchange_code,
    region,
) -> None:
    """
    Generates a styled card with a title and icon.

    Parameters:
        text (str): The title text for the card.
    """
    st.markdown(
        f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Investment Table</title>
                <style>
                    .mod-ui-table {{
                        width: 100%;
                        border-collapse: collapse;
                    }}
                    .mod-ui-table th, .mod-ui-table td {{
                        text-align: left;
                        padding: 8px;
                        border-bottom: 1px solid #ddd;
                    }}
                    .mod-ui-table--two-column th {{
                        background-color: #f2f2f2;
                    }}
                    .mod-profile-and-investment-app__table--invest td .mod-format__currency {{
                        font-style: italic;
                    }}
                </style>
            </head>
            <body>
                <table class="mod-ui-table mod-ui-table--two-column mod-profile-and-investment-app__table--invest">
                    <tbody>
                        <tr>
                            <th>Fund Name</th>
                            <td>{fund_long_name}</td>
                        </tr>
                        <tr>
                            <th>Fund Category</th>
                            <td>{fund_category}</td>
                        </tr>
                        <tr>
                            <th>Total net assets</th>
                            <td>{total_net_assets}</td>
                        </tr>
                        <tr>
                            <th>Inception date</th>
                            <td>{inception_date}</td>
                        </tr>
                        <tr>
                            <th>Fund Family</th>
                            <td>
                                <div>{fund_family}</div>
                            </td>
                        </tr>
                        <tr>
                            <th>Currency</th>
                            <td>
                                <div>{currency}</div>
                            </td>
                        </tr>
                        <tr>
                            <th>Exchange Name</th>
                            <td>{exchange_name}</td>
                        </tr>
                        <tr>
                            <th>Exchange code</th>
                            <td>{exchange_code}</td>
                        </tr>
                        <tr>
                            <th>Region</th>
                            <td>{region}</td>
                        </tr>
                    </tbody>
                </table>
            </body>
            </html>""",
        unsafe_allow_html=True,
    )


def generate_long_text(text: str) -> None:
    """
    Generates a styled card with a title and icon.

    Parameters:
        text (str): The title text for the card.
    """
    st.markdown(
        f"""
        <div style='border: 1px solid #e6e6e6; border-radius: 5px; padding: 10px; display: flex; justify-content: flex-start; align-items: center'>
            <i class='fas fa-chart-line' style='font-size: 24px; color: #0072C6; margin-right: 10px'></i>
            <h3 style='text-align: left; margin: 0'>{text}</h3>
        </div>
         """,
        unsafe_allow_html=True,
    )


def color_highlighter(val: str) -> str:
    """
    Returns CSS styling for a pandas DataFrame cell based on whether its value is positive or negative.

    Parameters:
        val (str): The cell value.

    Returns:
        str: The CSS styling string.
    """
    if val.startswith("-"):
        return "color: rgba(255, 0, 0, 0.9);"
    else:
        return None


def create_donut_chart(
    labels,
    values,
    hole_size=0.3,
    title_text="Your Chart Title",
    hoverinfo="label+percent",
):
    """
    Creates a Plotly donut chart.

    Parameters:
    - labels: The labels for each segment of the donut chart.
    - values: The values for each segment of the donut chart.
    - hole_size: The size of the donut hole. Default is 0.3.
    - title_text: The title of the chart.
    - hoverinfo: The information to show on hover. Default is 'label+percent'.

    Returns:
    - A Plotly figure object representing the donut chart.
    """
    fig = go.Figure()
    fig.add_trace(
        go.Pie(
            labels=labels,
            values=values,
            textinfo=hoverinfo,
            showlegend=False,
            hovertemplate="<b>%{label}</b><br>%{value}<br><extra></extra>",
            hole=hole_size,
        )
    )

    fig.update_layout(
        title=dict(text=title_text),
        annotations=[dict(text="", x=1, y=1, font_size=12, showarrow=False)],
    )

    return fig


def create_candlestick_chart(df_fact_etf):
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df_fact_etf["price_date"],
                open=df_fact_etf["open"],
                high=df_fact_etf["high"],
                low=df_fact_etf["low"],
                close=df_fact_etf["close"],
                increasing_line_color="green",
                decreasing_line_color="red",
            )
        ]
    )
    fig.update_layout(
        title="Open, High, Low, Close (OHLC)", xaxis_title="Date", yaxis_title="Price"
    )
    return fig


def create_volume_chart(df_fact_etf):
    fig = go.Figure(
        data=[
            go.Scatter(
                x=df_fact_etf["price_date"],
                y=df_fact_etf["volume"],
                line=dict(color="blue"),
            )
        ]
    )
    fig.update_layout(title="Trading Volume", xaxis_title="Date", yaxis_title="Volume")
    return fig
