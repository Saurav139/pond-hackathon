# PlatForge.ai Backend

AI-powered cloud infrastructure provisioning backend.

## Features

- 🚀 **Dynamic Cloud Provisioning**: Automatically creates AWS/GCP accounts and resources
- 🤖 **AI Recommendations**: Smart infrastructure recommendations based on use cases
- 💾 **Account Persistence**: Saves and loads existing startup accounts
- 🔧 **Service Configuration**: Individual service setup with connection details
- 📊 **Infrastructure Catalog**: 25+ supported cloud services

## Quick Start

1. **Install Dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure Secrets**:
   Create `platforge_secrets.json` with your AWS/GCP credentials:
   ```json
   {
     "aws": {
       "access_key_id": "YOUR_ACCESS_KEY",
       "secret_access_key": "YOUR_SECRET_KEY",
       "organization_id": "o-xxxxxxxxxx",
       "region": "us-east-1"
     },
     "gcp": {
       "service_account_file": "path/to/service-account.json",
       "organization_id": "123456789012",
       "billing_account_id": "XXXXXX-XXXXXX-XXXXXX"
     }
   }
   ```

3. **Run the API**:
   ```bash
   python app.py
   ```

   Server starts on `http://localhost:8001`

## API Endpoints

- `POST /recommendations` - Get infrastructure recommendations
- `POST /auto-provision` - Auto-provision startup infrastructure
- `POST /setup` - Install packages for infrastructure
- `POST /verify` - Verify installations
- `POST /configure` - Generate configuration files

## Core Components

- **`app.py`** - FastAPI web server
- **`dynamic_cloud_provisioner.py`** - Main provisioning engine
- **`infrastructure_catalog.py`** - Service catalog and recommendations
- **`platforge_accounts.json`** - Account persistence database

## Supported Services

### AWS Services
- RDS (PostgreSQL/MySQL)
- Redshift (Data Warehouse)
- EC2 (Compute)
- S3 (Storage)
- DynamoDB (NoSQL)
- AWS Glue (ETL)

### GCP Services
- BigQuery (Data Warehouse)
- Cloud SQL (Database)
- Compute Engine (Compute)
- Cloud Storage (Storage)
- Firestore (NoSQL)
- Dataflow (ETL)

### Third-Party Services
- MongoDB Atlas
- Snowflake
- Tableau
- Power BI

## Architecture

```
Backend/
├── app.py                          # FastAPI server
├── dynamic_cloud_provisioner.py    # Core provisioning logic
├── infrastructure_catalog.py       # Service recommendations
├── platforge_secrets.json         # Credentials (not in git)
├── platforge_accounts.json        # Account persistence
└── requirements.txt               # Python dependencies
```