# Computer Science Project – Group 15

Supervisor: Samuel GOUTIN

Members: Clara BEAUVAIS, Houda EDDARDOURI, Sarra CHAMSI, Raphaël CARRERE

creation of the sports application SporTrack

# Overview
Strava is a popular social network used to record and share sports activities. However, many of its features are paid, and some may not fit everyone’s expectations.
This project aims to develop an improved alternative to Strava: SporTrack

Concretely, the project consists of:

-A REST API responsible for managing data and interacting with the database.

A graphical interface for displaying and interacting with the user’s activities.
# Core Features :
## F1 — Activity Management
A user must be able to:
Create an activity by uploading a GPX file,
View their activities, with the possibility to apply one or two filters,
Modify or delete any of their activities.
## F2 — News Feed
A user must access a feed displaying activities from all users they follow.
## F3 — Social Interactions
A user must be able to like and comment on activities posted by users they follow.
## F4 — Personal Statistics
A user must access statistics about their own activity, such as:

-Number of activities per week and per sport,

-Number of kilometers completed per week,

-Number of hours of activity per week.
# Optional Features :
## FO1:
Visualize statistics from F4 using bar plots, calendar heatmaps, or other visual tools.
## FO2:
Visualize the route of activities on a map.
## FO3:
A user should be able to:
-Create a route from a starting and ending address,
-Visualize this route on a map,
Download the GPS trace of the route.

## FO4:
Access performance predictions (e.g., estimated times on new distances) based on past activities.

# Run SporTrack Locally :
To run the application locally, follow the steps below.
## 1. Install the dependencies 
Before starting the application, install all required packages using:  
pip install -r requirements.txt
Make sure to run this command inside the virtual environment you are using for the project.
## 2. Start the backend (FastAPI API) 
Open a first terminal and start the backend server with:
uvicorn client.api:app --host 0.0.0.0 --port 8000 --reload
The backend will then be available at: http://localhost:8000
## 3. Start the user interface (Streamlit)
Open a second terminal and run the Streamlit application:
streamlit run app_streamlit/main.py
The user interface will automatically open in your browser at the address provided by Streamlit (usually:http://localhost:8501


