from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import platform
from dynamic_installation_agent import DynamicInstallationAgent
from infrastructure_verification import InfrastructureVerification
from infrastructure_catalog import PlatformCatalog
from simple_config_generator import SimpleConfigGenerator
from dynamic_cloud_provisioner import DynamicCloudProvisioner
import asyncio
import threading

app = FastAPI(
    title="PlatForge.ai API",
    version="1.0",
    description="AI-powered platform engineering automation",
)

class InstallationRequest(BaseModel):
    flow_description: str = None
    project_name: str = "platforge_project"
    recommendations: List[dict] = None

class VerificationRequest(BaseModel):
    project_name: str = "platforge_project"

class RecommendationRequest(BaseModel):
    use_case: str
    company_stage: str = "startup"
    cloud_preference: str = "any"

class ConfigurationRequest(BaseModel):
    project_display_name: str
    project_name: str = "platforge_project"
    include_cloud: bool = False

class AutoProvisionRequest(BaseModel):
    startup_name: str
    founder_email: str
    founder_name: str
    project_name: str = "platforge_project"
    recommendations: Optional[List[str]] = None  # AI recommendations for services

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:3001", 
        "http://127.0.0.1:3000",
        "https://*.vercel.app",  # Allow all Vercel domains
        "https://your-app.vercel.app"  # Replace with your actual domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "PlatForge.ai API is running!", 
        "endpoints": {
            "os": "/os",
            "setup": "/setup",
            "verify": "/verify",
            "recommendations": "/recommendations",
            "configure": "/configure",
            "auto_provision": "/auto-provision"
        }
    }

@app.get("/os")
async def get_os():
    return {
        "os": platform.system(),
        "version": platform.release()
    }

@app.post("/setup")
async def setup_infrastructure(request: InstallationRequest):
    """Setup infrastructure packages based on pipeline and OS"""
    try:
        agent = DynamicInstallationAgent(request.project_name)
        
        # Run installation based on what's provided
        def run_installation():
            if request.recommendations:
                # Use recommendation-based installation
                return agent.install_packages_from_recommendations(request.recommendations)
            elif request.flow_description:
                # Use flow description-based installation
                return agent.install_packages_for_flow(request.flow_description)
            else:
                return {
                    "status": "error",
                    "message": "Either flow_description or recommendations must be provided"
                }
        
        result = run_installation()
        
        return {
            "status": "success",
            "message": "Infrastructure setup completed",
            "result": result
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Infrastructure setup failed: {str(e)}"
        }

@app.post("/verify")
async def verify_infrastructure(request: VerificationRequest):
    """Verify infrastructure installation and show software versions"""
    try:
        verifier = InfrastructureVerification(request.project_name)
        
        # Run verification
        def run_verification():
            return verifier.run_full_verification()
        
        result = run_verification()
        
        return {
            "status": "success",
            "message": "Infrastructure verification completed",
            "result": result
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Infrastructure verification failed: {str(e)}"
        }

@app.post("/recommendations")
async def get_infrastructure_recommendations(request: RecommendationRequest):
    """Get infrastructure recommendations based on use case and preferences"""
    try:
        catalog = PlatformCatalog()
        
        # Get recommendations based on request parameters (startup-focused)
        recommendations = catalog.get_recommendations_for_use_case(
            use_case=request.use_case,
            company_stage="startup",  # Always startup
            cloud_preference=request.cloud_preference
        )
        
        return {
            "status": "success",
            "message": f"Found {len(recommendations)} recommendations for {request.use_case}",
            "recommendations": recommendations,
            "request_parameters": {
                "use_case": request.use_case,
                "company_stage": request.company_stage,
                "cloud_preference": request.cloud_preference
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get recommendations: {str(e)}"
        }

@app.post("/configure")
async def generate_configuration(request: ConfigurationRequest):
    """Generate ready-to-use configuration files"""
    try:
        generator = SimpleConfigGenerator(request.project_name)
        
        # Get installed packages from verification
        verifier = InfrastructureVerification(request.project_name)
        verification_result = verifier.run_full_verification()
        
        if verification_result["status"] != "success":
            return {
                "status": "error",
                "message": "Please complete installation and verification first"
            }
        
        # Get list of installed packages
        installed_packages = verification_result.get("debug_info", {}).get("installed_packages", [])
        
        # Generate configurations
        config_result = generator.generate_ready_to_use_configs(
            project_display_name=request.project_display_name,
            installed_tools=installed_packages,
            include_cloud=request.include_cloud
        )
        
        return {
            "status": "success",
            "message": config_result["message"],
            "result": config_result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Configuration generation failed: {str(e)}"
        }

@app.post("/auto-provision")
async def auto_provision_startup_infrastructure(request: AutoProvisionRequest):
    """Automatically provision cloud infrastructure based on installed pipeline"""
    try:
        # Get verification results to see what's installed (only if not using recommendations)
        verification_result = {"status": "success", "debug_info": {"installed_packages": []}}
        
        if not request.recommendations:
            # Only require verification if we're not using AI recommendations
            verifier = InfrastructureVerification(request.project_name)
            verification_result = verifier.run_full_verification()
            
            if verification_result["status"] != "success":
                return {
                    "status": "error",
                    "message": "Please complete installation and verification first"
                }
        
        # Determine pipeline services from AI recommendations or installed packages
        pipeline_services = []
        
        print(f"🔍 Debug - Received request:")
        print(f"   startup_name: {request.startup_name}")
        print(f"   recommendations: {request.recommendations}")
        print(f"   recommendations type: {type(request.recommendations)}")
        
        if request.recommendations:
            # Use AI recommendations to determine services
            print(f"🤖 Using AI recommendations: {request.recommendations}")
            
            # Map recommendation keywords to service IDs
            recommendation_to_service_map = {
                # Database services
                "rds": "aws_rds",
                "postgres": "aws_rds", 
                "postgresql": "aws_rds",
                "mysql": "aws_rds",
                "database": "aws_rds",
                "redshift": "redshift",
                "bigquery": "bigquery",
                "cloud sql": "gcp_cloud_sql",
                "firestore": "firestore",
                "dynamodb": "dynamodb",
                "mongodb": "mongodb",
                "snowflake": "snowflake",
                
                # Compute services
                "ec2": "aws_ec2",
                "compute": "gcp_compute",
                "virtual machine": "gcp_compute",
                "vm": "gcp_compute",
                "kubernetes": "gke",
                "gke": "gke",
                
                # Analytics & Data
                "analytics": "bigquery",
                "data warehouse": "bigquery",
                "tableau": "tableau",
                "powerbi": "powerbi",
                "power bi": "powerbi",
                "looker": "looker",
                
                # Other services
                "storage": "cloud_storage",
                "s3": "s3",
                "dataflow": "gcp_dataflow",
                "glue": "aws_glue",
                "pubsub": "gcp_pubsub",
                "pub/sub": "gcp_pubsub"
            }
            
            # Extract services from recommendations
            for recommendation in request.recommendations:
                rec_lower = recommendation.lower()
                for keyword, service_id in recommendation_to_service_map.items():
                    if keyword in rec_lower and service_id not in pipeline_services:
                        pipeline_services.append(service_id)
                        print(f"📝 Mapped '{keyword}' → {service_id}")
            
            if not pipeline_services:
                # If no specific services found in recommendations, provide default based on common patterns
                print("🔍 No specific services found in recommendations, using intelligent defaults")
                if any(word in " ".join(request.recommendations).lower() for word in ["data", "analytics", "database"]):
                    pipeline_services = ["bigquery", "aws_rds"]  # Mixed cloud for data use cases
                else:
                    pipeline_services = ["aws_rds", "aws_ec2"]  # Default web app stack
        
        else:
            # Fallback: Use installed packages (old behavior)
            print("📦 No recommendations provided, falling back to installed packages")
            
            installed_packages = verification_result.get("debug_info", {}).get("installed_packages", [])
            
            package_to_service_map = {
                "redshift-connector": "redshift",
                "psycopg2-binary": "aws_rds",
                "mysql-connector-python": "aws_rds", 
                "pymongo": "mongodb",
                "snowflake-connector-python": "snowflake",
                "paramiko": "aws_ec2",
                "fabric": "aws_ec2",
                "awswrangler": "aws_glue",
                "google-cloud-bigquery": "bigquery",
                "google-cloud-compute": "gcp_compute",
                "google-cloud-sql-connector": "gcp_cloud_sql",
                "google-cloud-firestore": "firestore",
                "apache-beam[gcp]": "gcp_dataflow",
                "google-cloud-dataflow": "gcp_dataflow",
                "google-cloud-pubsub": "gcp_pubsub",
                "kubernetes": "gke",
                "google-cloud-container": "gke",
                "google-cloud-build": "gcp_build",
                "tableauserverclient": "tableau",
                "powerbiclient": "powerbi",
                "looker-sdk": "looker",
            }
            
            for package in installed_packages:
                if package in package_to_service_map:
                    service_id = package_to_service_map[package]
                    if service_id not in pipeline_services:
                        pipeline_services.append(service_id)
            
            if not pipeline_services:
                return {
                    "status": "error",
                    "message": "No supported services found. Either provide recommendations or install specific service packages."
                }
        
        # Initialize provisioner
        provisioner = DynamicCloudProvisioner()
        
        # Startup info from request
        startup_info = {
            "name": request.startup_name,
            "email": request.founder_email,
            "founder_name": request.founder_name
        }
        
        # Auto-provision everything
        provisioning_result = provisioner.auto_provision_startup_infrastructure(
            startup_info, pipeline_services
        )
        
        return {
            "status": "success",
            "message": f"🎉 {request.startup_name} infrastructure provisioned successfully!",
            "result": provisioning_result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Auto-provisioning failed: {str(e)}"
        }


if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.environ.get("PORT", 8001))
    host = "0.0.0.0"  # Railway needs this
    
    print("Starting PlatForge.ai API...")
    print(f"API endpoint: http://{host}:{port}")
    print(f"Auto-provision endpoint: http://{host}:{port}/auto-provision")
    uvicorn.run(app, host=host, port=port)