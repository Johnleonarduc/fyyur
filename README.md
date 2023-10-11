# Fyyur - A Musical Venue and Artist Booking Platform

## Introduction

Fyyur is a musical venue and artist booking site designed to facilitate the discovery and booking of shows between local performing artists and venues. This platform allows users to list new artists and venues, discover them, and create shows with artists as venue owners. In this project, we have established the data models to power the API endpoints for Fyyur by connecting to a PostgreSQL database for storing, querying, and managing information about artists and venues on the platform.

To view platform click here: https://fyyur-wrmd.onrender.com/
## Overview

Fyyur is a fully functioning site capable of the following using a PostgreSQL database:

- Creating new venues, artists, and shows.
- Searching for venues and artists.
- Learning more about a specific artist or venue.

Fyyur aims to be the next platform that artists and musical venues can use to find each other, discover new music shows, and make that connection happen.

## Tech Stack (Dependencies)

### 1. Backend Dependencies
- **virtualenv**: A tool to create isolated Python environments.
- **SQLAlchemy ORM**: Our ORM library of choice.
- **PostgreSQL**: Our database of choice.
- **Python3** and **Flask**: Our server language and server framework.
- **Flask-Migrate**: Used for creating and running schema migrations.

### 2. Frontend Dependencies
- **HTML**.
- **CSS**
- **Javascript** 
- **Bootstrap** 
## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py
  ├── config.py
  ├── error.log
  ├── forms.py
  ├── requirements.txt
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```
## Development Setup
1. **Download the project starter code locally**
```
git clone https://github.com/Johnleonarduc/fyyur.git
cd fyyur
```

2. **Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

3. **Install the dependencies:**
```
pip install -r requirements.txt
```

4. **Create Database Locally**
- Ensure you have PostgreSQL installed or download it online
- use PgAdmin or Command prompt to create your local database, name it e.g. fyyur
- Set your environment variables or update the config file to reflect your database configurations

5. **Run Migrations:**
Since the migrations have already been created, running the upgrade command, creates the necessary feilds in the database
```
flask upgrade
```

6. **Run the development server:**
```
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
python3 app.py
```

or

```
flask run
```

6. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

