import platform
import subprocess
import psutil
import json
import os
from typing import Dict, List, Any
from pydantic import BaseModel


class SystemInfo(BaseModel):
    os: str
    version: str
    architecture: str
    hostname: str


class ResourceInfo(BaseModel):
    ram_gb: int
    cpu_cores: int
    cpu_frequency_mhz: float
    disk_space_gb: int
    available_disk_gb: int


class SoftwareInfo(BaseModel):
    docker_installed: bool
    kubernetes_installed: bool
    terraform_installed: bool
    aws_cli_installed: bool
    gcp_cli_installed: bool
    azure_cli_installed: bool
    python_version: str
    node_version: str


class EnvironmentReport(BaseModel):
    system: SystemInfo
    resources: ResourceInfo
    software: SoftwareInfo
    recommendations: List[str]


class EnvironmentDetectionAgent:
    def __init__(self):
        self.agent_name = "Environment Detection Agent"
        self.version = "1.0.0"
    
    def detect_system_info(self) -> SystemInfo:
        """Detect basic system information"""
        return SystemInfo(
            os=platform.system(),
            version=platform.version(),
            architecture=platform.machine(),
            hostname=platform.node()
        )
    
    def check_resources(self) -> ResourceInfo:
        """Check system resources"""
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        cpu_freq = psutil.cpu_freq()
        
        return ResourceInfo(
            ram_gb=memory.total // (1024**3),
            cpu_cores=psutil.cpu_count(),
            cpu_frequency_mhz=cpu_freq.current if cpu_freq else 0.0,
            disk_space_gb=disk.total // (1024**3),
            available_disk_gb=disk.free // (1024**3)
        )
    
    def _check_command_exists(self, command: str) -> bool:
        """Check if a command exists in the system"""
        try:
            subprocess.run([command, '--version'], 
                         capture_output=True, check=True, timeout=5)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def _get_version(self, command: str) -> str:
        """Get version of a command"""
        try:
            result = subprocess.run([command, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.stdout.strip().split('\n')[0]
        except:
            return "Unknown"
    
    def detect_software(self) -> SoftwareInfo:
        """Detect installed software and tools"""
        return SoftwareInfo(
            docker_installed=self._check_command_exists('docker'),
            kubernetes_installed=self._check_command_exists('kubectl'),
            terraform_installed=self._check_command_exists('terraform'),
            aws_cli_installed=self._check_command_exists('aws'),
            gcp_cli_installed=self._check_command_exists('gcloud'),
            azure_cli_installed=self._check_command_exists('az'),
            python_version=self._get_version('python3') or self._get_version('python'),
            node_version=self._get_version('node')
        )
    
    def generate_recommendations(self, system: SystemInfo, resources: ResourceInfo, 
                               software: SoftwareInfo) -> List[str]:
        """Generate recommendations based on detected environment"""
        recommendations = []
        
        # Resource recommendations
        if resources.ram_gb < 4:
            recommendations.append("Consider upgrading RAM to at least 4GB for better performance")
        
        if resources.available_disk_gb < 10:
            recommendations.append("Low disk space detected. Free up space before deployment")
        
        # Software recommendations
        if not software.docker_installed:
            recommendations.append("Install Docker for containerized deployments")
        
        if not software.terraform_installed:
            recommendations.append("Install Terraform for infrastructure automation")
        
        # Cloud CLI recommendations
        cloud_clis = [software.aws_cli_installed, software.gcp_cli_installed, software.azure_cli_installed]
        if not any(cloud_clis):
            recommendations.append("Install at least one cloud CLI (AWS, GCP, or Azure)")
        
        # OS-specific recommendations
        if system.os == "Windows":
            recommendations.append("Consider using WSL2 for better Linux compatibility")
        
        return recommendations
    
    def run_full_scan(self) -> EnvironmentReport:
        """Run complete environment detection and return report"""
        print(f"🔍 {self.agent_name} starting environment scan...")
        
        system_info = self.detect_system_info()
        print(f"✅ System detected: {system_info.os} {system_info.architecture}")
        
        resource_info = self.check_resources()
        print(f"✅ Resources scanned: {resource_info.ram_gb}GB RAM, {resource_info.cpu_cores} CPU cores")
        
        software_info = self.detect_software()
        print(f"✅ Software scan complete")
        
        recommendations = self.generate_recommendations(system_info, resource_info, software_info)
        
        report = EnvironmentReport(
            system=system_info,
            resources=resource_info,
            software=software_info,
            recommendations=recommendations
        )
        
        print(f"📋 Environment scan complete. {len(recommendations)} recommendations generated.")
        return report
    
    def save_report(self, report: EnvironmentReport, filename: str = "environment_report.json"):
        """Save environment report to JSON file"""
        with open(filename, 'w') as f:
            json.dump(report.model_dump(), f, indent=2)
        print(f"💾 Report saved to {filename}")


if __name__ == "__main__":
    agent = EnvironmentDetectionAgent()
    report = agent.run_full_scan()
    agent.save_report(report)
    
    print("\n" + "="*50)
    print("ENVIRONMENT REPORT SUMMARY")
    print("="*50)
    print(f"OS: {report.system.os} {report.system.version}")
    print(f"Architecture: {report.system.architecture}")
    print(f"RAM: {report.resources.ram_gb}GB")
    print(f"CPU Cores: {report.resources.cpu_cores}")
    print(f"Available Disk: {report.resources.available_disk_gb}GB")
    print(f"\nInstalled Tools:")
    print(f"  Docker: {'✅' if report.software.docker_installed else '❌'}")
    print(f"  Terraform: {'✅' if report.software.terraform_installed else '❌'}")
    print(f"  AWS CLI: {'✅' if report.software.aws_cli_installed else '❌'}")
    print(f"  GCP CLI: {'✅' if report.software.gcp_cli_installed else '❌'}")
    print(f"  Azure CLI: {'✅' if report.software.azure_cli_installed else '❌'}")
    
    if report.recommendations:
        print(f"\n🔧 Recommendations:")
        for i, rec in enumerate(report.recommendations, 1):
            print(f"  {i}. {rec}")