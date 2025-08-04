#!/usr/bin/env python3
"""
Test script to verify service account creation and console links
"""

import json
from dynamic_cloud_provisioner import DynamicCloudProvisioner

def test_service_account_creation():
    """Test the complete service account creation flow"""
    
    print("🧪 Testing Service Account Creation")
    print("=" * 50)
    
    # Initialize provisioner
    provisioner = DynamicCloudProvisioner()
    
    # Test startup info
    startup_info = {
        "name": "TestServiceAccount",
        "email": "test@serviceaccount.com",
        "founder_name": "Test Founder"
    }
    
    # Test with GCP services to trigger service account creation
    pipeline_services = ["bigquery", "looker"]
    
    print(f"📦 Testing with services: {', '.join(pipeline_services)}")
    print()
    
    # Auto-provision everything
    try:
        result = provisioner.auto_provision_startup_infrastructure(startup_info, pipeline_services)
        
        print("✅ PROVISIONING COMPLETED!")
        print("=" * 50)
        
        # Check GCP environment
        if "gcp" in result.get("provisioned_environments", {}):
            gcp_env = result["provisioned_environments"]["gcp"]
            print(f"🔧 GCP Project: {gcp_env['project_id']}")
            print(f"🔑 Service Account: {gcp_env.get('service_account', 'N/A')}")
            
            # Check service account credentials
            if "credentials" in gcp_env:
                creds = gcp_env["credentials"]
                print(f"📧 Service Account Email: {creds.get('email', 'N/A')}")
                print(f"🔗 Console URL: {creds.get('console_url', 'N/A')}")
                print(f"🔐 Keys URL: {creds.get('keys_url', 'N/A')}")
                print(f"⚡ Status: {creds.get('status', 'N/A')}")
                
                # Check instructions
                if "instructions" in creds:
                    print("📝 Instructions:")
                    for i, instruction in enumerate(creds["instructions"], 1):
                        print(f"   {i}. {instruction}")
            else:
                print("⚠️ No service account credentials found")
        else:
            print("⚠️ No GCP environment found in result")
        
        print("\n" + "=" * 50)
        print("🎯 FRONTEND INTEGRATION TEST")
        print("=" * 50)
        
        # Test what the frontend would receive
        print("📱 Frontend would receive:")
        frontend_data = {
            "status": result["status"],
            "account_info": result.get("account_info"),
            "provisioned_environments": result.get("provisioned_environments"),
            "provisioned_resources": result.get("provisioned_resources")
        }
        
        print(json.dumps(frontend_data, indent=2))
        
        # Verify service account links are accessible
        if "gcp" in result.get("provisioned_environments", {}):
            gcp_env = result["provisioned_environments"]["gcp"]
            if "credentials" in gcp_env:
                creds = gcp_env["credentials"]
                console_url = creds.get("console_url")
                keys_url = creds.get("keys_url")
                
                print(f"\n🔗 Service Account Management:")
                print(f"   Console URL: {console_url}")
                print(f"   Keys URL: {keys_url}")
                
                if console_url and keys_url:
                    print("✅ Frontend should display both service account links")
                else:
                    print("⚠️ Missing service account URLs for frontend")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_service_account_creation()
    exit(0 if success else 1)