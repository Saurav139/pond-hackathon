import platform
import subprocess
import psutil
import json
from typing import Dict, List, Any
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain import hub
import os


class OSCheckingAgent:
    def __init__(self, openai_api_key: str = None):
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it directly.")
        
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=self.api_key
        )
        
        self.tools = self._create_tools()
        self.agent_executor = self._create_agent()
    
    def _create_tools(self) -> List[Tool]:
        """Create LangChain tools for OS checking"""
        
        def get_system_info() -> str:
            """Get basic system information"""
            info = {
                "os": platform.system(),
                "version": platform.version(),
                "architecture": platform.machine(),
                "hostname": platform.node(),
                "platform": platform.platform()
            }
            return json.dumps(info, indent=2)
        
        def get_resource_info() -> str:
            """Get system resource information"""
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            cpu_freq = psutil.cpu_freq()
            
            info = {
                "ram_total_gb": round(memory.total / (1024**3), 2),
                "ram_available_gb": round(memory.available / (1024**3), 2),
                "ram_percent_used": memory.percent,
                "cpu_cores": psutil.cpu_count(),
                "cpu_frequency_mhz": cpu_freq.current if cpu_freq else 0.0,
                "disk_total_gb": round(disk.total / (1024**3), 2),
                "disk_free_gb": round(disk.free / (1024**3), 2),
                "disk_percent_used": round((disk.used / disk.total) * 100, 2)
            }
            return json.dumps(info, indent=2)
        
        def check_software_installed() -> str:
            """Check if common development software is installed"""
            def command_exists(command: str) -> bool:
                try:
                    subprocess.run([command, '--version'], 
                                 capture_output=True, check=True, timeout=5)
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                    return False
            
            def get_version(command: str) -> str:
                try:
                    result = subprocess.run([command, '--version'], 
                                          capture_output=True, text=True, timeout=5)
                    return result.stdout.strip().split('\n')[0]
                except:
                    return "Not installed"
            
            software = {
                "docker": {
                    "installed": command_exists('docker'),
                    "version": get_version('docker') if command_exists('docker') else "Not installed"
                },
                "kubernetes": {
                    "installed": command_exists('kubectl'),
                    "version": get_version('kubectl') if command_exists('kubectl') else "Not installed"
                },
                "terraform": {
                    "installed": command_exists('terraform'),
                    "version": get_version('terraform') if command_exists('terraform') else "Not installed"
                },
                "aws_cli": {
                    "installed": command_exists('aws'),
                    "version": get_version('aws') if command_exists('aws') else "Not installed"
                },
                "gcp_cli": {
                    "installed": command_exists('gcloud'),
                    "version": get_version('gcloud') if command_exists('gcloud') else "Not installed"
                },
                "azure_cli": {
                    "installed": command_exists('az'),
                    "version": get_version('az') if command_exists('az') else "Not installed"
                },
                "python": {
                    "installed": command_exists('python3') or command_exists('python'),
                    "version": get_version('python3') or get_version('python')
                },
                "node": {
                    "installed": command_exists('node'),
                    "version": get_version('node') if command_exists('node') else "Not installed"
                }
            }
            return json.dumps(software, indent=2)
        
        return [
            Tool(
                name="get_system_info",
                description="Get basic system information including OS, version, architecture, and hostname",
                func=get_system_info
            ),
            Tool(
                name="get_resource_info", 
                description="Get system resource information including RAM, CPU, and disk usage",
                func=get_resource_info
            ),
            Tool(
                name="check_software_installed",
                description="Check if common development tools and cloud CLIs are installed",
                func=check_software_installed
            )
        ]
    
    def _create_agent(self) -> AgentExecutor:
        """Create LangChain agent for OS checking"""
        
        # Create a specific prompt for the agent
        prompt = PromptTemplate(
            input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
            template="""You are an OS checking agent. Use the available tools to analyze the system and provide recommendations.

Available tools: {tools}
Tool names: {tool_names}

IMPORTANT: Use the EXACT tool names:
- get_system_info (for OS, version, architecture info)
- get_resource_info (for RAM, CPU, disk info)  
- check_software_installed (for software versions)

Question: {input}

Thought: I need to call the tools using their exact names.
{agent_scratchpad}"""
        )
        
        # Create the agent
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # Create agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
        
        return agent_executor
    
    def run_os_check(self) -> Dict[str, Any]:
        """Run the complete OS checking workflow"""
        
        query = """Please perform a complete system analysis:
        1. Get system information (OS, version, architecture)
        2. Check system resources (RAM, CPU, disk)
        3. Check what software is installed
        4. Based on the findings, provide recommendations for improvements"""
        
        # Run the agent
        response = self.agent_executor.invoke({"input": query})
        
        # Also get raw data for structured output
        system_info = json.loads(self.tools[0].func())
        resource_info = json.loads(self.tools[1].func())
        software_info = json.loads(self.tools[2].func())
        
        # Combine all data
        full_system_info = {**system_info, **resource_info, "software": software_info}
        
        # Generate recommendations
        recommendations = self._generate_recommendations(full_system_info)
        
        return {
            "system_info": full_system_info,
            "recommendations": recommendations,
            "agent_response": response["output"],
            "scan_complete": True
        }
    
    def _generate_recommendations(self, system_info: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on system info"""
        recommendations = []
        
        # RAM recommendations
        if system_info.get("ram_total_gb", 0) < 4:
            recommendations.append("Consider upgrading RAM to at least 4GB for better performance")
        
        if system_info.get("ram_percent_used", 0) > 80:
            recommendations.append("High RAM usage detected. Consider closing unnecessary applications")
        
        # Disk recommendations
        if system_info.get("disk_free_gb", 0) < 10:
            recommendations.append("Low disk space detected. Free up space before deployment")
        
        if system_info.get("disk_percent_used", 0) > 90:
            recommendations.append("Critical disk space warning. Immediate cleanup required")
        
        return recommendations
    
    def format_report(self, result: Dict[str, Any]) -> str:
        """Format the OS check result into a readable report"""
        system_info = result["system_info"]
        recommendations = result["recommendations"]
        
        report = []
        report.append("="*60)
        report.append("OS CHECKING AGENT REPORT")
        report.append("="*60)
        
        # System Information
        report.append("\n🖥️  SYSTEM INFORMATION:")
        report.append(f"  OS: {system_info.get('os', 'Unknown')} {system_info.get('version', '')}")
        report.append(f"  Architecture: {system_info.get('architecture', 'Unknown')}")
        report.append(f"  Hostname: {system_info.get('hostname', 'Unknown')}")
        report.append(f"  Platform: {system_info.get('platform', 'Unknown')}")
        
        # Resource Information
        report.append("\n📊 RESOURCE INFORMATION:")
        report.append(f"  RAM: {system_info.get('ram_total_gb', 0):.1f}GB total, "
                     f"{system_info.get('ram_available_gb', 0):.1f}GB available "
                     f"({system_info.get('ram_percent_used', 0):.1f}% used)")
        report.append(f"  CPU: {system_info.get('cpu_cores', 0)} cores @ "
                     f"{system_info.get('cpu_frequency_mhz', 0):.0f}MHz")
        report.append(f"  Disk: {system_info.get('disk_total_gb', 0):.1f}GB total, "
                     f"{system_info.get('disk_free_gb', 0):.1f}GB free "
                     f"({system_info.get('disk_percent_used', 0):.1f}% used)")
        
        
        # Recommendations
        if recommendations:
            report.append("\n🔧 RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                report.append(f"  {i}. {rec}")
        else:
            report.append("\n✅ No recommendations - system looks good!")
        
        report.append("\n" + "="*60)
        
        return "\n".join(report)


def main():
    """Example usage - can be run locally or deployed to LangChain/LangGraph platform"""
    try:
        # Initialize the agent
        agent = OSCheckingAgent()
        
        print("🔍 Starting OS Checking Agent...")
        
        # Run the OS check
        result = agent.run_os_check()
        
        # Format and display the report
        report = agent.format_report(result)
        print(report)
        
        # Save report to file
        with open("os_check_report.json", "w") as f:
            json.dump(result, f, indent=2)
        print("\n💾 Report saved to os_check_report.json")
        
        return result
        
    except Exception as e:
        print(f"❌ Error running OS check: {str(e)}")
        return None


if __name__ == "__main__":
    main()