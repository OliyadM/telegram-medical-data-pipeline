# Telegram Medical Data Pipeline

An end-to-end ELT pipeline that extracts raw Telegram data from Ethiopian medical-related channels, transforms it using dbt, and prepares it for analytical access via a FastAPI-powered API.

> 🚧 This repository is under active development as part of a data engineering challenge.  
> ✅ Tasks 0–2 (project setup, scraping, and transformation) are targeted for interim submission.

---

## 📌 Project Goals

Build a complete data product that:
- Scrapes messages and media from Telegram channels
- Stores raw messages and images in a partitioned data lake
- Loads and transforms the data using PostgreSQL and dbt
- Enriches image data using object detection (YOLOv8)
- Serves insights via an analytical API

---

## 🗂️ Project Structure (so far)

```bash
telegram-medical-data-pipeline/
├── data/
│   └── raw/
│       ├── telegram_messages/     # JSON messages by day & channel
│       └── telegram_images/       # downloaded images
├── scraping/
│   └── scrape_telegram.py         # (coming in Task 1)
├── channels.txt                   # list of Telegram channels to scrape
├── .env                           # (NOT committed) holds secrets
├── .gitignore                     # excludes .env, data/, etc.
├── requirements.txt               # Python deps
├── docker-compose.yml             # PostgreSQL & app containers
├── Dockerfile                     # for reproducible scraping env
└── README.md
