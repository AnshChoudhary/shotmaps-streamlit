# Shotmaps Streamlit Web App

This repository contains a simple Python application for displaying shotmaps of matches played till 2020 built with Streamlit. The data is extracted from Statsbomb data available online. Streamlit is an open-source Python library that makes it easy to create web applications for data science and machine learning.

## Prerequisites

Before running the application, make sure you have the following installed:

- Python (version 3.x recommended)
- Pip (Python package installer)

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/AnshChoudhary/shotmaps-streamlit.git
    ```

2. Navigate to the project directory:

    ```bash
    cd shotmaps-streamlit
    ```

3. Download the Statsbomb data from this repository https://github.com/statsbomb/open-data and put in inside the project folder.

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To run the Streamlit app, use the following command:

```bash
streamlit run footstream.py
