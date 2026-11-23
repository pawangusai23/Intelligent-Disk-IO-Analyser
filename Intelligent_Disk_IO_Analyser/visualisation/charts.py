
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


def create_movement_chart(result, disk_size):
    """Create an animated disk head movement chart."""

    path = result["movement_path"]
    requests = result["service_order"]

    fig = go.Figure()

    # Disk cylinder track
    fig.add_trace(go.Scatter(
        x=list(range(disk_size)),
        y=[0] * disk_size,
        mode="lines",
        line=dict(color="#334155", width=5),
        name="Disk track"
    ))

    # Requested cylinders
    fig.add_trace(go.Scatter(
        x=requests,
        y=[0] * len(requests),
        mode="markers",
        marker=dict(
            size=13,
            color="#F59E0B",
            symbol="circle"
        ),
        name="Requests"
    ))

    # Head movement path
    fig.add_trace(go.Scatter(
        x=path,
        y=[0.15] * len(path),
        mode="lines+markers",
        line=dict(color="#38BDF8", width=3),
        marker=dict(size=8),
        name="Movement path"
    ))

    # Animated head marker
    fig.add_trace(go.Scatter(
        x=[path[0]],
        y=[0.35],
        mode="markers",
        marker=dict(
            size=19,
            color="#22C55E",
            symbol="diamond"
        ),
        name="Disk head"
    ))

    frames = []

    for i, position in enumerate(path):
        frames.append(go.Frame(
            name=str(i),
            data=[
                go.Scatter(
                    x=[position],
                    y=[0.35]
                )
            ],
            traces=[3]
        ))

    fig.frames = frames

    fig.update_layout(
        title=f"{result['algorithm']} - Disk Head Movement",
        xaxis_title="Cylinder Number",
        yaxis=dict(
            visible=False,
            range=[-0.2, 0.65]
        ),
        xaxis=dict(range=[0, disk_size - 1]),
        template="plotly_dark",
        height=400,
        showlegend=True,
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "buttons": [
                {
                    "label": "Play",
                    "method": "animate",
                    "args": [
                        None,
                        {
                            "frame": {"duration": 650, "redraw": True},
                            "transition": {"duration": 300},
                            "fromcurrent": True
                        }
                    ]
                },
                {
                    "label": "Pause",
                    "method": "animate",
                    "args": [
                        [None],
                        {
                            "frame": {"duration": 0},
                            "mode": "immediate",
                            "transition": {"duration": 0}
                        }
                    ]
                }
            ]
        }]
    )

    return fig


def create_performance_chart(metrics_list):
    """Compare total head movement."""

    df = pd.DataFrame(metrics_list)

    fig = px.bar(
        df,
        x="algorithm",
        y="total_head_movement",
        color="algorithm",
        text="total_head_movement",
        title="Total Disk Head Movement Comparison",
        labels={
            "algorithm": "Scheduling Algorithm",
            "total_head_movement": "Head Movement (Cylinders)"
        },
        template="plotly_dark"
    )

    fig.update_layout(showlegend=False)

    return fig


def create_ranking_chart(recommendation):
    """Display recommendation scores."""

    df = pd.DataFrame(recommendation["rankings"])

    fig = px.bar(
        df,
        x="algorithm",
        y="score",
        color="score",
        text="score",
        title="Intelligent Algorithm Ranking",
        labels={
            "algorithm": "Algorithm",
            "score": "Performance Score"
        },
        template="plotly_dark"
    )

    fig.update_layout(showlegend=False)

    return fig
