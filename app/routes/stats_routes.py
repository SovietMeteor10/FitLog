from flask import Blueprint, render_template
import pandas as pd
import plotly.graph_objects as go
import numpy as np

stats_bp = Blueprint('statistics', __name__)

@stats_bp.route('/', methods=['GET'])
def statistics():
    line_graph_html = line_graph()
    heatmap_html = heat_map()
    radial_graph_html = radial_graph()
    return render_template('statistics.html', line_graph=line_graph_html, heatmap=heatmap_html, radial_graph=radial_graph_html)

### WE NEED NEW QUERIES IN THESE FUNCTIONS ###

def get_line_graph_data():
    #run a query to get the time series data from the fields that we pass in to this function
    
    #fake data for now:
    dataX = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    dataY = np.random.randint(0, 5, size=len(dataX))
    return dataX, dataY

def get_heat_map_data():
    # Generate a date range for the entire year of 2024
    date_range = pd.date_range(start="2024-01-01", end="2024-12-31", freq='D')
    
    # Generate random values for each date (you can adjust the range as needed)
    values = np.random.randint(0, 2, size=len(date_range))  # Random values between 0 and 1
    
    # Create a DataFrame
    df = pd.DataFrame({'date': date_range, 'value': values})
    
    # Ensure that the 'date' column exists and is in datetime format
    df['date'] = pd.to_datetime(df['date'])
    
    # Add additional columns for day of the week and week of the year
    df['day_of_week'] = df['date'].dt.weekday  # Monday=0, Sunday=6
    df['week_of_year'] = df['date'].dt.isocalendar().week
    
    # Aggregate the data by taking the mean for duplicate combinations
    df_aggregated = df.groupby(['day_of_week', 'week_of_year'])['value'].mean().reset_index()

    # Pivot the DataFrame to create a heatmap format
    heatmap_data = df_aggregated.pivot(index='day_of_week', columns='week_of_year', values='value').fillna(0)

    return heatmap_data

def get_radial_graph():

    # Example data: Replace this with your own data fetching
    labels = ["Arms", "Upper Leg", "Lower Leg", "Chest", "Back", "Abs", "Glutes", "Arms"]

    values = [5, 10, 7, 8, 9, 6, 4, 5]  # remember to put the last value twice!

    return labels, values

def line_graph():

    result = get_line_graph_data()
    if not result:
        print("No data returned from get_line_graph_data")
        return None
    dataX, dataY = result

    fig = go.Figure(data=go.Scatter(x=dataX, y=dataY, mode='lines+markers'))
    fig.update_layout(
        xaxis_title="X Axis",
        yaxis_title="Y Axis",

        modebar_remove=['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'resetScale', 'hoverClosestCartesian', 'hoverCompareCartesian', 'toImage', 'autoscale','lasso2d'],
        plot_bgcolor='#333',  # Background color of the plot area
        paper_bgcolor='#333',  # Background color of the entire figure
        font=dict(
            color='white',  # Text color
        ),
        xaxis=dict(title='Day of the Week'),
        yaxis=dict(title='Session Hours'),
    )

    return fig.to_html(full_html=False)

def heat_map():

    data = get_heat_map_data()

    # Check that the data is a DataFrame and is correctly formatted
    if isinstance(data, pd.DataFrame):
        # Directly use the data (no aggregation)
        heatmap_data = data.fillna(0)

        # Create the heatmap figure
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,  # 1-52 weeks
            y=['Mon  ', 'Tue  ', 'Wed  ', 'Thu  ', 'Fri  ', 'Sat  ', 'Sun  '],
            colorscale='Greens',
            showscale=False,
            hoverinfo='none'
        ))

        # Define the months and create the x-axis labels
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        tickvals = list(range(4, 52))  # Week numbers 1 to 52
        ticktext = ['' for _ in tickvals]  # Start with empty text for all ticks

        # Set month labels at every fourth tick (1st, 5th, 9th, etc.)
        for i in range(0, len(tickvals), 4):
            # Use modulus to cycle through the months (i % 12) ensures we stay within the bounds of the months list
            ticktext[i] = months[(i // 4) % 12]  # Assign months to every fourth tick

        fig.update_layout(
            dragmode=False,
            clickmode='none',
            modebar_remove=['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'resetScale', 'hoverClosestCartesian', 'hoverCompareCartesian', 'toImage', 'autoscale'],
            plot_bgcolor='#333',  # Background color of the plot area
            paper_bgcolor='#333',
            font=dict(
                family='Arial',  # Font family for text
                size=14,  # Font size
                color='rgb(0, 0, 0)'  # Font color (black in this case)
            ),
            xaxis=dict(
                title='Month',
                titlefont=dict(color='#e0e0e0'),  # X-axis title color
                tickfont=dict(color='#e0e0e0'),  # X-axis tick labels color
                tickvals=tickvals,  # Use the week numbers for tick positions
                ticktext=ticktext  # Add month labels at every fourth tick
            ),
            yaxis=dict(
                title='Day of the Week',
                titlefont=dict(color='#e0e0e0'),  # Y-axis title color
                tickfont=dict(color='#e0e0e0')  # Y-axis tick labels color
            ),
            margin=dict(l=120)
        )

        # Return the heatmap as HTML
        return fig.to_html(full_html=False)

    else:
        print("Data is not a DataFrame!")
        return ""

def radial_graph():
    labels, values = get_radial_graph()
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=labels,
        mode='lines+markers',  # Use 'lines' for a line or 'lines+markers' to show both
        line=dict(color='orange', width=2),
        opacity=0.8,
        fill='toself',  # This will fill the area under the line
        fillcolor='rgba(0, 0, 255, 0.2)'  # Set the fill color with some transparency
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0, max(values)]),
            bgcolor='#1e1e1e',
        ),
        showlegend=False,

        modebar_remove=['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'resetScale', 'hoverClosestCartesian', 'hoverCompareCartesian', 'toImage', 'autoscale','lasso2d'],

        plot_bgcolor='#333',  # Background color of the plot area
        paper_bgcolor='#333',  # Background color of the entire figure
        font=dict(
            color='white',  # Text color
        )
    )
    return fig.to_html(full_html=False)

