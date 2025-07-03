# Activity Finder

Backend to finally find what to do.

![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-21201E?logo=creativecommons&logoColor=white)
![Python 3.12](https://img.shields.io/badge/python-3.12-192841?logo=python&logoColor=white)
![Django 5.1](https://img.shields.io/badge/django-5.1-092E20?logo=django&logoColor=white)

## Overview

A platform to **explore** and **book exciting activities**—whether it’s a relaxing appointment with a **nail master** or a seat at a **symphony concert**. Easily find what’s happening **around you** or in **any location** you choose.
For **event organizers**, it’s a powerful tool to **promote your events** alongside **social media**, while providing everything your visitors need—**schedules**, **venue layouts**, and **guided routes** to even the most **tucked-away spots**.

## Getting Started

Follow the steps below to set up and run the project.

### Prerequisites


Install `Docker Desktop` from [official website](https://www.docker.com/).
`docker cli` will be installed by default.

### Setup

1. **Clone the repository**

   Pull the project to your local machine:

   ```sh
   git clone https://github.com/iamkorniichuk/activity-finder.git
   cd activity-finder
   ```

2. **Set up environment**

   Create a `.env` file in the root directory and populate it with variables like showed in [example](.env.example).

3. **Run the project**

   Build the containers and start the application:

   ```sh
   docker compose up --build
   ```

   > :warning: Make sure you have running Docker instance.

   Local API's schema will be at http://127.0.0.1:8000/schema/redoc/
