# Intelligent-Disk-IO-Analyser
An interactive disk scheduling simulator and performance analyser built with Python and Streamlit. The project implements six disk I/O scheduling algorithms, compares their performance using different metrics, visualises disk head movement, and provides rule-based recommendations.

Overview

Disk scheduling is an important operating system function that determines the order in which pending disk I/O requests are serviced. Different scheduling algorithms can produce different disk head movements and performance outcomes.

The Intelligent Disk I/O Scheduling Analyser provides an interactive environment to simulate, analyse, and compare commonly used disk scheduling algorithms.

Users can enter disk parameters, execute algorithms, inspect their service sequences, compare performance metrics, and identify a suitable algorithm based on selected optimisation objectives.

Features

Six disk scheduling algorithms implemented and compared.

Interactive disk simulation to visualise disk head movement.

Performance analysis using total and average head movement, direction changes, and estimated seek time.

Interactive charts for comparing algorithm performance.

Rule-based intelligent recommendation to identify suitable algorithms based on performance objectives.

Report generation to export analysis results.

Streamlit interface for interactive experimentation.

Algorithms Implemented

Algorithm

Full Name

Description

FCFS

First Come First Serve

Services requests in their arrival order.

SSTF

Shortest Seek Time First

Selects the request closest to the current head position.

SCAN

Elevator Algorithm

Moves in one direction, servicing requests, then reverses direction.

C-SCAN

Circular SCAN

Services requests in one direction and returns to the opposite end before continuing.

LOOK

LOOK Scheduling

Similar to SCAN, but reverses at the last pending request instead of the disk boundary.

C-LOOK

Circular LOOK

Similar to C-SCAN, but jumps between the last and first pending requests.

Technology Stack

Technology

Purpose

Python

Core programming language and algorithm implementation

Streamlit

Interactive web application

Pandas

Data handling and tabular performance analysis

NumPy

Numerical operations

Plotly

Interactive charts and visualisations

PDF generation library

Exporting analysis reports

Performance Metrics

The application evaluates algorithms using the following metrics:

1. Total Head Movement

Measures the total distance travelled by the disk head.

[
THM = \sum_{i=1}^{n}|H_i-H_{i-1}|
]

Where:

(H_i) represents the current head position.

(H_{i-1}) represents the previous head position.

2. Average Head Movement

[
AHM = \frac{Total\ Head\ Movement}{Number\ of\ Requests}
]

3. Estimated Seek Time

[
Estimated\ Seek\ Time = THM \times Seek\ Time\ Per\ Cylinder
]

This is a simplified estimate based on a configurable seek time per cylinder. It is not a measurement of actual disk hardware latency.

4. Direction Changes

Counts changes in the direction of disk head movement according to the application's metric implementation.

Intelligent Recommendation

The project includes a rule-based recommendation component that evaluates algorithm performance and ranks algorithms according to selected objectives.

The recommendation system supports:

Minimum Head Movement: Prioritises the algorithm with the lowest total head movement.

Balanced Performance: Uses a weighted scoring approach to compare performance metrics.

The recommendation system is rule-based. It does not use a trained machine learning model.

Example Simulation

The following configuration can be used to test the algorithms:

Parameter

Value

Disk cylinder range

0–199

Initial head position

53

Request queue

98, 183, 37, 122, 14, 124, 65, 67

Seek time per cylinder

0.1 ms

Initial direction

Right

Example Results

Algorithm

Total Head Movement

Average Movement

Estimated Seek Time

FCFS

640

80.00

64.0 ms

SSTF

236

29.50

23.6 ms

SCAN

331

41.38

33.1 ms

C-SCAN

382

47.75

38.2 ms

LOOK

299

37.38

29.9 ms

C-LOOK

322

40.25

32.2 ms

For this particular request queue, SSTF produces the lowest total head movement. This does not mean SSTF is always the best algorithm; its behaviour depends on the request distribution, and it can cause starvation under certain workloads.

Application Modules

The application is organised around the following functional modules:

Dashboard – Provides an overview of the application.

Disk Simulator – Accepts disk parameters and simulates scheduling algorithms.

Performance Analysis – Compares algorithm results using metrics and charts.

Intelligent Recommendation – Ranks algorithms according to selected objectives.

Reports – Generates reports containing simulation and analysis results.

Project Structure

The project is organised into separate modules for algorithms, core logic, visualisation, and report generation.

Intelligent_Disk_IO_Analyser/
│
├── app.py
├── requirements.txt
│
├── algorithms/
│   └── disk_algorithms.py
│
├── core/
│   ├── metrics.py
│   └── recommender.py
│
├── visualisation/
│   └── charts.py
│
├── reports/
│   └── pdf_report.py
│
└── tests/
    ├── test_algorithms.py
    ├── test_metrics.py
    └── test_recommender.py

The structure above represents the main application modules; update the tree if your final repository contains additional files or different filenames.

Installation and Setup

Prerequisites

Python 3.9 or later

pip package manager

Git

1. Clone the Repository

git clone https://github.com/YOUR-USERNAME/Intelligent-Disk-IO-Scheduling-Analyser.git

2. Navigate to the Project Directory

cd Intelligent-Disk-IO-Scheduling-Analyser

3. Create a Virtual Environment

Windows:

python -m venv .venv
.venv\Scripts\activate

Linux / macOS:

python3 -m venv .venv
source .venv/bin/activate

4. Install Dependencies

pip install -r requirements.txt

5. Run the Application

streamlit run app.py

The application will open in your default browser. If it does not, open the local URL displayed in your terminal, usually:

http://localhost:8501

Running Tests

Run the test suite using:

python -m unittest discover -s tests -v

The tests cover the disk scheduling algorithms, performance metric calculations, and recommendation logic.

Limitations

Uses a static request queue rather than dynamically arriving disk requests.

Estimated seek time is based on a simplified linear model.

Does not simulate rotational latency or data transfer time.

Does not measure actual physical disk performance.

SSTF may cause starvation when new nearby requests repeatedly arrive.

Recommendation results depend on the selected scoring criteria and weights.

Future Enhancements

Support for dynamic disk request arrivals.

Waiting-time and fairness analysis.

More realistic disk latency modelling.

Additional disk scheduling algorithms.

Customisable recommendation weights.

Integration with real operating system disk monitoring.

More detailed performance reports.

Academic Project

Project: Intelligent Disk I/O Scheduling Analyser
Course: MCA – First Semester
Submitted by: Pawan Gusai
Roll Number: 26MCAP101N020
Submitted to: Dr. Neerja Negi
