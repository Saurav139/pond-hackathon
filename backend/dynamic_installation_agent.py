import os
import subprocess
import platform
import json
import time
from typing import Dict, List, Any, Optional
from pathlib import Path
import venv
from infrastructure_catalog import PlatformCatalog

class DynamicInstallationAgent:
    def __init__(self, project_name: str = "platforge_project"):
        self.project_name = project_name
        self.os_name = platform.system()
        self.project_dir = Path.home() / "platforge_projects" / project_name
        self.venv_dir = self.project_dir / "venv"
        self.catalog = PlatformCatalog()
        
        # Package mappings for different services (will be expanded dynamically)
        self.service_packages = {
            "aws": {
                "python": ["boto3>=1.26.0", "awscli"],
                "system": {
                    "Darwin": "brew install awscli",
                    "Linux": "sudo apt-get install -y awscli",
                    "Windows": "winget install Amazon.AWSCLI"
                }
            },
            "redshift": {
                "python": ["redshift-connector>=2.0.0", "psycopg2-binary>=2.9.0"],
                "system": {}
            },
            "ec2": {
                "python": ["paramiko>=2.8.0", "boto3>=1.26.0"],
                "system": {}
            },
            "tableau": {
                "python": ["tableauserverclient>=0.25.0"],
                "system": {}
            },
            "lambda": {
                "python": ["boto3>=1.26.0"],
                "system": {}
            },
            "s3": {
                "python": ["boto3>=1.26.0"],
                "system": {}
            },
            "pandas": {
                "python": ["pandas>=1.5.0"],
                "system": {}
            },
            "common": {
                "python": ["python-dotenv>=1.0.0", "requests>=2.28.0"],
                "system": {}
            }
        }
    
    def parse_infrastructure_flow(self, flow_description: str) -> List[str]:
        """Parse flow description and extract required services"""
        # For now, this is a simple keyword-based parser
        # In production, this would use the chatbot's structured output
        
        services = []
        flow_lower = flow_description.lower()
        
        # Check for various service keywords
        service_keywords = {
            "aws": ["aws", "amazon"],
            "s3": ["s3", "storage"],
            "lambda": ["lambda", "serverless"],
            "redshift": ["redshift", "data warehouse"],
            "ec2": ["ec2", "server", "virtual machine", "compute"],
            "tableau": ["tableau", "visualization"],
            "pandas": ["pandas", "data processing", "csv", "excel"]
        }
        
        for service, keywords in service_keywords.items():
            if any(keyword in flow_lower for keyword in keywords):
                services.append(service)
        
        # Always add common utilities
        services.append("common")
        
        return list(set(services))  # Remove duplicates
    
    def generate_requirements_from_flow(self, services: List[str]) -> List[str]:
        """Generate Python requirements based on services needed"""
        requirements = []
        
        for service in services:
            if service in self.service_packages:
                requirements.extend(self.service_packages[service]["python"])
        
        return list(set(requirements))  # Remove duplicates
    
    def generate_system_commands_from_flow(self, services: List[str]) -> List[Dict[str, str]]:
        """Generate system installation commands based on services"""
        commands = []
        
        for service in services:
            if service in self.service_packages:
                system_config = self.service_packages[service]["system"]
                if self.os_name in system_config and system_config[self.os_name]:
                    commands.append({
                        "service": service,
                        "command": system_config[self.os_name]
                    })
        
        return commands
    
    def create_project_structure(self) -> Dict[str, Any]:
        """Create project directory and virtual environment"""
        try:
            self.project_dir.mkdir(parents=True, exist_ok=True)
            
            if not self.venv_dir.exists():
                venv.create(self.venv_dir, with_pip=True)
            
            return {
                "status": "success",
                "message": "Project structure created successfully",
                "project_dir": str(self.project_dir),
                "venv_dir": str(self.venv_dir)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create project structure: {str(e)}"
            }
    
    def _run_command(self, command: str, timeout: int = 300) -> Dict[str, Any]:
        """Run a shell command with timeout"""
        print(f"Executing command: {command}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            print(f"Command completed with return code: {result.returncode}")
            return {
                "status": "success" if result.returncode == 0 else "error",
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": command
            }
        except subprocess.TimeoutExpired:
            print(f"Command timed out after {timeout} seconds")
            return {
                "status": "error",
                "message": f"Command timed out after {timeout} seconds",
                "command": command
            }
        except Exception as e:
            print(f"Command failed with exception: {e}")
            return {
                "status": "error",
                "message": str(e),
                "command": command
            }
    
    def install_packages_for_flow(self, flow_description: str) -> Dict[str, Any]:
        """Install packages based on infrastructure flow description"""
        
        # Parse the flow to get required services
        required_services = self.parse_infrastructure_flow(flow_description)
        
        # Generate requirements
        python_requirements = self.generate_requirements_from_flow(required_services)
        system_commands = self.generate_system_commands_from_flow(required_services)
        
        installation_log = []
        
        # Step 1: Create project structure
        structure_result = self.create_project_structure()
        installation_log.append({"step": "project_structure", "result": structure_result})
        
        if structure_result["status"] == "error":
            return {
                "status": "error",
                "message": "Failed to create project structure",
                "log": installation_log
            }
        
        # Step 2: Create requirements.txt
        requirements_file = self.project_dir / "requirements.txt"
        with open(requirements_file, 'w') as f:
            for req in python_requirements:
                f.write(f"{req}\n")
        
        # Step 3: Install essential system packages (with shorter timeout and error handling)
        system_results = []
        essential_packages = ["aws"]  # Only install essential ones
        
        for cmd_info in system_commands:
            if any(essential in cmd_info['service'] for essential in essential_packages):
                print(f"Installing {cmd_info['service']}...")
                # Use shorter timeout and don't fail if it doesn't work
                result = self._run_command(cmd_info['command'], timeout=120)
                result["service"] = cmd_info['service']
                system_results.append(result)
                time.sleep(1)
            else:
                print(f"Skipping {cmd_info['service']} (not essential for this demo)...")
                system_results.append({
                    "service": cmd_info['service'],
                    "status": "skipped",
                    "message": "Not essential for demo"
                })
        
        installation_log.append({"step": "system_packages", "result": system_results})
        
        # Step 4: Install Python packages one by one for better progress tracking
        if self.os_name == "Windows":
            pip_path = self.venv_dir / "Scripts" / "pip"
        else:
            pip_path = self.venv_dir / "bin" / "pip"
        
        print("Upgrading pip...")
        upgrade_cmd = f'"{pip_path}" install --upgrade pip'
        upgrade_result = self._run_command(upgrade_cmd, timeout=120)
        
        if upgrade_result["status"] == "error":
            print(f"Warning: Failed to upgrade pip: {upgrade_result.get('stderr', 'Unknown error')}")
        
        # Install each Python package individually to show progress
        python_results = []
        for requirement in python_requirements:
            package_name = requirement.split('>=')[0].split('==')[0].strip()
            print(f"Installing Python package: {package_name}...")
            
            install_cmd = f'"{pip_path}" install "{requirement}"'
            result = self._run_command(install_cmd, timeout=300)  # 5 minutes per package
            result["package"] = package_name
            python_results.append(result)
            
            if result["status"] == "success":
                print(f"✅ Successfully installed {package_name}")
            else:
                print(f"❌ Failed to install {package_name}: {result.get('stderr', 'Unknown error')}")
            
            time.sleep(0.5)  # Brief pause between installations
        
        installation_log.append({"step": "python_packages", "result": python_results})
        
        return {
            "status": "success",
            "message": "Dynamic installation completed",
            "flow_description": flow_description,
            "detected_services": required_services,
            "python_requirements": python_requirements,
            "project_dir": str(self.project_dir),
            "log": installation_log
        }
    
    def install_packages_from_recommendations(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Install packages based on catalog recommendations"""
        
        installation_log = []
        
        # Step 1: Create project structure
        structure_result = self.create_project_structure()
        installation_log.append({"step": "project_structure", "result": structure_result})
        
        if structure_result["status"] == "error":
            return {
                "status": "error",
                "message": "Failed to create project structure",
                "log": installation_log
            }
        
        # Step 2: Collect all packages from recommendations
        all_packages = []
        tool_names = []
        
        for rec in recommendations:
            tool_names.append(rec["name"])
            if "packages" in rec:
                all_packages.extend(rec["packages"])
        
        # Remove duplicates while preserving order
        unique_packages = []
        seen = set()
        for pkg in all_packages:
            if pkg not in seen:
                unique_packages.append(pkg)
                seen.add(pkg)
        
        # Step 3: Create requirements.txt
        requirements_file = self.project_dir / "requirements.txt"
        with open(requirements_file, 'w') as f:
            for pkg in unique_packages:
                f.write(f"{pkg}\n")
        
        # Step 4: Install Python packages
        if self.os_name == "Windows":
            pip_path = self.venv_dir / "Scripts" / "pip"
        else:
            pip_path = self.venv_dir / "bin" / "pip"
        
        print("Upgrading pip...")
        upgrade_cmd = f'"{pip_path}" install --upgrade pip'
        upgrade_result = self._run_command(upgrade_cmd, timeout=120)
        
        if upgrade_result["status"] == "error":
            print(f"Warning: Failed to upgrade pip: {upgrade_result.get('stderr', 'Unknown error')}")
        
        # Install each Python package individually
        python_results = []
        for package in unique_packages:
            package_name = package.split('>=')[0].split('==')[0].split('[')[0].strip()
            print(f"Installing Python package: {package_name}...")
            
            install_cmd = f'"{pip_path}" install "{package}"'
            result = self._run_command(install_cmd, timeout=300)
            result["package"] = package_name
            python_results.append(result)
            
            if result["status"] == "success":
                print(f"✅ Successfully installed {package_name}")
            else:
                print(f"❌ Failed to install {package_name}: {result.get('stderr', 'Unknown error')}")
            
            time.sleep(0.5)
        
        installation_log.append({"step": "python_packages", "result": python_results})
        
        return {
            "status": "success",
            "message": "Catalog-based installation completed",
            "recommended_tools": tool_names,
            "installed_packages": unique_packages,
            "project_dir": str(self.project_dir),
            "log": installation_log
        }


# Test the current flow
if __name__ == "__main__":
    # This is the current test flow
    test_flow = "Transfer local data to AWS S3, then load into Redshift data warehouse, and visualize with Tableau"
    
    agent = DynamicInstallationAgent("test_project")
    result = agent.install_packages_for_flow(test_flow)
    print(json.dumps(result, indent=2))