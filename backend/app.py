from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000"],
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
        # Get verification results to see what's installed
        verifier = InfrastructureVerification(request.project_name)
        verification_result = verifier.run_full_verification()
        
        if verification_result["status"] != "success":
            return {
                "status": "error",
                "message": "Please complete installation and verification first"
            }
        
        # Get installed packages (these map to our 25 services)
        installed_packages = verification_result.get("debug_info", {}).get("installed_packages", [])
        
        # Map installed packages to service IDs - only AWS/GCP services + Analytics tools
        package_to_service_map = {
            # Database-specific packages
            "redshift-connector": "redshift",
            "psycopg2-binary": "aws_rds",  # PostgreSQL driver for RDS
            "mysql-connector-python": "aws_rds",  # MySQL driver for RDS
            "pymongo": "mongodb",
            "snowflake-connector-python": "snowflake",
            
            # AWS-specific packages
            "paramiko": "aws_ec2",  # SSH client for EC2
            "fabric": "aws_ec2",   # Remote execution for EC2
            "awswrangler": "aws_glue",  # AWS Glue data wrangler
            
            # GCP-specific packages
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
            
            # Analytics & Visualization packages (third-party)
            "tableauserverclient": "tableau",
            "powerbiclient": "powerbi",
            "looker-sdk": "looker",
            
            # Note: boto3 is generic AWS SDK - don't auto-map to specific service
            # Only map when specific service packages are installed
        }
        
        # Convert packages to service IDs
        pipeline_services = []
        for package in installed_packages:
            if package in package_to_service_map:
                service_id = package_to_service_map[package]
                if service_id not in pipeline_services:
                    pipeline_services.append(service_id)
        
        # If no specific services found, check if generic SDKs are present
        if not pipeline_services:
            generic_sdks = []
            if "boto3" in installed_packages:
                generic_sdks.append("boto3 (AWS SDK)")
            if any(pkg.startswith("google-cloud") for pkg in installed_packages):
                generic_sdks.append("google-cloud (GCP SDK)")
            
            if generic_sdks:
                return {
                    "status": "error",
                    "message": f"Found generic SDKs ({', '.join(generic_sdks)}) but no specific service packages. Install specific packages like 'redshift-connector', 'psycopg2-binary', etc. to enable auto-provisioning."
                }
            else:
                return {
                    "status": "error",
                    "message": "No supported services found in your pipeline"
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
    print("Starting PlatForge.ai API...")
    print("API endpoint: http://localhost:8001")
    print("Auto-provision endpoint: http://localhost:8001/auto-provision")
    uvicorn.run(app, host="localhost", port=8001)