from flask import Blueprint, render_template, session
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import func, extract, desc, distinct
from app.models import Session, Exercise, SessionExercise, User
from app.database import db_session
from datetime import date, timedelta

stats_bp = Blueprint("statistics", __name__)


@stats_bp.route("/", methods=["GET"])
def statistics():
    line_graph_html = line_graph()
    heatmap_html = heat_map()
    radial_graph_html = radial_graph()

    most_common_exercise = (
        db_session.query(
            Exercise.exercise_name, func.count(Exercise.exercise_id).label("count")
        )
        .join(SessionExercise)
        .join(Session)
        .filter(Session.user_id == session.get("user_id"))
        .group_by(Exercise.exercise_id)
        .order_by(desc("count"))
        .first()
    )

    most_common_muscle_group = (
        db_session.query(
            Exercise.category, func.count(distinct(Session.session_id)).label("count")
        )
        .select_from(Session)
        .join(SessionExercise)
        .join(Exercise)
        .filter(Session.user_id == session.get("user_id"))
        .group_by(Exercise.category)
        .order_by(desc("count"))
        .first()
    )

    least_common_exercise = (
        db_session.query(
            Exercise.exercise_name, func.count(Exercise.exercise_id).label("count")
        )
        .join(SessionExercise)
        .join(Session)
        .filter(Session.user_id == session.get("user_id"))
        .group_by(Exercise.exercise_id)
        .order_by("count")
        .first()
    )

    least_common_muscle_group = (
        db_session.query(
            Exercise.category, func.count(distinct(Session.session_id)).label("count")
        )
        .select_from(Session)
        .join(SessionExercise)
        .join(Exercise)
        .filter(Session.user_id == session.get("user_id"))
        .group_by(Exercise.category)
        .order_by("count")
        .first()
    )

    user = db_session.query(User).filter(User.user_id == session.get("user_id")).first()

    # Calculate BMI
    bmi = None
    if user and user.weight and user.height:
        bmi = user.weight / ((user.height / 100) ** 2)

    summary_statistics = {
        "most_common_exercise": (
            most_common_exercise.exercise_name if most_common_exercise else None
        ),
        "most_common_muscle_group": (
            most_common_muscle_group.category if most_common_muscle_group else None
        ),
        "least_common_exercise": (
            least_common_exercise.exercise_name if least_common_exercise else None
        ),
        "least_common_muscle_group": (
            least_common_muscle_group.category if least_common_muscle_group else None
        ),
        "bmi": round(bmi, 2) if bmi else None,
    }

    return render_template(
        "statistics.html",
        line_graph=line_graph_html,
        heatmap=heatmap_html,
        radial_graph=radial_graph_html,
        summary_statistics=summary_statistics,
    )


# WE NEED NEW QUERIES IN THESE FUNCTIONS ###


def get_line_graph_data():
    today = date.today()
    last_seven_days = [(today - timedelta(days=i)).isoformat() for i in range(7)]

    # Query to get the sum of durations for each day in the last 7 days
    query = (
        db_session.query(
            func.date(Session.date).label("day"),
            func.coalesce(func.sum(Session.duration), 0).label("total_duration"),
        )
        .filter(
            Session.user_id == session.get("user_id"),
            Session.date >= today - timedelta(days=6),
        )
        .group_by(func.date(Session.date))
    )

    # Execute the query and fetch results
    results = {row.day.isoformat(): row.total_duration for row in query.all()}

    # Create the final list, filling in zeros for days without sessions
    durations = [results.get(day, 0) for day in last_seven_days]

    return last_seven_days[::-1], durations[::-1]


def get_heat_map_data():
    # Generate a date range for the entire year of 2024
    query = (
        db_session.query(
            extract("dow", Session.date).label("day_of_week"),
            extract("week", Session.date).label("week_of_year"),
            func.count(Session.session_id).label("session_count"),
        )
        .filter(Session.user_id == session.get("user_id"))
        .group_by(extract("dow", Session.date), extract("week", Session.date))
    )

    results = query.all()

    df = pd.DataFrame(results, columns=["day_of_week", "week_of_year", "session_count"])

    all_days = pd.DataFrame({"day_of_week": range(7)})
    all_weeks = pd.DataFrame({"week_of_year": range(1, 54)})
    complete_grid = all_days.merge(all_weeks, how="cross")

    df = complete_grid.merge(df, on=["day_of_week", "week_of_year"], how="left").fillna(
        0
    )

    # Pivot the DataFrame to create the heatmap format
    heatmap_df = df.pivot(
        index="day_of_week", columns="week_of_year", values="session_count"
    )

    # Replace NaN values with 0
    heatmap_df = heatmap_df.fillna(0)

    # Rename the index to day names
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    heatmap_df.index = day_names

    return heatmap_df


def get_radial_graph():
    query = (
        db_session.query(
            Exercise.category, func.count(Exercise.exercise_id).label("category_count")
        )
        .join(SessionExercise)
        .join(Session)
        .filter(Session.user_id == session.get("user_id"))
        .filter(Exercise.category.isnot(None))
        .group_by(Exercise.category)
        .order_by(Exercise.category)
    )

    results = query.all()

    labels = [category for category, _ in results]
    if len(labels) != 0:
        labels.append(labels[0])
    values = [count for _, count in results]
    if len(values) != 0:
        values.append(values[0])

    return labels, values


def line_graph():
    result = get_line_graph_data()
    if not result:
        print("No data returned from get_line_graph_data")
        return None
    dataX, dataY = result

    fig = go.Figure(data=go.Scatter(x=dataX, y=dataY, mode="lines+markers"))
    fig.update_layout(
        xaxis_title="X Axis",
        yaxis_title="Y Axis",
        modebar_remove=[
            "zoom",
            "pan",
            "select",
            "zoomIn",
            "zoomOut",
            "resetScale",
            "hoverClosestCartesian",
            "hoverCompareCartesian",
            "toImage",
            "autoscale",
            "lasso2d",
        ],
        plot_bgcolor="#1c1c1c",  # Background color of the plot area
        paper_bgcolor="#1c1c1c",  # Background color of the entire figure
        font=dict(
            color="white",  # Text color
        ),
        xaxis=dict(title="Day of the Week"),
        yaxis=dict(title="Session Hours"),
    )

    return fig.to_html(full_html=False)


def heat_map():

    data = get_heat_map_data()

    # Check that the data is a DataFrame and is correctly formatted
    if isinstance(data, pd.DataFrame):
        # Directly use the data (no aggregation)
        heatmap_data = data.fillna(0)

        # Create the heatmap figure
        fig = go.Figure(
            data=go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns,  # 1-52 weeks
                y=["Mon  ", "Tue  ", "Wed  ", "Thu  ", "Fri  ", "Sat  ", "Sun  "],
                colorscale="Greens",
                showscale=False,
                hoverinfo="none",
            )
        )

        # Define the months and create the x-axis labels
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        tickvals = list(range(4, 52))  # Week numbers 1 to 52
        ticktext = ["" for _ in tickvals]  # Start with empty text for all ticks

        # Set month labels at every fourth tick (1st, 5th, 9th, etc.)
        for i in range(0, len(tickvals), 4):
            # Use modulus to cycle through the months (i % 12) ensures we stay within the bounds of the months list
            ticktext[i] = months[(i // 4) % 12]  # Assign months to every fourth tick

        fig.update_layout(
            dragmode=False,
            clickmode="none",
            modebar_remove=[
                "zoom",
                "pan",
                "select",
                "zoomIn",
                "zoomOut",
                "resetScale",
                "hoverClosestCartesian",
                "hoverCompareCartesian",
                "toImage",
                "autoscale",
            ],
            plot_bgcolor="#1c1c1c",  # Background color of the plot area
            paper_bgcolor="#1c1c1c",
            font=dict(
                family="Arial",  # Font family for text
                size=14,  # Font size
                color="rgb(0, 0, 0)",  # Font color (black in this case)
            ),
            xaxis=dict(
                title="Month",
                titlefont=dict(color="#e0e0e0"),  # X-axis title color
                tickfont=dict(color="#e0e0e0"),  # X-axis tick labels color
                tickvals=tickvals,  # Use the week numbers for tick positions
                ticktext=ticktext,  # Add month labels at every fourth tick
            ),
            yaxis=dict(
                title="Day of the Week",
                titlefont=dict(color="#e0e0e0"),  # Y-axis title color
                tickfont=dict(color="#e0e0e0"),  # Y-axis tick labels color
            ),
            margin=dict(l=120),
        )

        # Return the heatmap as HTML
        return fig.to_html(full_html=False)

    else:
        print("Data is not a DataFrame!")
        return ""


def radial_graph():
    labels, values = get_radial_graph()
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=labels,
            mode="lines+markers",  # Use 'lines' for a line or 'lines+markers' to show both
            line=dict(color="orange", width=2),
            opacity=0.8,
            fill="toself",  # This will fill the area under the line
            fillcolor="rgba(0, 0, 255, 0.2)",  # Set the fill color with some transparency
        )
    )
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0, max(values)]),
            bgcolor="#1c1c1c",
        ),
        showlegend=False,
        modebar_remove=[
            "zoom",
            "pan",
            "select",
            "zoomIn",
            "zoomOut",
            "resetScale",
            "hoverClosestCartesian",
            "hoverCompareCartesian",
            "toImage",
            "autoscale",
            "lasso2d",
        ],
        plot_bgcolor="#1c1c1c",  # Background color of the plot area
        paper_bgcolor="#1c1c1c",  # Background color of the entire figure
        font=dict(
            color="white",  # Text color
        ),
    )
    return fig.to_html(full_html=False)
