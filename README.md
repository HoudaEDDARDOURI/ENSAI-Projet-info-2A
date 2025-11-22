# Computer Science Project – Group 15

Supervisor: Samuel GOUTIN

Members: Clara BEAUVAIS, Houda EDDARDOURI, Sarra CHAMSI, Raphaël CARRERE

creation of the sports application SporTrack

# Overview
Strava is a popular social network used to record and share sports activities. However, many of its features are paid, and some may not fit everyone’s expectations.
This project aims to develop an improved alternative to Strava: SporTrack

Concretely, the project consists of:

-A REST API responsible for managing data and interacting with the database.

-A graphical interface for displaying and interacting with the user’s activities.
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

-Download the GPS trace of the route.

## FO4:
Access performance predictions (e.g., estimated times on new distances) based on past activities.

# User Guide
## 1. Clone the Project

- Clone the repository to your machine using HTTPS or SSH:
- 
```bash
git clone <REPOSITORY_URL>
```
- Move into the project directory:
```bash
cd ENSAI-Projet-info-2A
```
## 2. Install Dependencies

Before running the application, install all required packages:

```bash
pip install -r "requirements.txt"
```

## 3. Database Setup
### 3.1 Create a PostgreSQL Service

You can use:

Onyxia (recommended), or your local PostgreSQL installation

### 3.2 Connect via CloudBeaver

- Open CloudBeaver
- Create a new PostgreSQL connection
- Specify: Host, Port, Database name, Username and Password
- Click Create

### 3.3 Initialise the Database

- Select the newly created connection
- Open an SQL Editor
- In the data folder, copy the script db_init.sql into your SQL Editor
- The script creates:
    - a database named my_app
    - two schemas:
      app → production data
      test → dedicated to automated tests

## 4. Run the Application
### 4.1 Start the Backend (FastAPI)

Open a first terminal and run:
```bash
cd src
uvicorn client.api:app --host 0.0.0.0 --port 8000 --reload
```
Interactive API documentation (Swagger UI): http://localhost:8000/docs

### 4.2 Start the User Interface (Streamlit)

In a second terminal, run:
```bash
streamlit run app_streamlit/main.py
```

Streamlit will automatically open in your browser, usually at: http://localhost:8501

## 5. (Optional) Using Onyxia

If you choose to expose port 8000 (API) and port 8501 (Streamlit), Onyxia will automatically generate two public URLs that you can share.

# Using the Application

Once the interface is open, you can explore the app freely.

1. Create an Account
2. Log In
3. Create an Activity
  Two options are available:
        a) Upload a GPX file : We provide sample GPX files in the data/ folder.
        b) Enter the activity manually by specifying duration and distance.
4. Navigate the User Space
You can edit your user profile, view your feed, like and comment posts, follow and unfollow other users


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


