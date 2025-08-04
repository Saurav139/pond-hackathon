#!/usr/bin/env python3
"""
Script to check if BigQuery datasets were actually created
"""

import json
from pathlib import Path
from google.oauth2 import service_account
from google.cloud import bigquery

def check_bigquery_datasets():
    """Check what BigQuery datasets exist in the project"""
    
    # Load credentials
    secrets_file = Path(__file__).parent / "platforge_secrets.json"
    with open(secrets_file, 'r') as f:
        secrets = json.load(f)
    
    service_account_file = secrets["gcp"]["service_account_file"]
    project_id = secrets["gcp"]["project_id"]
    
    print(f"🔍 Checking BigQuery datasets in project: {project_id}")
    print("=" * 60)
    
    try:
        # Load service account credentials
        credentials = service_account.Credentials.from_service_account_file(service_account_file)
        
        # Create BigQuery client
        client = bigquery.Client(project=project_id, credentials=credentials)
        
        # List all datasets
        datasets = list(client.list_datasets())
        
        if not datasets:
            print("❌ No datasets found in the project")
            print("\n🔧 Possible reasons:")
            print("   1. Datasets were not actually created")
            print("   2. Service account doesn't have permission to list datasets")
            print("   3. Datasets were created in a different project")
            return False
        
        print(f"✅ Found {len(datasets)} dataset(s):")
        print()
        
        for i, dataset in enumerate(datasets, 1):
            dataset_id = dataset.dataset_id
            dataset_ref = client.get_dataset(dataset.reference)
            
            print(f"{i}. Dataset: {dataset_id}")
            print(f"   Full ID: {dataset.project}.{dataset_id}")
            print(f"   Description: {dataset_ref.description or 'No description'}")
            print(f"   Location: {dataset_ref.location}")
            print(f"   Created: {dataset_ref.created}")
            print(f"   Modified: {dataset_ref.modified}")
            
            # Generate direct links
            console_url = f"https://console.cloud.google.com/bigquery?project={project_id}&ws=!1m5!1m4!4m3!1s{project_id}!2s{dataset_id}!3e1"
            dataset_url = f"https://console.cloud.google.com/bigquery?project={project_id}&p={project_id}&d={dataset_id}&page=dataset"
            
            print(f"   🔗 Console URL: {console_url}")
            print(f"   🔗 Dataset URL: {dataset_url}")
            
            # Check tables in dataset
            tables = list(client.list_tables(dataset))
            if tables:
                print(f"   📊 Tables ({len(tables)}):")
                for table in tables:
                    print(f"      - {table.table_id}")
            else:
                print(f"   📊 Tables: None (empty dataset)")
            
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to check datasets: {e}")
        
        if "bigquery.datasets.list" in str(e):
            print("\n🔧 SOLUTION: Grant BigQuery Data Viewer role to your service account")
            print(f"   1. Visit: https://console.cloud.google.com/iam-admin/iam?project={project_id}")
            print("   2. Find your service account")
            print("   3. Add role: 'BigQuery Data Viewer' or 'BigQuery Admin'")
            print("   4. Try again")
        
        return False

if __name__ == "__main__":
    check_bigquery_datasets()