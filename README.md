#MCA Insights Engine: Comprehensive Solution

This repository contains the complete implementation of the MCA Insights Engine—an end-to-end Python data application designed to merge, track, and enrich frequently updated corporate data.

The solution fulfills all required steps for data pipeline construction (Tasks A, B, C) and the final Streamlit application layer (Tasks D, E).

##I. Solution Overview (Data Pipeline)

The project is structured as a series of Python scripts designed to turn simulated raw data into auditable, enriched insights.

Data Preparation Summary (Tasks A, B, C)

###Task A/B: Data Processing & Auditing (data_processing.py, change_detector.py)

What I Did: I created and ran scripts to merge simulated state-wise data, fix data quality issues (like duplicates and nulls), and generate three daily change logs.

Key Logic: I used advanced Pandas functions like .compare() and .difference() to track specific changes (new incorporations, capital changes) between sequential datasets (Day 1, Day 2, and Day 3).

Task C: Enrichment and Auditing (data_enricher.py)

Goal: To add context (Sector, Director Name) and satisfy the 50-100 record size requirement.

Method (The Proxy): I implemented a proxy simulation for web scraping. Instead of hitting live sites, the script randomly assigned pre-written values for Sector and Director Names.

Data Structure: The script used Pandas .melt() to transform the data into the required long auditing format (CIN, FIELD, SOURCE), explicitly 

##II. The Final App (Tasks D & E)

The final user interface is built using Streamlit (app.py), integrating all the processed data for user consumption.

Final Application Features

###Query Layer (Task D): The dashboard displays the final enriched company data.

Filters: Includes dynamic Filters by State, Status, and Year.

Search: Implements robust Search functionality by CIN or Company Name.

AI Summary (Task E1): A function performs simple Pandas calculations on the Change Log to generate summarized counts of New Incorporations and Field Updates. (This serves as the required proxy for AI Summary Generation.)

Chatbot Proxy (Task E2): Implemented with rule-based logic that translates natural language queries (e.g., "new incorporations in Maharashtra") into direct data filters on the audit log.

Setup Instructions

##Clone this repository.

###Install dependencies: pip install -r requirements.txt

###Run the application from the root directory: streamlit run app.py
