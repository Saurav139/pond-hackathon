# PlatForge.ai Frontend

Modern React/Next.js frontend for AI-powered cloud infrastructure provisioning.

## Features

- 🤖 **AI Chat Assistant**: Interactive chatbot for infrastructure recommendations
- 🚀 **4-Section Workflow**: Streamlined provisioning process
- ⚙️ **Service Configuration**: Real-time service setup and connection details
- 📱 **Responsive Design**: Works on desktop and mobile
- 🎨 **Cyber Theme**: Modern dark UI with glowing effects

## Quick Start

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm run dev
   ```

   Frontend runs on `http://localhost:3000`

3. **Build for Production**:
   ```bash
   npm run build
   npm start
   ```

## Pages & Components

### **Main Pages**
- **`/`** - Chat Assistant (Home page)
- **`/services`** - 4-Section Services Workflow

### **4-Section Workflow**

1. **📋 Recommendations** 
   - Displays AI recommendations from chatbot
   - Button to modify recommendations

2. **🚀 Auto-Provision Infrastructure**
   - Input: Startup name, founder email, founder name  
   - Creates cloud accounts automatically
   - Shows account details after provisioning

3. **⚙️ Service Configuration**
   - Individual service setup (RDS, EC2, S3, etc.)
   - Connection strings and console links
   - Real-time status updates

4. **📦 Packages Install** 
   - Coming soon feature
   - Automated package installation

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **State**: React Hooks (useState, useEffect)

## Architecture

```
Frontend/
├── src/
│   └── app/
│       ├── page.tsx              # Chat assistant (home)
│       ├── services/
│       │   └── page.tsx          # 4-section workflow
│       ├── layout.tsx            # Root layout
│       └── globals.css           # Global styles
├── public/                       # Static assets
├── package.json                  # Dependencies
└── tailwind.config.ts           # Tailwind configuration
```

## Key Features

### **Dynamic Recommendations**
- Loads recommendations from localStorage or URL params
- Syncs with backend API recommendations
- Button to return to chat for modifications

### **Real-time Provisioning**
- Shows provisioning status in real-time
- Account creation with console links
- Service-by-service configuration display

### **Responsive Design**
- 2x2 grid layout on desktop
- Stacked layout on mobile
- Cyber-themed with glowing effects

### **Data Persistence**
- Recommendations stored in localStorage
- Account information persisted across sessions
- Service configuration details saved

## API Integration

Connects to backend at `http://localhost:8001`:
- `POST /auto-provision` - Create infrastructure
- `POST /recommendations` - Get AI recommendations
- Service-specific endpoints for configuration

## Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Type checking
npm run type-check

# Build production
npm run build
```
