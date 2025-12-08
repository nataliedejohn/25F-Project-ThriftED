# Fall 2025 CS 3200 Project ThriftED
- A student-verified campus marketplace for safer, sustainable buying and seller.

# Overview
ThriftED is a campus-focused resale platform designed for Northeastern students to buy and sell textbooks, furniture, electronics, clothing, and other everyday student essentials. Compared to popular platforms like Craigslist or Facebook, ThriftED restricts all the listings, messaging, and pickup locations to verified students on campus to create a safer, more efficient, and data-driven marketplace of users.

# This project implements the full ThriftED system using:
- Streamlit (front-end)
- Flask (REST API)
- MySQL (relational database and schema)
- Docker Compose (local deployment)

The application includes role-based experiences for Buyers, Sellers, Moderators, and Data Analysts, each with their own unique features, stories and data workflows.

# Features
Buyer
- Filter items by price, category, and location
- View product recommendations based on search + purchase history
- Message sellers in-app
- Choose campus pickup locations
- See verified-student badges

# Seller
- Create and manage listings
- Mark items as active, sold, on hold, etc.
- Get price guidance from historical data
- View analytics: listing views, saves, performance
- Message buyers without sharing personal info

# Moderator
- Approve, move, or remove listings
- Restrict or ban users
- Verify high-value items
- Manage user disputes and messaging reports
- Edit global guidelines

# Data Analyst
- Dashboard for trends: popular items, price ranges, listing velocity
- Satisfaction & feedback analysis
- Personalized recommendations powered by search/view data
- Detect outliers and abnormal listing behavior

# Installing

# Executing program

# Team
Team Name: SQL Squad
- Project Name: ThriftED
- Members: Lindsay Cheung, Natalie DeJohn, Cozette Kinney, Alex Yang, Ryan Yim

## Prerequisites

- A GitHub Account
- A terminal-based git client or GUI Git client such as GitHub Desktop or the Git plugin for VSCode.
- A distribution of Python running on your laptop. The distribution supported by the course is [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install).
  - Create a new Python 3.11 environment in `conda` named `db-proj` by running:  
     ```bash
     conda create -n db-proj python=3.11
     ```
  - Install the Python dependencies listed in `api/requirements.txt` and `app/src/requirements.txt` into your local Python environment. You can do this by running `pip install -r requirements.txt` in each respective directory.
     ```bash
     cd api
     pip install -r requirements.txt
     cd ../app
     pip install -r requirements.txt
     ```
     Note that the `..` means go to the parent folder of the folder you're currently in (which is `api/` after the first command)
- VSCode with the Python Plugin installed
  - You may use some other Python/code editor.  However, Course staff will only support VS Code.
- Docker Desktop


## Structure of the Repo

- This repository is organized into five main directories:
  - `./app` - the Streamlit app
  - `./api` - the Flask REST API
  - `./database-files` - SQL scripts to initialize the MySQL database
- The repo also contains a `docker-compose.yaml` file that is used to set up the Docker containers for the front end app, the REST API, and MySQL database. 
