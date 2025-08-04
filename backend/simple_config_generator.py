"""
PlatForge.ai Simple Configuration Generator
Zero-config approach - minimal user input, maximum working configs
"""

import os
import json
from typing import Dict, List, Any
from pathlib import Path

class SimpleConfigGenerator:
    def __init__(self, project_name: str = "platforge_project"):
        self.project_name = project_name
        self.project_dir = Path.home() / "platforge_projects" / project_name
        self.config_dir = self.project_dir / "config"
        
    def generate_ready_to_use_configs(self, project_display_name: str, installed_tools: List[str], include_cloud: bool = False) -> Dict[str, Any]:
        """Generate immediately usable configurations with zero additional setup needed"""
        
        # Create config directory
        self.config_dir.mkdir(exist_ok=True)
        
        # Sanitize project name for use in configs
        safe_project_name = project_display_name.lower().replace(' ', '-').replace('_', '-')
        
        generated_files = {}
        
        # Generate configurations that work out of the box
        generated_files['docker_compose'] = self._create_docker_compose(safe_project_name, installed_tools)
        generated_files['env_file'] = self._create_env_file(safe_project_name, installed_tools, include_cloud)
        generated_files['app_starter'] = self._create_app_starter(safe_project_name, installed_tools)
        generated_files['quick_start'] = self._create_quick_start_guide(safe_project_name, installed_tools)
        
        if include_cloud:
            generated_files['cloud_template'] = self._create_cloud_template(safe_project_name, installed_tools)
        
        return {
            "status": "success",
            "message": f"Ready-to-use configuration generated for '{project_display_name}'",
            "config_directory": str(self.config_dir),
            "safe_project_name": safe_project_name,
            "generated_files": generated_files,
            "next_steps": [
                "Run: cd " + str(self.config_dir),
                "Run: docker-compose up -d",
                "Run: python app.py",
                "Open: http://localhost:3001 (if Metabase installed)"
            ]
        }
    
    def _create_docker_compose(self, project_name: str, installed_tools: List[str]) -> str:
        """Create docker-compose.yml with working local services"""
        
        compose_content = [
            "# PlatForge.ai Generated Docker Compose",
            "# Ready to run: docker-compose up -d",
            "",
            "version: '3.8'",
            "services:",
            ""
        ]
        
        # PostgreSQL database (if postgres tools installed)
        if any(tool in installed_tools for tool in ['psycopg2-binary', 'postgres']):
            compose_content.extend([
                "  database:",
                "    image: postgres:13",
                "    container_name: " + f"{project_name}-db",
                "    environment:",
                "      POSTGRES_DB: " + f"{project_name.replace('-', '_')}_db",
                "      POSTGRES_USER: admin",
                "      POSTGRES_PASSWORD: dev123",
                "    ports:",
                "      - \"5432:5432\"",
                "    volumes:",
                "      - db_data:/var/lib/postgresql/data",
                "    healthcheck:",
                "      test: [\"CMD-SHELL\", \"pg_isready -U admin\"]",
                "      interval: 10s",
                "      timeout: 5s",
                "      retries: 5",
                ""
            ])
        
        # Redis cache
        if any(tool in installed_tools for tool in ['redis']):
            compose_content.extend([
                "  cache:",
                "    image: redis:alpine",
                "    container_name: " + f"{project_name}-cache",
                "    ports:",
                "      - \"6379:6379\"",
                ""
            ])
        
        # MongoDB
        if any(tool in installed_tools for tool in ['pymongo', 'mongodb']):
            compose_content.extend([
                "  mongodb:",
                "    image: mongo:5",
                "    container_name: " + f"{project_name}-mongo",
                "    ports:",
                "      - \"27017:27017\"",
                "    volumes:",
                "      - mongo_data:/data/db",
                ""
            ])
        
        # Metabase (if analytics tools)
        if any(tool in installed_tools for tool in ['metabase', 'tableau']):
            compose_content.extend([
                "  dashboard:",
                "    image: metabase/metabase:latest",
                "    container_name: " + f"{project_name}-dashboard",
                "    ports:",
                "      - \"3001:3000\"",
                "    environment:",
                "      MB_DB_TYPE: postgres",
                "      MB_DB_DBNAME: " + f"{project_name.replace('-', '_')}_db",
                "      MB_DB_PORT: 5432",
                "      MB_DB_USER: admin",
                "      MB_DB_PASS: dev123",
                "      MB_DB_HOST: database",
                "    depends_on:",
                "      database:",
                "        condition: service_healthy",
                ""
            ])
        
        # Volumes section
        volumes = []
        if any(tool in installed_tools for tool in ['psycopg2-binary', 'postgres']):
            volumes.append("  db_data:")
        if any(tool in installed_tools for tool in ['pymongo', 'mongodb']):
            volumes.append("  mongo_data:")
        
        if volumes:
            compose_content.extend(["volumes:"] + volumes)
        
        # Write file
        compose_file = self.config_dir / "docker-compose.yml"
        with open(compose_file, 'w') as f:
            f.write('\n'.join(compose_content))
        
        return str(compose_file)
    
    def _create_env_file(self, project_name: str, installed_tools: List[str], include_cloud: bool) -> str:
        """Create .env with working defaults"""
        
        env_content = [
            "# PlatForge.ai Generated Environment Variables",
            "# Ready to use - no changes needed for local development",
            "",
            f"PROJECT_NAME={project_name}",
            "ENVIRONMENT=development",
            "DEBUG=true",
            ""
        ]
        
        # Database config
        if any(tool in installed_tools for tool in ['psycopg2-binary', 'postgres']):
            db_name = f"{project_name.replace('-', '_')}_db"
            env_content.extend([
                "# Database (ready to use locally)",
                f"DATABASE_URL=postgresql://admin:dev123@localhost:5432/{db_name}",
                "DB_HOST=localhost",
                "DB_PORT=5432",
                f"DB_NAME={db_name}",
                "DB_USER=admin",
                "DB_PASSWORD=dev123",
                ""
            ])
        
        # Redis
        if any(tool in installed_tools for tool in ['redis']):
            env_content.extend([
                "# Cache (ready to use locally)",
                "REDIS_URL=redis://localhost:6379",
                ""
            ])
        
        # MongoDB
        if any(tool in installed_tools for tool in ['pymongo', 'mongodb']):
            env_content.extend([
                "# MongoDB (ready to use locally)",
                "MONGODB_URL=mongodb://localhost:27017",
                f"MONGODB_DATABASE={project_name.replace('-', '_')}_db",
                ""
            ])
        
        # Application settings
        env_content.extend([
            "# Application Settings",
            "SECRET_KEY=dev-secret-key-change-in-production",
            "PORT=8000",
            ""
        ])
        
        # Cloud settings (empty for later)
        if include_cloud:
            if any(tool in installed_tools for tool in ['google-cloud-compute', 'google-cloud-bigquery']):
                env_content.extend([
                    "# Google Cloud (fill when ready to deploy)",
                    "GOOGLE_CLOUD_PROJECT=",
                    "GOOGLE_APPLICATION_CREDENTIALS=",
                    ""
                ])
            
            if any(tool in installed_tools for tool in ['boto3', 'awscli']):
                env_content.extend([
                    "# AWS (fill when ready to deploy)", 
                    "AWS_REGION=us-east-1",
                    "AWS_ACCESS_KEY_ID=",
                    "AWS_SECRET_ACCESS_KEY=",
                    ""
                ])
        
        # Write file
        env_file = self.config_dir / ".env"
        with open(env_file, 'w') as f:
            f.write('\n'.join(env_content))
        
        return str(env_file)
    
    def _create_app_starter(self, project_name: str, installed_tools: List[str]) -> str:
        """Create working starter application"""
        
        app_content = [
            f'"""',
            f'{project_name.title()} - Starter Application',
            'Generated by PlatForge.ai - Ready to customize!',
            '"""',
            "",
            "import os",
            "from dotenv import load_dotenv",
            "",
            "# Load environment variables",
            "load_dotenv()",
            "",
            "def main():",
            f'    print("🚀 Starting {project_name.title()}...")',
            f'    print("📁 Project: {project_name}")',
            '    print("🌍 Environment:", os.getenv("ENVIRONMENT", "development"))',
            '    print("")',
            ""
        ]
        
        # Database connection example
        if any(tool in installed_tools for tool in ['psycopg2-binary']):
            app_content.extend([
                "    # Database connection test",
                "    try:",
                "        import psycopg2",
                "        conn = psycopg2.connect(os.getenv('DATABASE_URL'))",
                "        cur = conn.cursor()",
                "        cur.execute('SELECT version();')",
                "        version = cur.fetchone()[0]",
                "        print('✅ Database connected:', version.split()[0:2])",
                "        cur.close()",
                "        conn.close()",
                "    except Exception as e:",
                "        print('❌ Database connection failed:', e)",
                "        print('💡 Make sure to run: docker-compose up -d')",
                "    print()",
                ""
            ])
        
        # Google Cloud test
        if any(tool in installed_tools for tool in ['google-cloud-compute']):
            app_content.extend([
                "    # Google Cloud test (will work when credentials are set)",
                "    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')",
                "    if project_id:",
                "        try:",
                "            from google.cloud import compute_v1",
                "            print('✅ Google Cloud SDK ready for project:', project_id)",
                "        except Exception as e:",
                "            print('⚠️  Google Cloud setup needed:', e)",
                "    else:",
                "        print('💡 Google Cloud: Add GOOGLE_CLOUD_PROJECT to .env when ready')",
                "    print()",
                ""
            ])
        
        # Success message
        app_content.extend([
            '    print("🎉 Your platform is running!")',
            '    print("📝 Next steps:")',
            '    print("   1. Customize this app.py file")',
            '    print("   2. Add your business logic")',
        ])
        
        if any(tool in installed_tools for tool in ['metabase']):
            app_content.append('    print("   3. Open dashboard at: http://localhost:3001")')
        
        app_content.extend([
            '    print("   4. Deploy to cloud when ready!")',
            "",
            "if __name__ == '__main__':",
            "    main()"
        ])
        
        # Write file
        app_file = self.config_dir / "app.py"
        with open(app_file, 'w') as f:
            f.write('\n'.join(app_content))
        
        return str(app_file)
    
    def _create_quick_start_guide(self, project_name: str, installed_tools: List[str]) -> str:
        """Create simple getting started guide"""
        
        guide_content = [
            f"# {project_name.title()} - Quick Start",
            "",
            "Your platform is ready! Follow these 3 simple steps:",
            "",
            "## 1️⃣ Start Your Services",
            "```bash",
            "docker-compose up -d",
            "```",
            "",
            "## 2️⃣ Run Your App",
            "```bash",
            "python app.py",
            "```",
            "",
            "## 3️⃣ Access Your Platform",
        ]
        
        if any(tool in installed_tools for tool in ['metabase']):
            guide_content.extend([
                "- **Analytics Dashboard**: http://localhost:3001",
                "- **Database**: localhost:5432 (admin/dev123)",
            ])
        else:
            guide_content.append("- **Database**: localhost:5432 (admin/dev123)")
        
        guide_content.extend([
            "",
            "## 🎨 Customize Your App",
            "",
            "1. Edit `app.py` - Add your business logic",
            "2. Modify `docker-compose.yml` - Add more services",
            "3. Update `.env` - Configure for production",
            "",
            "## 🚀 Deploy to Cloud",
            "",
            "When you're ready to go live:",
            "1. Update `.env` with your cloud credentials",
            "2. Use the cloud template files",
            "3. Deploy with one command!",
            "",
            "---",
            "*Generated by PlatForge.ai - AI-powered platform engineering*"
        ])
        
        # Write file
        guide_file = self.config_dir / "QUICK_START.md"
        with open(guide_file, 'w') as f:
            f.write('\n'.join(guide_content))
        
        return str(guide_file)
    
    def _create_cloud_template(self, project_name: str, installed_tools: List[str]) -> str:
        """Create cloud deployment template (only if requested)"""
        
        # Simple cloud template - user fills in when ready
        cloud_content = [
            f"# {project_name.title()} - Cloud Deployment",
            "",
            "## When You're Ready to Deploy...",
            "",
            "1. **Choose your cloud provider**",
            "2. **Update .env with your credentials**",
            "3. **Run deployment commands**",
            "",
            "### Google Cloud",
            "```bash",
            "# Set your project",
            "export GOOGLE_CLOUD_PROJECT=your-project-id",
            "",
            "# Deploy database",
            "gcloud sql instances create " + f"{project_name}-db --database-version=POSTGRES_13",
            "```",
            "",
            "### AWS",
            "```bash", 
            "# Deploy with Terraform (coming soon)",
            "terraform init",
            "terraform plan",
            "terraform apply",
            "```"
        ]
        
        # Write file
        cloud_file = self.config_dir / "CLOUD_DEPLOYMENT.md"
        with open(cloud_file, 'w') as f:
            f.write('\n'.join(cloud_content))
        
        return str(cloud_file)


if __name__ == "__main__":
    # Test the simple config generator
    generator = SimpleConfigGenerator("test_project")
    
    test_tools = ["psycopg2-binary", "docker", "metabase"]
    
    result = generator.generate_ready_to_use_configs(
        project_display_name="My Startup App",
        installed_tools=test_tools,
        include_cloud=False
    )
    
    print(json.dumps(result, indent=2))