#!/usr/bin/env python3
"""
Debug the accounts structure to find Looker
"""

import json
from pathlib import Path

def debug_accounts():
    """Debug accounts to find Looker data"""
    
    accounts_file = Path(__file__).parent / "platforge_accounts.json"
    
    if not accounts_file.exists():
        print("❌ No accounts database found")
        return
    
    with open(accounts_file, 'r') as f:
        data = json.load(f)
    
    # Handle both dictionary and list formats
    if isinstance(data, dict):
        accounts = list(data.values()) if data else []
    else:
        accounts = data if data else []
    
    print(f"🔍 Found {len(accounts)} accounts")
    print("=" * 60)
    
    # Check the most recent few accounts
    recent_accounts = accounts[-3:] if len(accounts) >= 3 else accounts
    for i, account in enumerate(recent_accounts, max(1, len(accounts)-len(recent_accounts)+1)):
        print(f"\n📋 Account #{i}: {account.get('startup_name', 'Unknown')}")
        
        if "provisioned_resources" in account:
            print(f"   Resources: {len(account['provisioned_resources'])}")
            for j, resource in enumerate(account["provisioned_resources"]):
                service = resource.get("service", "Unknown")
                status = resource.get("status", "Unknown")
                print(f"      {j+1}. {service} - {status}")
        else:
            print("   No provisioned_resources found")
        
        # Check if this account has Looker
        has_looker = False
        if "provisioned_resources" in account:
            for resource in account["provisioned_resources"]:
                if resource.get("service") == "Looker":
                    has_looker = True
                    print(f"   🎯 FOUND LOOKER!")
                    print(f"      Name: {resource.get('name', 'N/A')}")
                    print(f"      Status: {resource.get('status', 'N/A')}")
                    if "setup_instructions" in resource:
                        print(f"      Setup Instructions: {len(resource['setup_instructions'])} steps")
                    if "sample_lookml" in resource:
                        print(f"      LookML: {'Yes' if resource['sample_lookml'].strip() else 'No'}")
                    break
        
        if not has_looker:
            print("   ❌ No Looker found in this account")

if __name__ == "__main__":
    debug_accounts()