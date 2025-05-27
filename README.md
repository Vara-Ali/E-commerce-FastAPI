# E-commerce Admin API

## Overview
A comprehensive RESTful API for managing e-commerce operations including products, sales, and inventory for Amazon & Walmart platforms.

## Technology Stack
- **Programming Language**: Python 3.12.2
- **Framework**: FastAPI
- **API Type**: RESTful API
- **Database**: Postgres
- **ORM**: SQLAlchemy

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Vara-Ali/E-commerce-FastAPI.git
   cd E-commerce-FastAPI



2. **Create virtual environment**
bashpython -m venv venv

3. **Activate virtual environment**

Windows:
bashvenv\Scripts\activate

macOS/Linux:
bashsource venv/bin/activate



4. **Install dependencies**
bashpip install -r requirements.txt

5. **Set up database**
bash# Database will be created automatically on first run
python main.py

6. **Run the application**
bashuvicorn main:app --reload

7. **Access the API**

API Base URL: http://localhost:8000
