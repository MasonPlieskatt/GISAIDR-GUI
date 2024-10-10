
# GISAIDR Interfacer GUI

## Overview

This application provides a graphical interface using **CustomTkinter** that allows users to interact programmatically with the GISAID database via the **GISAIDR** package. The GUI facilitates querying total viral counts for specific amino acid substitutions over a user-defined time period and geographical locations. It features login functionality, real-time file monitoring, data input, and an option to run R scripts for further analysis.

### Key Features:
- User-friendly GUI built with **CustomTkinter**.
- Retrieves viral data from the **GISAID** database using **GISAIDR**.
- Monitors file changes and updates data dynamically.
- Saves and appends data to a long-term storage CSV file.
- Allows users to compare total viral counts across entries.
- Includes login management with stored credentials.

---

## Prerequisites

To run this project, ensure you have the following software installed:

- **Python 3.x**
- **R**
- **CustomTkinter** for the GUI.
- **Watchdog** for monitoring file changes.
- **GISAIDR** package from GitHub for interacting with the GISAID database.

### Required Python Libraries:
- `customtkinter`
- `tkinter`
- `watchdog`

Install the necessary Python dependencies via pip:
```bash
pip3 install customtkinter watchdog
```


### Required R Libraries:
- `devtools` to install the **GISAIDR** package from GitHub.

### GISAIDR Package Installation:

The **GISAIDR** package must be installed from GitHub. The application will automatically prompt users to install it if it's not detected. You can also install it manually in your R environment by running:

```r
# Install devtools if not already installed
if (!requireNamespace("devtools", quietly = TRUE)) {
  install.packages("devtools")
}

# Install GISAIDR from GitHub
devtools::install_github("Wytamma/GISAIDR")
```

---

## Usage Instructions
### 0. Running the Code:
- To start the application, input the following line into terminal, shell, or cmd opened at the installation path. Additionally, you can build the "GISAIDR_GUI" file yourself.
```bash
python3 GISAIDR_GUI.py
```

### 1. Login Window:
- When you start the application, a login window will appear.
- Enter your **GISAID** credentials and choose the appropriate database (EpiCoV, EpiPox, or EpiRSV).
- The login information will be saved in the `credentials.txt` file for future sessions.

### 2. Main GUI:
Once logged in, the main interface provides the following features:

#### Input Fields:
- **Data Nickname**: A custom name for your data set.
- **Start Date / End Date**: The period over which you want to retrieve data (in `YYYY-MM-DD` format).
- **Geographical Locations**: The location(s) you want to query.
- **Amino Acids Substitutions**: The amino acid substitutions you are interested in.

#### Switches:
- **Run Data Query**: Once all fields are filled in, toggle the switch to run the GISAID query, which will:
  - Write the input data to a file.
  - Execute an R script that queries the GISAID database.
  - Append the retrieved data (including total viral counts) to the `longterm_storage.csv` file.

#### Table Display:
- Displays previously retrieved data, including:
  - Data Nickname
  - Start Date, End Date
  - Location
  - Amino Acid Substitutions
  - Total Viral Count
- The table is dynamically updated based on the data in `longterm_storage.csv`.

#### Comparison Mode:
- Use the "Toggle Comparison" checkbox to compare viral counts across entries. The background color will change based on the comparison results.

#### Data Wipe Option:
- Type "DELETE ALL DATA" into the provided text box to clear the contents of the `longterm_storage.csv` file.

---

## File Structure

- `credentials.txt`: Stores the GISAID login credentials (username, password, and database).
- `input_data.txt`: Stores the query input data (data nickname, start date, end date, locations, and amino acid substitutions).
- `longterm_storage.csv`: Keeps a record of all the past queries and their respective viral counts.
- `GISAID_search_summary.csv`: Temporary file to store the results of the most recent GISAID query.

---

## Acknowledgments

- The **GISAIDR** package by Wytamma Wirth & Sebastian Duchene for programmatic access to GISAID data. (https://github.com/Wytamma/GISAIDR)
- **CustomTkinter** for providing a modern, customizable Tkinter interface.

---

