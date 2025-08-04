#!/usr/bin/env python3
"""
Script to enable required GCP APIs for service account creation
"""

import json
from pathlib import Path
from google.oauth2 import service_account
from google.cloud.service_usage_v1 import ServiceUsageClient

def enable_required_apis():
    """Enable the IAM API in the GCP project"""
    
    # Load credentials
    secrets_file = Path(__file__).parent / "platforge_secrets.json"
    with open(secrets_file, 'r') as f:
        secrets = json.load(f)
    
    service_account_file = secrets["gcp"]["service_account_file"]
    project_id = secrets["gcp"]["project_id"]
    
    print(f"🔧 Enabling APIs for project: {project_id}")
    
    try:
        # Load service account credentials
        credentials = service_account.Credentials.from_service_account_file(service_account_file)
        
        # Create Service Usage client
        client = ServiceUsageClient(credentials=credentials)
        
        # APIs to enable
        apis_to_enable = [
            "iam.googleapis.com",                    # IAM API for service account creation
            "cloudresourcemanager.googleapis.com",  # Resource Manager API for project access
            "serviceusage.googleapis.com"           # Service Usage API (should already be enabled)
        ]
        
        for api in apis_to_enable:
            try:
                print(f"🔨 Enabling {api}...")
                
                # Check if already enabled
                service_name = f"projects/{project_id}/services/{api}"
                
                try:
                    service = client.get_service(name=service_name)
                    if hasattr(service, 'state') and str(service.state) == 'ENABLED':
                        print(f"   ✅ Already enabled: {api}")
                        continue
                except Exception:
                    # Service doesn't exist or not accessible, try to enable it
                    pass
                
                # Enable the service
                operation = client.enable_service(name=service_name)
                
                print(f"   ⏳ Enabling {api}... (this may take a few minutes)")
                result = operation.result(timeout=300)  # 5 minute timeout
                
                print(f"   ✅ Successfully enabled: {api}")
                
            except Exception as e:
                print(f"   ⚠️ Failed to enable {api}: {e}")
                
                if "SERVICE_DISABLED" in str(e) or "has not been used" in str(e):
                    # Extract the activation URL from the error
                    error_str = str(e)
                    if "https://console.developers.google.com" in error_str:
                        start = error_str.find("https://console.developers.google.com")
                        end = error_str.find(" ", start)
                        if end == -1:
                            end = len(error_str)
                        url = error_str[start:end]
                        print(f"   🔗 Manual activation required: {url}")
        
        print("\n🎉 API enablement process completed!")
        print("📝 If any APIs failed to enable automatically, use the provided URLs to enable them manually.")
        
    except Exception as e:
        print(f"❌ Failed to enable APIs: {e}")
        
        # Provide manual URLs
        project_number = "759955412071"  # From the error message
        print("\n🔗 Manual API Enablement URLs:")
        print(f"   IAM API: https://console.developers.google.com/apis/api/iam.googleapis.com/overview?project={project_number}")
        print(f"   Resource Manager: https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project={project_number}")
        
        return False
    
    return True

if __name__ == "__main__":
    success = enable_required_apis()
    if success:
        print("\n✅ You can now test service account creation again!")