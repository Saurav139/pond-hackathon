"""
PlatForge.ai Tool Catalog - 25 Supported Platform Tools
"""

from typing import Dict, List, Any

class PlatformCatalog:
    def __init__(self):
        self.catalog = {
            # Data Storage & Databases
            "aws_rds": {
                "name": "AWS RDS",
                "category": "Data Storage & Databases",
                "description": "PostgreSQL, MySQL, Aurora managed database service",
                "use_cases": ["web_app", "ecommerce", "saas", "enterprise"],
                "packages": ["boto3", "psycopg2-binary", "mysql-connector-python"],
                "system_requirements": ["awscli"]
            },
            "gcp_cloud_sql": {
                "name": "Google Cloud SQL",
                "category": "Data Storage & Databases",
                "description": "Managed PostgreSQL, MySQL database service",
                "use_cases": ["web_app", "ecommerce", "saas", "gcp_ecosystem"],
                "packages": ["google-cloud-sql-connector", "psycopg2-binary"],
                "system_requirements": ["gcloud"]
            },
            "redshift": {
                "name": "Amazon Redshift",
                "category": "Data Storage & Databases", 
                "description": "Data warehouse for analytics",
                "use_cases": ["analytics", "data_warehouse", "bi", "reporting"],
                "packages": ["redshift-connector", "boto3"],
                "system_requirements": ["awscli"]
            },
            "bigquery": {
                "name": "Google BigQuery",
                "category": "Data Storage & Databases",
                "description": "Serverless data warehouse & analytics",
                "use_cases": ["analytics", "data_warehouse", "big_data", "machine_learning"],
                "packages": ["google-cloud-bigquery", "pandas-gbq"],
                "system_requirements": ["gcloud"]
            },
            "mongodb": {
                "name": "MongoDB Atlas",
                "category": "Data Storage & Databases",
                "description": "NoSQL document database",
                "use_cases": ["web_app", "mobile_app", "content_management", "real_time"],
                "packages": ["pymongo", "motor"],
                "system_requirements": []
            },
            "snowflake": {
                "name": "Snowflake",
                "category": "Data Storage & Databases",
                "description": "Cloud data platform",
                "use_cases": ["data_warehouse", "analytics", "machine_learning", "enterprise"],
                "packages": ["snowflake-connector-python"],
                "system_requirements": []
            },
            "dynamodb": {
                "name": "DynamoDB",
                "category": "Data Storage & Databases",
                "description": "AWS NoSQL key-value store",
                "use_cases": ["serverless", "gaming", "mobile_app", "iot"],
                "packages": ["boto3"],
                "system_requirements": ["awscli"]
            },
            "firestore": {
                "name": "Google Firestore",
                "category": "Data Storage & Databases",
                "description": "GCP NoSQL document database",
                "use_cases": ["mobile_app", "real_time", "serverless", "gcp_ecosystem"],
                "packages": ["google-cloud-firestore"],
                "system_requirements": ["gcloud"]
            },
            
            # Data Processing & ETL
            "aws_glue": {
                "name": "AWS Glue",
                "category": "Data Processing & ETL",
                "description": "Serverless ETL service",
                "use_cases": ["etl", "data_transformation", "serverless", "aws_ecosystem"],
                "packages": ["boto3", "awswrangler"],
                "system_requirements": ["awscli"]
            },
            "gcp_dataflow": {
                "name": "Google Cloud Dataflow",
                "category": "Data Processing & ETL",
                "description": "Stream and batch data processing",
                "use_cases": ["stream_processing", "batch_processing", "etl", "gcp_ecosystem"],
                "packages": ["apache-beam[gcp]", "google-cloud-dataflow"],
                "system_requirements": ["gcloud"]
            },
            "gcp_pubsub": {
                "name": "Google Pub/Sub",
                "category": "Data Processing & ETL",
                "description": "Messaging and streaming service",
                "use_cases": ["messaging", "event_driven", "real_time", "microservices"],
                "packages": ["google-cloud-pubsub"],
                "system_requirements": ["gcloud"]
            },
            
            # Analytics & Visualization
            "tableau": {
                "name": "Tableau",
                "category": "Analytics & Visualization",
                "description": "Business intelligence platform",
                "use_cases": ["business_intelligence", "data_visualization", "reporting", "dashboards"],
                "packages": ["tableauserverclient"],
                "system_requirements": []
            },
            "powerbi": {
                "name": "Power BI",
                "category": "Analytics & Visualization",
                "description": "Microsoft analytics platform",
                "use_cases": ["business_intelligence", "microsoft_ecosystem", "reporting"],
                "packages": ["powerbiclient"],
                "system_requirements": []
            },
            "looker": {
                "name": "Looker",
                "category": "Analytics & Visualization",
                "description": "Google analytics platform",
                "use_cases": ["business_intelligence", "gcp_ecosystem", "enterprise"],
                "packages": ["looker-sdk"],
                "system_requirements": []
            },
            
            # Cloud Infrastructure
            "aws_ec2": {
                "name": "AWS EC2",
                "category": "Cloud Infrastructure",
                "description": "Virtual servers in the cloud",
                "use_cases": ["web_hosting", "compute", "scalable_apps", "aws_ecosystem"],
                "packages": ["boto3", "paramiko"],
                "system_requirements": ["awscli"]
            },
            "gcp_compute": {
                "name": "Google Compute Engine",
                "category": "Cloud Infrastructure",
                "description": "GCP virtual machines",
                "use_cases": ["web_hosting", "compute", "scalable_apps", "gcp_ecosystem"],
                "packages": ["google-cloud-compute"],
                "system_requirements": ["gcloud"]
            },
            "gke": {
                "name": "Google Kubernetes Engine (GKE)",
                "category": "Cloud Infrastructure",
                "description": "Managed Kubernetes service",
                "use_cases": ["kubernetes", "container_orchestration", "microservices", "gcp_ecosystem"],
                "packages": ["kubernetes", "google-cloud-container"],
                "system_requirements": ["kubectl", "gcloud"]
            },
            
            "gcp_build": {
                "name": "Google Cloud Build",
                "category": "DevOps & Monitoring",
                "description": "CI/CD pipeline service",
                "use_cases": ["ci_cd", "automation", "deployment", "gcp_ecosystem"],
                "packages": ["google-cloud-build"],
                "system_requirements": ["gcloud"]
            }
        }
    
    def get_recommendations_for_use_case(self, use_case: str, company_stage: str = "startup", cloud_preference: str = "any") -> List[Dict[str, Any]]:
        """Get tool recommendations based on use case, company stage, and cloud preference"""
        recommendations = []
        
        # Use case mapping to recommended tools - focused on startup needs (one tool per category)
        use_case_recommendations = {
            "saas_platform": {
                "aws": ["aws_rds", "aws_ec2"],
                "gcp": ["gcp_cloud_sql", "gcp_compute"],
                "any": ["aws_rds", "aws_ec2"]
            },
            "ecommerce": {
                "aws": ["aws_rds", "aws_ec2"],
                "gcp": ["gcp_cloud_sql", "gcp_compute"],
                "any": ["aws_rds", "aws_ec2"]
            },
            "data_analytics": {
                "aws": ["redshift", "tableau"],
                "gcp": ["bigquery", "looker"],
                "any": ["bigquery", "tableau"]
            },
            "mobile_app": {
                "aws": ["dynamodb"],
                "gcp": ["firestore"],
                "any": ["mongodb"]
            },
            "web_app": {
                "aws": ["aws_rds", "aws_ec2"],
                "gcp": ["gcp_cloud_sql", "gcp_compute"],
                "any": ["aws_rds", "aws_ec2"]
            },
            "data_pipeline": {
                "aws": ["redshift", "aws_glue"],
                "gcp": ["bigquery", "gcp_dataflow"],
                "any": ["bigquery", "gcp_dataflow"]
            },
            "real_time_app": {
                "aws": ["dynamodb", "aws_ec2"],
                "gcp": ["firestore", "gcp_pubsub"],
                "any": ["mongodb", "firestore"]
            }
        }
        
        # Get base recommendations
        base_tools = use_case_recommendations.get(use_case, {}).get(cloud_preference, 
                    use_case_recommendations.get(use_case, {}).get("any", ["aws_rds"]))
        
        # All recommendations are optimized for startups (cost-effective choices)
        
        # Build recommendation objects
        for tool_id in base_tools:
            if tool_id in self.catalog:
                tool = self.catalog[tool_id].copy()
                tool["tool_id"] = tool_id
                recommendations.append(tool)
        
        return recommendations
    
    def get_tool_by_id(self, tool_id: str) -> Dict[str, Any]:
        """Get specific tool information"""
        return self.catalog.get(tool_id, {})
    
    def get_all_tools_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all tools in a specific category"""
        tools = []
        for tool_id, tool_info in self.catalog.items():
            if tool_info["category"] == category:
                tool_info["tool_id"] = tool_id
                tools.append(tool_info)
        return tools


if __name__ == "__main__":
    catalog = PlatformCatalog()
    
    # Test recommendations
    print("=== SaaS Platform (AWS Preference) ===")
    recommendations = catalog.get_recommendations_for_use_case("saas_platform", "startup", "aws")
    for rec in recommendations:
        print(f"- {rec['name']}: {rec['description']}")
    
    print("\n=== Data Analytics (GCP Preference) ===")
    recommendations = catalog.get_recommendations_for_use_case("data_analytics", "enterprise", "gcp")
    for rec in recommendations:
        print(f"- {rec['name']}: {rec['description']}")
    
    print("\n=== Real-time App (Any Cloud) ===")
    recommendations = catalog.get_recommendations_for_use_case("real_time_app", "startup", "any")
    for rec in recommendations:
        print(f"- {rec['name']}: {rec['description']}")