# PlatForge.ai

🚀 **AI-Powered Cloud Infrastructure Provisioning Platform**

PlatForge.ai automatically creates and configures cloud and related infrastructure for startups in minutes. Just describe your needs, and our AI will provision everything from AWS/GCP accounts to databases, visualization services, and more.

## ✨ Features

- 🤖 **AI-Powered Recommendations**: Smart infrastructure suggestions based on your use case
- 🚀 **Auto-Provisioning**: Creates AWS/GCP accounts and resources automatically  
- ⚙️ **Service Configuration**: Individual service setup with real connection details
- 💾 **Account Persistence**: Remembers existing accounts to avoid duplicates
- 📊 **15+ Supported Services**: AWS, GCP, MongoDB, Tableau, and more


## 🏗️ Architecture

```
PlatForge.ai/
├── backend/          # Python FastAPI + AI provisioning engine
├── frontend/         # Next.js React application
└── README.md         # This file
```

## 🚀 Quick Start

### **1. Backend Setup**
```bash
cd backend
pip install -r requirements.txt

# Configure your AWS/GCP credentials in platforge_secrets.json
python app.py
```
Backend runs on `http://localhost:8001`

### **2. Frontend Setup**  
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:3000`

### **3. Usage Flow**
1. **Chat with AI** → Get infrastructure recommendations
2. **Auto-Provision** → Enter startup details to create cloud accounts  
3. **Configure Services** → Get connection strings and console links
4. **Start Building** → Your infrastructure is ready!

## 🎯 Use Cases

Perfect for startups needing:
- **Data Analytics**: BigQuery + Tableau + Redshift
- **Web Applications**: RDS + EC2 + S3  
- **Mobile Apps**: DynamoDB + Lambda + API Gateway
- **SaaS Platforms**: Multi-service cloud architectures
- **Real-time Apps**: Pub/Sub + Streaming + NoSQL

## 🔧 Supported Services

### Cloud Providers
- **AWS**: RDS, Redshift, EC2, S3, DynamoDB, Lambda, Glue
- **GCP**: BigQuery, Cloud SQL, Compute Engine, Cloud Storage, Firestore

### Third-Party
- **Databases**: MongoDB Atlas, Snowflake
- **Analytics**: Tableau, Power BI, Looker  
- **DevOps**: Docker, Terraform, Airflow

## 💡 How It Works

1. **AI Analysis**: Understands your startup's needs from natural language
2. **Smart Recommendations**: Suggests optimal tech stack from 15+ services
3. **Account Creation**: Creates isolated cloud sub-accounts automatically
4. **Resource Provisioning**: Sets up databases, compute, storage, etc.
5. **Configuration Ready**: Provides connection strings and console access
6. **Persistence**: Remembers everything for future use

## 🔐 Security & Isolation

- Each startup gets **isolated AWS sub-accounts**  
- **Cross-account roles** for secure resource management
- **Credentials management** with proper IAM policies
- **No shared resources** between different startups

## 📊 Database

Uses JSON file-based persistence for development:
- `backend/platforge_accounts.json` - Account database
- `backend/platforge_secrets.json` - Credentials (not in git)

## 🛠️ Development

### **Backend Development**
```bash
cd backend
python app.py              # Start API server
python -m pytest           # Run tests (if available)
```

### **Frontend Development** 
```bash
cd frontend
npm run dev                 # Start dev server
npm run build              # Build for production
npm run type-check         # TypeScript checking
```

## 🎨 UI/UX

- **Cyber Theme**: Dark UI with neon accents and glowing effects
- **4-Section Workflow**: Recommendations → Provision → Configure → Install
- **Real-time Updates**: Live provisioning status and service configuration
- **Responsive Design**: Works on desktop and mobile

## 🔄 Workflow

```mermaid
graph LR
    A[Chat Assistant] --> B[Get Recommendations]
    B --> C[Auto-Provision Account]
    C --> D[Configure Services]
    D --> E[Ready to Build!]
```

## 📈 What's Next

- [ ] Support for more cloud providers (Azure, DigitalOcean)
- [ ] Database migration to PostgreSQL/MongoDB
- [ ] Terraform integration for infrastructure as code
- [ ] Cost optimization recommendations
- [ ] Team collaboration features
- [ ] CI/CD pipeline templates

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)  
5. Open Pull Request


---

**Built for startups, by developers who understand the pain of cloud setup.** 🚀
