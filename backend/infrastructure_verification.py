import subprocess
import platform
import json
from typing import Dict, List, Any
from pathlib import Path

class InfrastructureVerification:
    def __init__(self, project_name: str = "platforge_project"):
        self.project_name = project_name
        self.os_name = platform.system()
        self.project_dir = Path.home() / "platforge_projects" / project_name
        
        # Define what to verify for each service
        self.verification_commands = {
            "aws": {
                "command": "aws --version",
                "name": "AWS CLI",
                "expected_keywords": ["aws-cli"]
            },
            "python": {
                "command": "python3 --version",
                "name": "Python",
                "expected_keywords": ["Python"]
            },
            "docker": {
                "command": "docker --version",
                "name": "Docker",
                "expected_keywords": ["Docker version"]
            },
            "node": {
                "command": "node --version",
                "name": "Node.js",
                "expected_keywords": ["v"]
            },
            "pip": {
                "command": "pip3 --version",
                "name": "pip",
                "expected_keywords": ["pip"]
            }
        }
        
        # Python packages to verify in venv
        self.python_packages = [
            "boto3",
            "pandas",
            "redshift-connector",
            "psycopg2",
            "tableauserverclient",
            "python-dotenv",
            "requests"
        ]

    def _run_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Run a shell command and return result"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {
                "status": "success" if result.returncode == 0 else "error",
                "returncode": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "command": command
            }
        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "message": f"Command timed out after {timeout} seconds",
                "command": command
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "command": command
            }

    def verify_system_packages(self) -> Dict[str, Any]:
        """Verify system-level packages"""
        results = {}
        
        for package_key, config in self.verification_commands.items():
            print(f"Verifying {config['name']}...")
            result = self._run_command(config["command"])
            
            verification_result = {
                "name": config["name"],
                "installed": result["status"] == "success",
                "version": "",
                "location": "",
                "details": result.get("stdout", result.get("stderr", ""))
            }
            
            if result["status"] == "success":
                # Extract version info
                output = result["stdout"]
                if any(keyword in output for keyword in config["expected_keywords"]):
                    verification_result["version"] = output.split('\n')[0] if output else "Unknown"
                    
                    # Try to get installation location
                    if package_key == "python":
                        location_result = self._run_command("which python3")
                        if location_result["status"] == "success":
                            verification_result["location"] = location_result["stdout"]
                    else:
                        location_result = self._run_command(f"which {package_key}")
                        if location_result["status"] == "success":
                            verification_result["location"] = location_result["stdout"]
            
            results[package_key] = verification_result
        
        return results

    def verify_python_packages(self) -> Dict[str, Any]:
        """Verify Python packages in virtual environment"""
        results = {}
        
        # Check if venv exists
        venv_dir = self.project_dir / "venv"
        if not venv_dir.exists():
            return {
                "status": "error",
                "message": "Virtual environment not found",
                "venv_path": str(venv_dir)
            }
        
        # Get python path from venv
        if self.os_name == "Windows":
            python_path = venv_dir / "Scripts" / "python"
        else:
            python_path = venv_dir / "bin" / "python"
        
        # Verify each package
        for package in self.python_packages:
            print(f"Verifying Python package: {package}")
            
            # Try to import and get version
            test_command = f'"{python_path}" -c "import {package.replace("-", "_")}; print(f\'{package}: {{getattr({package.replace("-", "_")}, "__version__", "unknown")}}\');"'
            result = self._run_command(test_command)
            
            package_result = {
                "name": package,
                "installed": result["status"] == "success",
                "version": "",
                "import_path": "",
                "details": result.get("stdout", result.get("stderr", ""))
            }
            
            if result["status"] == "success":
                output = result["stdout"]
                if ":" in output:
                    package_result["version"] = output.split(":", 1)[1].strip()
                
                # Get package location
                location_command = f'"{python_path}" -c "import {package.replace("-", "_")}; print({package.replace("-", "_")}.__file__ if hasattr({package.replace("-", "_")}, \'__file__\') else \'built-in\')"'
                location_result = self._run_command(location_command)
                if location_result["status"] == "success":
                    package_result["import_path"] = location_result["stdout"]
            
            results[package] = package_result
        
        return results

    def verify_project_structure(self) -> Dict[str, Any]:
        """Verify project directory structure"""
        structure_info = {
            "project_dir": {
                "path": str(self.project_dir),
                "exists": self.project_dir.exists(),
                "size_mb": 0
            },
            "venv_dir": {
                "path": str(self.project_dir / "venv"),
                "exists": (self.project_dir / "venv").exists(),
                "size_mb": 0
            },
            "requirements_file": {
                "path": str(self.project_dir / "requirements.txt"),
                "exists": (self.project_dir / "requirements.txt").exists(),
                "content": ""
            }
        }
        
        # Get directory sizes
        try:
            if self.project_dir.exists():
                total_size = sum(f.stat().st_size for f in self.project_dir.rglob('*') if f.is_file())
                structure_info["project_dir"]["size_mb"] = round(total_size / (1024 * 1024), 2)
            
            venv_dir = self.project_dir / "venv"
            if venv_dir.exists():
                venv_size = sum(f.stat().st_size for f in venv_dir.rglob('*') if f.is_file())
                structure_info["venv_dir"]["size_mb"] = round(venv_size / (1024 * 1024), 2)
        except:
            pass
        
        # Read requirements.txt
        requirements_file = self.project_dir / "requirements.txt"
        if requirements_file.exists():
            try:
                with open(requirements_file, 'r') as f:
                    structure_info["requirements_file"]["content"] = f.read()
            except:
                pass
        
        return structure_info

    def run_full_verification(self) -> Dict[str, Any]:
        """Run simplified infrastructure verification focused on services"""
        print("Starting PlatForge.ai platform verification...")
        
        # Check if venv exists first
        venv_dir = self.project_dir / "venv"
        if not venv_dir.exists():
            return {
                "status": "error",
                "message": "Virtual environment not found. Run Infrastructure Setup first.",
                "services": {}
            }
        
        # Get python path from venv
        if self.os_name == "Windows":
            python_path = venv_dir / "Scripts" / "python"
        else:
            python_path = venv_dir / "bin" / "python"
        
        # Read requirements.txt to see what was actually installed
        requirements_file = self.project_dir / "requirements.txt"
        installed_packages = []
        
        if requirements_file.exists():
            try:
                with open(requirements_file, 'r') as f:
                    requirements_content = f.read()
                    for line in requirements_content.strip().split('\n'):
                        if line.strip() and not line.startswith('#'):
                            # Extract package name (remove version specifiers)
                            package_name = line.split('>=')[0].split('==')[0].split('<')[0].strip()
                            installed_packages.append(package_name)
            except Exception as e:
                print(f"Error reading requirements.txt: {e}")
        
        # Map package names to service names and their import names
        package_info = {
            "boto3": {"service": "AWS SDK", "import": "boto3"},
            "redshift-connector": {"service": "Redshift Database", "import": "redshift_connector"},
            "psycopg2-binary": {"service": "PostgreSQL Driver", "import": "psycopg2"}, 
            "tableauserverclient": {"service": "Tableau Client", "import": "tableauserverclient"},
            "python-dotenv": {"service": "Environment Config", "import": "dotenv"},
            "requests": {"service": "HTTP Client", "import": "requests"},
            "pandas": {"service": "Data Processing", "import": "pandas"},
            "awscli": {"service": "AWS CLI", "import": None},  # CLI tool, not importable
            "google-cloud-sql-connector": {"service": "Google Cloud SQL", "import": "google.cloud.sql.connector"},
            "google-cloud-compute": {"service": "Google Compute Engine", "import": "google.cloud.compute"},
            "docker": {"service": "Docker Client", "import": "docker"},
            "python-terraform": {"service": "Terraform", "import": "python_terraform"},
            "google-cloud-bigquery": {"service": "Google BigQuery", "import": "google.cloud.bigquery"},
            "apache-airflow": {"service": "Apache Airflow", "import": "airflow"},
            "pyspark": {"service": "Apache Spark", "import": "pyspark"},
            "dbt-core": {"service": "dbt Core", "import": "dbt"},
            "snowflake-connector-python": {"service": "Snowflake", "import": "snowflake.connector"}
        }
        
        services_status = {}
        
        for package_name in installed_packages:
            if package_name not in package_info:
                # Skip packages not in our mapping
                continue
                
            pkg_info = package_info[package_name]
            service_name = pkg_info["service"]
            import_name = pkg_info["import"]
            
            print(f"Checking {service_name}...")
            
            # Handle CLI tools that aren't importable
            if import_name is None:
                services_status[service_name] = {
                    "status": "installed",
                    "path": "Command line tool"
                }
                continue
            
            # Try to import and get location
            test_command = f'"{python_path}" -c "import {import_name}; print({import_name}.__file__ if hasattr({import_name}, \'__file__\') else \'built-in\')"'
            result = self._run_command(test_command)
            
            if result["status"] == "success":
                location = result["stdout"].strip()
                # Clean up the path to show relative to venv
                if str(venv_dir) in location:
                    location = location.replace(str(venv_dir), "venv")
                
                services_status[service_name] = {
                    "status": "installed",
                    "path": location
                }
            else:
                print(f"Failed to import {import_name}: {result.get('stderr', 'Unknown error')}")
                services_status[service_name] = {
                    "status": "undetected", 
                    "path": f"Import failed: {result.get('stderr', 'Unknown error')[:50]}"
                }
        
        return {
            "status": "success",
            "message": "Service verification completed",
            "services": services_status,
            "debug_info": {
                "venv_path": str(venv_dir),
                "python_path": str(python_path),
                "requirements_file": str(requirements_file),
                "installed_packages": installed_packages,
                "requirements_exists": requirements_file.exists()
            }
        }


if __name__ == "__main__":
    verifier = InfrastructureVerification("aws_redshift_tableau_project")
    result = verifier.run_full_verification()
    print(json.dumps(result, indent=2))