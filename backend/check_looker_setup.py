#!/usr/bin/env python3
"""
Show the Looker configuration and setup instructions
"""

from dynamic_cloud_provisioner import DynamicCloudProvisioner
import json

def show_looker_setup():
    """Show the latest Looker configuration"""
    
    print("🔍 Latest Looker Configuration")
    print("=" * 60)
    
    # Initialize provisioner to get the latest account
    provisioner = DynamicCloudProvisioner()
    
    # Get existing accounts
    accounts = provisioner.list_existing_accounts()
    
    if not accounts:
        print("❌ No accounts found")
        return
    
    # Find the most recent account with Looker
    latest_account = None
    for account in reversed(accounts):  # Most recent first
        if "provisioned_resources" in account:
            for resource in account["provisioned_resources"]:
                if resource.get("service") == "Looker":
                    latest_account = account
                    break
        if latest_account:
            break
    
    if not latest_account:
        print("❌ No accounts with Looker found")
        return
    
    # Find the Looker resource
    looker_resource = None
    bigquery_resource = None
    
    for resource in latest_account["provisioned_resources"]:
        if resource.get("service") == "Looker":
            looker_resource = resource
        elif resource.get("service") == "BigQuery":
            bigquery_resource = resource
    
    if not looker_resource:
        print("❌ No Looker resource found")
        return
    
    print(f"📊 Looker Instance: {looker_resource['name']}")
    print(f"🏢 Startup: {latest_account['startup_name']}")
    print(f"📧 Service Account: {latest_account.get('provisioned_environments', {}).get('gcp', {}).get('service_account', 'N/A')}")
    print()
    
    # Show BigQuery connection
    if bigquery_resource:
        print("🔗 Connected BigQuery Dataset:")
        print(f"   Dataset: {bigquery_resource['dataset_id']}")
        print(f"   Project: {bigquery_resource['project_id']}")
        print(f"   Console: {bigquery_resource['console_url']}")
        print()
    
    # Show Looker setup instructions
    if "setup_instructions" in looker_resource:
        print("📋 Setup Instructions:")
        for i, instruction in enumerate(looker_resource["setup_instructions"], 1):
            print(f"   {instruction}")
        print()
    
    # Show console URL
    print(f"🔗 Looker Console: {looker_resource['console_url']}")
    print()
    
    # Show sample LookML
    if "sample_lookml" in looker_resource and looker_resource["sample_lookml"].strip():
        print("📝 Sample LookML Configuration:")
        print("```lookml")
        print(looker_resource["sample_lookml"].strip())
        print("```")
        print()
    
    # Show Python SDK setup
    if "python_sdk_setup" in looker_resource:
        print("🐍 Python SDK Setup:")
        print("```python")
        print(looker_resource["python_sdk_setup"].strip())
        print("```")
        print()
    
    # Show connection details
    if "bigquery_connection" in looker_resource and looker_resource["bigquery_connection"]:
        print("🔌 BigQuery Connection Details:")
        conn = looker_resource["bigquery_connection"]
        print(f"   Project: {conn.get('project_id', 'N/A')}")
        print(f"   Dataset: {conn.get('dataset', 'N/A')}")
        print(f"   Service Account: {conn.get('service_account', 'N/A')}")
        print()
    
    print("✅ Looker is configured and ready for setup!")
    print("🔧 Next steps:")
    print("   1. Visit the Looker Console link above")
    print("   2. Follow the setup instructions")
    print("   3. Use the provided LookML and Python code")

if __name__ == "__main__":
    show_looker_setup()