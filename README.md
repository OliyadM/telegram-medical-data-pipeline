Telegram Medical Data Pipeline
An end-to-end ELT pipeline that extracts raw Telegram data from Ethiopian medical-related channels, transforms it using dbt, and prepares it for analytical access via a FastAPI-powered API.

🚧 This repository is under active development as part of a data engineering challenge.
✅ Tasks 0–2 (project setup, scraping, and transformation) are targeted for interim submission.

📌 Project Goals
This project aims to build a robust data product that:

Scrapes messages and media (images) from public Telegram channels related to Ethiopian medical businesses.

Stores raw messages and images in a partitioned data lake organized by date and channel for incremental processing.

Loads the raw data into PostgreSQL and applies dbt transformations to clean, validate, and model the data into dimensional tables (star schema).

Enriches the dataset with object detection metadata on images using YOLOv8.

Serves processed insights through a FastAPI-powered analytical API to answer business questions such as product trends, pricing, and channel activity.

🗂️ Project Structure (so far)

telegram-medical-data-pipeline/
├── data/
│   └── raw/
│       ├── telegram_messages/     # JSON message files partitioned by date & channel
│       └── telegram_images/       # downloaded images organized by date & channel
├── scraping/
│   └── scrape_telegram.py         # Script to scrape Telegram data using Telethon
├── channels.txt                   # List of Telegram channels URLs to scrape
├── .env                           # Environment variables (API keys, DB creds) - NOT committed
├── .gitignore                     # Excludes sensitive and large files like .env and data/
├── requirements.txt               # Python dependencies for scraping & processing
├── docker-compose.yml             # Docker setup for PostgreSQL and app containers
├── Dockerfile                     # Defines scraping environment for reproducibility
├── dbt_project/
│   ├── models/                    # dbt SQL models for staging, marts, and facts
│   ├── schema.yml                 # dbt schema tests and documentation
│   └── dbt_project.yml            # dbt configuration file
└── README.md                      # This file
🚀 Getting Started
Prerequisites
Docker & Docker Compose installed

Python 3.8+

Telegram API credentials (API_ID, API_HASH)

Setup
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/telegram-medical-data-pipeline.git
cd telegram-medical-data-pipeline
Create and fill .env file with:

env
Copy
Edit
API_ID=your_api_id
API_HASH=your_api_hash
SESSION_NAME=your_session_name
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=telegram_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
Start Docker containers:

bash
Copy
Edit
docker-compose up -d
Install Python dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the scraper to collect data:

bash
Copy
Edit
python scraping/scrape_telegram.py
Load JSON data into PostgreSQL with the loader script.

Run dbt transformations:

bash
Copy
Edit
dbt run
dbt test
📊 Sample Data Example
Raw Telegram message JSON stored in:

data/raw/telegram_messages/2025-07-11/lobelia4cosmetics.json

json
Copy
Edit
{
  "id": 18525,
  "text": "**CHIA **SEEDS **\nPrice 3500 birr\nTelegram @Lobeliacosmetics\n...",
  "date": "2025-07-11 07:12:05+00:00",
  "has_photo": true,
  "sender_id": -1001666492664
}
