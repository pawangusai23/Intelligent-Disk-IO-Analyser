import streamlit as st
import pandas as pd

from reports.pdf_report import generate_pdf_report
from algorithms.disk_algorithms import run_algorithm
from core.metrics import calculate_metrics
from core.recommender import recommend_algorithm
from visualisation.charts import (
    create_movement_chart,
    create_performance_chart,
    create_ranking_chart,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Intelligent Disk I/O Analyser",
    page_icon="💽",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DESIGN SYSTEM
# ============================================================

st.markdown(
    """
    <style>
    /* ---------- Global canvas and typography ---------- */
    :root {
        --app-bg: #F4F7FC;
        --surface: #FFFFFF;
        --sidebar: #17243A;
        --sidebar-muted: #A9B7CC;
        --text: #17243A;
        --muted: #64748B;
        --primary: #356AE6;
        --primary-dark: #2856C5;
        --border: #E2E8F0;
        --success-bg: #EAF7F0;
        --success: #16865B;
        --warning-bg: #FFF7E6;
        --warning: #A66A08;
    }

    html, body, [class*="css"] {
        font-family: Inter, "Segoe UI", Arial, sans-serif;
    }

    .stApp {
        background: var(--app-bg);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(244, 247, 252, 0.92);
    }

    [data-testid="stMain"] {
        background: var(--app-bg);
    }

    .block-container {
        max-width: 1480px;
        padding-top: 2.0rem;
        padding-bottom: 2.5rem;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: var(--sidebar);
        border-right: 1px solid #263750;
    }

    section[data-testid="stSidebar"] > div {
        background: var(--sidebar);
    }

    section[data-testid="stSidebar"] * {
        color: #E8EEF8;
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] label {
        color: var(--sidebar-muted) !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        letter-spacing: -0.02em;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] > label {
        color: #A9B7CC !important;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] {
        gap: 0.25rem;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label {
        background: transparent;
        border-radius: 9px;
        padding: 0.45rem 0.65rem;
        transition: background 0.15s ease;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: #243650;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
        background: #29466F;
        border: 1px solid #426BA5;
    }

    section[data-testid="stSidebar"] [data-testid="stNumberInput"] input,
    section[data-testid="stSidebar"] [data-testid="stTextInput"] input,
    section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] {
        background: #FFFFFF !important;
        color: #17243A !important;
        border-radius: 8px !important;
    }

    section[data-testid="stSidebar"] [data-testid="stNumberInput"] button {
        color: #17243A !important;
    }

    .sidebar-brand {
        padding: 0.4rem 0 1.1rem 0;
        border-bottom: 1px solid #34445D;
        margin-bottom: 1.2rem;
    }

    .sidebar-brand-mark {
        font-size: 1.8rem;
        line-height: 1.2;
    }

    .sidebar-brand-name {
        color: #FFFFFF;
        font-size: 1.05rem;
        font-weight: 750;
        margin-top: 0.35rem;
    }

    .sidebar-brand-caption {
        color: #A9B7CC;
        font-size: 0.76rem;
        margin-top: 0.2rem;
    }

    .sidebar-section {
        color: #FFFFFF;
        font-size: 0.88rem;
        font-weight: 700;
        margin: 1.25rem 0 0.5rem 0;
    }

    .sidebar-help {
        color: #A9B7CC;
        font-size: 0.76rem;
        line-height: 1.5;
        margin-top: 0.5rem;
    }

    /* ---------- Headings and text ---------- */
    h1, h2, h3 {
        color: var(--text) !important;
        letter-spacing: -0.035em;
    }

    h1 {
        font-weight: 800 !important;
    }

    h2, h3 {
        font-weight: 750 !important;
    }

    p, li, span, label {
        color: inherit;
    }

    [data-testid="stMarkdownContainer"] p {
        color: var(--muted);
    }

    .page-eyebrow {
        color: var(--primary);
        font-size: 0.73rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .page-subtitle {
        color: var(--muted);
        font-size: 0.96rem;
        margin-top: -0.35rem;
        margin-bottom: 1.35rem;
    }

    .section-kicker {
        color: var(--muted);
        font-size: 0.77rem;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.45rem;
    }

    /* ---------- Cards ---------- */
    .hero-card {
        background: linear-gradient(115deg, #FFFFFF 0%, #EEF4FF 100%);
        border: 1px solid #DCE7FA;
        border-radius: 16px;
        padding: 1.45rem 1.6rem;
        margin: 0.35rem 0 1.25rem 0;
        box-shadow: 0 5px 18px rgba(30, 64, 120, 0.045);
    }

    .hero-title {
        color: #17243A;
        font-size: 1.45rem;
        font-weight: 800;
        letter-spacing: -0.035em;
        margin-bottom: 0.3rem;
    }

    .hero-copy {
        color: #64748B;
        font-size: 0.9rem;
        line-height: 1.55;
    }

    .metric-shell {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 13px;
        padding: 0.85rem 1rem;
        box-shadow: 0 3px 12px rgba(23, 36, 58, 0.035);
        min-height: 112px;
    }

    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 13px;
        padding: 0.95rem 1rem;
        box-shadow: 0 3px 12px rgba(23, 36, 58, 0.035);
    }

    [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-size: 0.82rem !important;
        font-weight: 650 !important;
    }

    [data-testid="stMetricValue"] {
        color: #17243A !important;
        font-weight: 800 !important;
    }

    .recommendation-card {
        background: linear-gradient(115deg, #EAF7F0 0%, #F5FBF7 100%);
        border: 1px solid #B9E4CC;
        border-left: 5px solid #16865B;
        border-radius: 14px;
        padding: 1.25rem 1.4rem;
        margin: 0.7rem 0 1rem 0;
    }

    .recommendation-label {
        color: #16865B;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .recommendation-name {
        color: #145C40;
        font-size: 2rem;
        font-weight: 850;
        margin: 0.15rem 0 0.25rem 0;
        letter-spacing: -0.04em;
    }

    .recommendation-copy {
        color: #426B59;
        font-size: 0.9rem;
        line-height: 1.55;
    }

    .info-strip {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 11px;
        padding: 0.85rem 1rem;
        color: #475569;
        font-size: 0.86rem;
        line-height: 1.5;
    }

    /* ---------- Streamlit widgets ---------- */
    div.stButton > button,
    div.stDownloadButton > button {
        border-radius: 9px;
        font-weight: 700;
        border: 1px solid #D5DFEF;
        min-height: 2.65rem;
    }

    div.stButton > button[kind="primary"],
    div.stDownloadButton > button[kind="primary"] {
        background: var(--primary);
        border-color: var(--primary);
        color: #FFFFFF;
    }

    div.stButton > button[kind="primary"]:hover,
    div.stDownloadButton > button[kind="primary"]:hover {
        background: var(--primary-dark);
        border-color: var(--primary-dark);
        color: #FFFFFF;
    }

    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
    }

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    hr {
        border-color: #E2E8F0 !important;
    }

    .app-footer {
        border-top: 1px solid #E2E8F0;
        margin-top: 2.5rem;
        padding-top: 1rem;
        color: #94A3B8;
        font-size: 0.76rem;
        text-align: center;
    }

    /* Keep the interface usable on narrower screens */
    @media (max-width: 768px) {
        .block-container {
            padding: 1.1rem 1rem 2rem 1rem;
        }
        .hero-title {
            font-size: 1.2rem;
        }
        .recommendation-name {
            font-size: 1.65rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR: NAVIGATION AND DISK CONFIGURATION
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-mark">💽</div>
            <div class="sidebar-brand-name">Disk I/O Analyser</div>
            <div class="sidebar-brand-caption">Advanced Operating Systems Project</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-section">Workspace</div>', unsafe_allow_html=True)

    page = st.radio(
        "Select module",
        [
            "Dashboard",
            "Disk Simulator",
            "Performance Analysis",
            "Intelligent Recommendation",
            "Reports",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown('<div class="sidebar-section">Disk configuration</div>', unsafe_allow_html=True)

    disk_size = st.number_input(
        "Disk size (cylinders)",
        min_value=2,
        max_value=10000,
        value=200,
        step=1,
    )

    head = st.number_input(
        "Initial head position",
        min_value=0,
        max_value=int(disk_size) - 1,
        value=min(53, int(disk_size) - 1),
        step=1,
    )

    request_input = st.text_area(
        "Disk request queue",
        value="98, 183, 37, 122, 14, 124, 65, 67",
        height=88,
        help="Enter cylinder numbers separated by commas.",
    )

    direction = st.selectbox(
        "Initial direction",
        ["right", "left"],
        format_func=lambda value: "Right" if value == "right" else "Left",
    )

    seek_time = st.number_input(
        "Seek time per cylinder (ms)",
        min_value=0.001,
        max_value=100.0,
        value=0.1,
        step=0.01,
        format="%.3f",
    )

    objective = st.selectbox(
        "Recommendation objective",
        ["balanced", "minimum_movement"],
        format_func=lambda value: (
            "Balanced performance"
            if value == "balanced"
            else "Minimum head movement"
        ),
    )

    st.markdown(
        """
        <div class="sidebar-help">
            Change the configuration above to recalculate all six scheduling
            algorithms and update the analysis throughout the application.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# INPUT VALIDATION
# ============================================================

try:
    raw_items = [item.strip() for item in request_input.split(",") if item.strip()]

    if not raw_items:
        raise ValueError("Enter at least one disk request.")

    try:
        requests = [int(item) for item in raw_items]
    except ValueError:
        raise ValueError("All disk requests must be whole numbers separated by commas.")

    if any(value < 0 or value >= int(disk_size) for value in requests):
        raise ValueError(
            f"Every request must be between 0 and {int(disk_size) - 1}."
        )

    if len(requests) != len(set(requests)):
        raise ValueError(
            "Duplicate requests are not supported in the current algorithm implementation."
        )

    if not 0 <= int(head) < int(disk_size):
        raise ValueError("Initial head position is outside the disk range.")

    input_valid = True

except ValueError as error:
    requests = []
    input_valid = False
    validation_error = str(error)


# ============================================================
# SHARED SIMULATION DATA
# ============================================================

algorithm_names = ["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"]

results = {}
all_metrics = []
recommendation = None
metrics_df = pd.DataFrame()

if input_valid:
    for algorithm_name in algorithm_names:
        result = run_algorithm(
            name=algorithm_name,
            requests=requests,
            head=int(head),
            disk_size=int(disk_size),
            direction=direction,
        )

        metrics = calculate_metrics(
            result,
            seek_time_per_cylinder=seek_time,
            direction=direction,
        )

        results[algorithm_name] = result
        all_metrics.append(metrics)

    recommendation = recommend_algorithm(
        all_metrics,
        objective=objective,
    )
    metrics_df = pd.DataFrame(all_metrics)


# ============================================================
# REUSABLE UI HELPERS
# ============================================================

def page_header(eyebrow, title, subtitle):
    st.markdown(f'<div class="page-eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def show_recommendation_card(recommendation_data, compact=False):
    best = recommendation_data["recommended_algorithm"]
    reason = recommendation_data["reason"]
    score = recommendation_data.get("recommended_score")

    score_line = ""
    if score is not None and not compact:
        score_line = f'<div class="recommendation-copy">Performance score: <strong>{score}</strong></div>'

    st.markdown(
        f"""
        <div class="recommendation-card">
            <div class="recommendation-label">Recommended algorithm</div>
            <div class="recommendation-name">{best}</div>
            <div class="recommendation-copy">{reason}</div>
            {score_line}
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_metrics_table(dataframe):
    display_df = dataframe.copy()

    column_labels = {
        "algorithm": "Algorithm",
        "total_head_movement": "Total movement",
        "average_head_movement": "Average movement",
        "direction_changes": "Direction changes",
        "requests_serviced": "Requests serviced",
        "estimated_seek_time_ms": "Estimated seek time (ms)",
    }

    display_df = display_df.rename(columns=column_labels)

    numeric_formats = {}
    for column in ["Average movement", "Estimated seek time (ms)"]:
        if column in display_df.columns:
            numeric_formats[column] = "{:.2f}"

    st.dataframe(
        display_df.style.format(numeric_formats),
        use_container_width=True,
        hide_index=True,
    )


def show_footer():
    st.markdown(
        """
        <div class="app-footer">
            Intelligent Disk I/O Scheduling Analyser
            &nbsp;•&nbsp; Advanced Operating Systems Mini Project
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# APPLICATION HEADER
# ============================================================

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">💽 Intelligent Disk I/O Scheduling Analyser</div>
        <div class="hero-copy">
            Compare disk scheduling strategies, inspect head movement,
            evaluate performance metrics and generate simulation reports.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not input_valid:
    st.error(f"Disk configuration needs attention: {validation_error}")
    st.info("Correct the highlighted configuration in the sidebar. The analysis will update automatically.")


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":
    page_header(
        "Overview",
        "System dashboard",
        "A consolidated view of the current disk workload and scheduling results.",
    )

    if input_valid:
        best = recommendation["recommended_algorithm"]

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Disk cylinders", f"{int(disk_size):,}")
        k2.metric("Initial head", f"{int(head):,}")
        k3.metric("Requests in queue", len(requests))
        k4.metric("Recommended", best)

        st.write("")
        show_recommendation_card(recommendation, compact=True)

        left, right = st.columns([1.5, 1], gap="large")

        with left:
            st.subheader("Head movement comparison")
            st.plotly_chart(
                create_performance_chart(all_metrics),
                use_container_width=True,
                config={"displayModeBar": True, "displaylogo": False},
            )

        with right:
            st.subheader("Workload configuration")
            st.markdown(
                f"""
                <div class="info-strip">
                    <strong>Request queue</strong><br>
                    {", ".join(map(str, requests))}
                    <br><br>
                    <strong>Initial direction</strong><br>
                    {direction.title()}
                    <br><br>
                    <strong>Seek time per cylinder</strong><br>
                    {seek_time:g} ms
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.subheader("Algorithm performance summary")
        show_metrics_table(metrics_df)

    else:
        st.warning("Enter a valid disk configuration to view the dashboard.")


# ============================================================
# DISK SIMULATOR
# ============================================================

elif page == "Disk Simulator":
    page_header(
        "Simulation lab",
        "Disk scheduling simulator",
        "Select an algorithm and inspect the order in which disk requests are serviced.",
    )

    if input_valid:
        selected_algorithm = st.selectbox(
            "Scheduling algorithm",
            algorithm_names,
            help="Choose one of the six implemented disk scheduling algorithms.",
        )

        result = results[selected_algorithm]
        selected_metric = metrics_df.loc[
            metrics_df["algorithm"] == selected_algorithm
        ].iloc[0]

        a, b, c = st.columns(3)
        a.metric("Selected algorithm", selected_algorithm)
        b.metric("Total head movement", f"{selected_metric['total_head_movement']} cylinders")
        c.metric("Estimated seek time", f"{selected_metric['estimated_seek_time_ms']:.2f} ms")

        st.subheader("Disk head movement path")
        st.plotly_chart(
            create_movement_chart(result, int(disk_size)),
            use_container_width=True,
            config={"displayModeBar": True, "displaylogo": False},
        )

        st.subheader("Simulation details")
        detail_left, detail_right = st.columns(2, gap="large")

        with detail_left:
            st.markdown("**Service order**")
            st.code("  →  ".join(map(str, result["service_order"])), language=None)

        with detail_right:
            st.markdown("**Movement path**")
            st.code("  →  ".join(map(str, result["movement_path"])), language=None)

        st.caption(
            "The movement chart visualises the calculated service path. "
            "The displayed seek time is an estimate based on the configured "
            "time per cylinder, not a measurement from physical disk hardware."
        )
    else:
        st.warning("Enter a valid disk configuration to run the simulator.")


# ============================================================
# PERFORMANCE ANALYSIS
# ============================================================

elif page == "Performance Analysis":
    page_header(
        "Analytics",
        "Performance analysis",
        "Compare the six algorithms using total movement, average movement and seek-time estimates.",
    )

    if input_valid:
        st.subheader("Total disk head movement")
        st.plotly_chart(
            create_performance_chart(all_metrics),
            use_container_width=True,
            config={"displayModeBar": True, "displaylogo": False},
        )

        st.subheader("Detailed performance metrics")
        show_metrics_table(metrics_df)

        st.subheader("Algorithm ranking")
        st.plotly_chart(
            create_ranking_chart(recommendation),
            use_container_width=True,
            config={"displayModeBar": True, "displaylogo": False},
        )
    else:
        st.warning("Enter a valid disk configuration to analyse performance.")


# ============================================================
# INTELLIGENT RECOMMENDATION
# ============================================================

elif page == "Intelligent Recommendation":
    page_header(
        "Decision support",
        "Intelligent algorithm recommendation",
        "The recommendation is calculated from the selected objective and the current simulation metrics.",
    )

    if input_valid:
        show_recommendation_card(recommendation)

        st.subheader("Algorithm ranking")
        ranking_df = pd.DataFrame(recommendation["rankings"])

        ranking_labels = {
            "algorithm": "Algorithm",
            "total_head_movement": "Total movement",
            "direction_changes": "Direction changes",
            "score": "Performance score",
        }
        ranking_df = ranking_df.rename(columns=ranking_labels)

        st.dataframe(
            ranking_df.style.format(
                {
                    "Performance score": "{:.2f}",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Ranking visualisation")
        st.plotly_chart(
            create_ranking_chart(recommendation),
            use_container_width=True,
            config={"displayModeBar": True, "displaylogo": False},
        )

        st.subheader("System warnings and limitations")
        if recommendation.get("warnings"):
            for warning in recommendation["warnings"]:
                st.warning(warning)
        else:
            st.success("No recommendation warnings were returned for this configuration.")

        st.info(
            "The recommendation engine is rule-based and compares simulated "
            "metrics. It is not a machine-learning model and does not measure "
            "real hardware latency or live request-arrival behaviour."
        )
    else:
        st.warning("Enter a valid disk configuration to generate a recommendation.")


# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":
    page_header(
        "Export centre",
        "Performance reports",
        "Review the current results and export a PDF report or CSV performance dataset.",
    )

    if input_valid:
        st.subheader("Report summary")
        k1, k2, k3 = st.columns(3)
        k1.metric("Algorithms analysed", len(all_metrics))
        k2.metric("Requests serviced per algorithm", len(requests))
        k3.metric("Recommended algorithm", recommendation["recommended_algorithm"])

        st.subheader("Performance preview")
        show_metrics_table(metrics_df)

        st.subheader("Recommended algorithm")
        show_recommendation_card(recommendation, compact=True)

        st.divider()

        pdf_col, csv_col = st.columns(2, gap="large")

        with pdf_col:
            st.markdown("**Complete PDF report**")
            st.caption("Includes disk configuration, performance comparison, recommendation, rankings and simulation details.")

            try:
                pdf_data = generate_pdf_report(
                    disk_size=int(disk_size),
                    head=int(head),
                    requests=requests,
                    direction=direction,
                    seek_time=seek_time,
                    metrics_list=all_metrics,
                    recommendation=recommendation,
                    results=results,
                )

                st.download_button(
                    label="Download PDF report",
                    data=pdf_data,
                    file_name="Disk_IO_Analysis_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary",
                )
                st.success("PDF report is ready.")
            except Exception as error:
                st.error(f"PDF generation failed: {error}")

        with csv_col:
            st.markdown("**Performance data (CSV)**")
            st.caption("A spreadsheet-friendly export of the six algorithm metrics.")
            st.download_button(
                label="Download performance CSV",
                data=metrics_df.to_csv(index=False),
                file_name="disk_scheduling_results.csv",
                mime="text/csv",
                use_container_width=True,
            )
    else:
        st.warning("Enter a valid disk configuration before generating reports.")


# ============================================================
# FOOTER
# ============================================================

show_footer()
