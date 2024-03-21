# Flask App

This is a simple Flask application that extracts data from PDF files and stores it in a SQLite database. It provides an API endpoint for uploading PDF files and extracting tabular data.

## Features

- Extracts tabular data from PDF files
- Stores data in a SQLite database
- Provides API endpoints for uploading PDF files and accessing data

## Installation

### Non-Docker Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   ```

2. Activate environment

   '''

   - for linux Ubantu

    ```sh
    source env/bin/activate
      ```
   - for windows

   ```sh
    env/Scripts/activate
    ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install jdk:
   '''
   For Linux
   https://download.oracle.com/java/22/latest/jdk-22_linux-x64_bin.deb

   After Installation this file than Add path in system environment variable

   '''

5. Run the Flask app:

   ```bash
   python app.py
   ```

6. The app should now be running on http://localhost:5000.


7. Run the apiclient.py


# Running Your Application with Docker

This guide provides instructions for running your application using Docker containers.


## Getting Started

5. Running the Docker Container:

   ```bash
   docker-compose up -d --build

   ```

This README file provides detailed instructions for cloning the project, running the Docker containers, accessing the container's shell, running the Python script inside the container, and stopping and removing the containers. It also includes further options for customization.





