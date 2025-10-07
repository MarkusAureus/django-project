News Digest Application

This is a small Django application designed to pull articles from various RSS feeds, manage them, and create curated digests. It uses Celery for periodic tasks and is containerized with Docker for easy setup and deployment.
Technicals

    Backend: Python, Django

    Database: PostgreSQL

    Async Tasks: Celery, Redis

    Containerization: Docker, Docker Compose

    RSS Parsing: feedparser

Project Structure

    my_project/: The main Django project directory containing settings.

    news/: The Django app handling all core logic (models, admin, tasks).

    Dockerfile: Defines the image for the Django application.

    docker-compose.yml: Defines and orchestrates all services (web, db, redis, celery).

    entrypoint.sh: A helper script to wait for the database to be ready before starting the application.

    requirements.txt: A list of Python dependencies.

How to Run

Prerequisites: You must have Docker and Docker Compose installed on your system.

    Extract the Archive
    Unzip the provided project archive into a directory on your machine.

    Build and Run the Services
    Navigate to the root directory of the project (where the docker-compose.yml file is located) in your terminal and run the following command:

    docker-compose up --build

    This command will build the Docker images and start all the necessary containers (web server, database, Redis, and Celery services). Leave this terminal running to see the application logs.

    Create a Superuser
    Open a new terminal window, navigate to the same project directory, and run this command to create an administrator account:

    docker-compose exec web python manage.py createsuperuser

    Follow the prompts to set up your username, email, and password.

How to Use

    Access the Admin Panel
    Open your web browser and go to http://localhost:8000/admin. Log in using the superuser credentials you just created.

    Add a News Source

        Navigate to the "News sources" section under "NEWS".

        Click "Add news source".

        Fill in the details (e.g., Name: Tech News, Rss url: http://feeds.arstechnica.com/arstechnica/index).

        Make sure to check the "Active" box.

        Save the source.

    Fetch Articles
    Articles are fetched automatically every 30 minutes. To trigger a fetch manually for testing, run the following command in your second terminal:

    docker-compose exec celery_worker celery -A my_project call news.tasks.fetch_rss_feeds

    After the command completes, you can view the pulled articles in the "Articles" section of the admin panel.

    Create a Digest

        Navigate to the "Digests" section.

        Click "Add digest".

        Give the digest a name.

        In the "Digest Articles" inline section at the bottom, click "Add another Digest Article" to add articles to your digest.

        Save the digest.
