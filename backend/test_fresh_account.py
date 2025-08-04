#!/usr/bin/env python3
"""
Test script to verify service account creation with a fresh startup
"""

import json
import uuid
from dynamic_cloud_provisioner import DynamicCloudProvisioner

def test_fresh_service_account():
    """Test with a completely new startup to avoid existing account loading"""
    
    print("🧪 Testing Fresh Service Account Creation")
    print("=" * 50)
    
    # Initialize provisioner
    provisioner = DynamicCloudProvisioner()
    
    # Test startup info with random ID to ensure fresh creation
    random_id = uuid.uuid4().hex[:8]
    startup_info = {
        "name": f"FreshStartup{random_id}",
        "email": f"founder{random_id}@fresh.com",
        "founder_name": "Fresh Founder"
    }
    
    # Test with GCP services to trigger service account creation
    pipeline_services = ["bigquery", "looker"]
    
    print(f"📦 Testing with fresh startup: {startup_info['name']}")
    print(f"📧 Email: {startup_info['email']}")
    print(f"🔧 Services: {', '.join(pipeline_services)}")
    print()
    
    # Auto-provision everything
    try:
        result = provisioner.auto_provision_startup_infrastructure(startup_info, pipeline_services)
        
        print("✅ PROVISIONING COMPLETED!")
        print("=" * 50)
        
        # Print the account_info that the frontend will receive
        if "account_info" in result:
            account_info = result["account_info"]
            print("🎯 FRONTEND ACCOUNT INFO:")
            print(f"   Account ID: {account_info.get('account_id', 'N/A')}")
            print(f"   Account Name: {account_info.get('account_name', 'N/A')}")
            print(f"   Provider: {account_info.get('provider', 'N/A')}")
            
            if account_info.get('service_account_email'):
                print(f"   Service Account: {account_info['service_account_email']}")
                print(f"   Console URL: {account_info.get('console_url', 'N/A')}")
                print(f"   Keys URL: {account_info.get('keys_url', 'N/A')}")
                print(f"   Project ID: {account_info.get('project_id', 'N/A')}")
            else:
                print(f"   Console URL: {account_info.get('console_url', 'N/A')}")
        else:
            print("⚠️ No account_info found in result")
        
        print("\n" + "=" * 50)
        print("📋 WHAT USER WILL SEE IN FRONTEND:")
        print("=" * 50)
        
        account_info = result.get("account_info", {})
        if account_info.get("service_account_email"):
            print("✅ Infrastructure Created Successfully")
            print("🔑 Dedicated Service Account:")
            print(f"   Email: {account_info['service_account_email']}")
            print(f"   Project: {account_info.get('project_id', 'N/A')}")
            print("Links:")
            print(f"   🔗 Manage Service Account → {account_info.get('console_url', 'N/A')}")
            print(f"   🔐 Create API Keys → {account_info.get('keys_url', 'N/A')}")
        else:
            print("❌ Would show generic account info instead of service account")
            print(f"   Account ID: {account_info.get('account_id', 'N/A')}")
            print(f"   Account Name: {account_info.get('account_name', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_fresh_service_account()
    exit(0 if success else 1)