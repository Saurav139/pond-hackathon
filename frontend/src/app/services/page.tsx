'use client'

import React, { useState } from 'react'
import { Wrench, Lightbulb, Zap, Settings, Package } from 'lucide-react'

export default function ServicesPage() {
  // Recommendations section (from chatbot) - will be populated from URL params or local storage
  const [recommendationsData, setRecommendationsData] = useState<any>(null)
  
  // Load recommendations on component mount
  React.useEffect(() => {
    // Try to get recommendations from URL params or local storage
    const urlParams = new URLSearchParams(window.location.search)
    const recommendationsParam = urlParams.get('recommendations')
    
    if (recommendationsParam) {
      try {
        const recommendations = JSON.parse(decodeURIComponent(recommendationsParam))
        setRecommendationsData(recommendations)
      } catch (e) {
        console.error('Failed to parse recommendations from URL:', e)
      }
    } else {
      // Try local storage as fallback
      const stored = localStorage.getItem('platforge_recommendations')
      if (stored) {
        try {
          const recommendations = JSON.parse(stored)
          setRecommendationsData(recommendations)
        } catch (e) {
          console.error('Failed to parse recommendations from storage:', e)
        }
      }
    }
  }, [])
  
  // Auto-provision section
  const [startupName, setStartupName] = useState('')
  const [founderEmail, setFounderEmail] = useState('')
  const [founderName, setFounderName] = useState('')
  const [provisionLoading, setProvisionLoading] = useState(false)
  const [provisionResult, setProvisionResult] = useState<any>(null)

  const handleAutoProvision = async () => {
    if (!startupName.trim() || !founderEmail.trim() || !founderName.trim()) {
      alert('Please fill in all startup details')
      return
    }

    setProvisionLoading(true)
    setProvisionResult(null)
    
    try {
      console.log('Starting auto-provisioning...', {
        startup_name: startupName,
        founder_email: founderEmail,
        founder_name: founderName
      })
      
      const response = await fetch('http://localhost:8001/auto-provision', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          startup_name: startupName,
          founder_email: founderEmail,
          founder_name: founderName,
          project_name: "platforge_pipeline_project"
        })
      })
      
      if (!response.ok) {
        throw new Error('Auto-provisioning failed')
      }
      
      const result = await response.json()
      setProvisionResult(result)
      
    } catch (error) {
      console.error('Auto-provisioning failed:', error)
      setProvisionResult({
        status: 'error',
        message: error instanceof Error ? error.message : 'Auto-provisioning failed'
      })
    } finally {
      setProvisionLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-black relative overflow-hidden">
      {/* Cyber grid background */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(6,182,212,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(6,182,212,0.1)_1px,transparent_1px)] bg-[size:50px_50px]"></div>
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-cyan-500/5 to-transparent"></div>
      
      {/* Header */}
      <header className="container mx-auto px-6 py-8 relative z-10">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Wrench className="h-8 w-8 text-cyan-400 drop-shadow-[0_0_10px_#06b6d4]" />
            <h1 className="text-3xl font-bold text-white drop-shadow-[0_0_10px_#06b6d4]">PlatForge.ai Services</h1>
          </div>
          <nav className="flex space-x-6">
            <a href="/" className="text-green-400 hover:text-green-300 font-medium border border-green-400/30 px-4 py-2 rounded-lg hover:shadow-[0_0_15px_#4ade80] transition-all">Chat Assistant</a>
          </nav>
        </div>
        <p className="text-green-300 mt-2 drop-shadow-[0_0_5px_#4ade80]">AI-powered platform engineering, simplified</p>
      </header>

      {/* Hero Section */}
      <main className="container mx-auto px-6 py-12 relative z-10">
        <div className="text-center mb-16">
          <h2 className="text-6xl font-bold text-white mb-6 drop-shadow-[0_0_20px_#06b6d4]">
            Build Your Platform
          </h2>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto mb-8">
            Get AI recommendations, auto-provision your infrastructure, configure services, and install packages. 
            All in one streamlined workflow.
          </p>
        </div>

        {/* 4 Section Grid */}
        <div className="grid md:grid-cols-2 gap-8 mb-16">
          
          {/* Section 1: Recommendations */}
          <div className="bg-black/70 backdrop-blur-sm rounded-xl p-6 border border-orange-400/50 hover:border-orange-400/70 hover:shadow-[0_0_30px_#f97316] transition-all flex flex-col">
            <div className="flex items-center space-x-3 mb-4">
              <Lightbulb className="h-8 w-8 text-orange-400 drop-shadow-[0_0_10px_#f97316]" />
              <h3 className="text-xl font-semibold text-white drop-shadow-[0_0_5px_#ffffff]">Recommendations</h3>
              <span className="px-2 py-1 rounded-full text-xs font-medium bg-orange-500/20 text-orange-400 border border-orange-400/30 shadow-[0_0_10px_#f97316]">
                FROM CHATBOT
              </span>
            </div>
            
            <p className="text-gray-300 mb-6">
              Platform recommendations from our AI chatbot. Go back to the chat to modify your requirements.
            </p>
            
            {/* Dynamic recommendations display */}
            <div className="space-y-3 flex-1">
              <div className="bg-orange-500/10 border border-orange-400/30 rounded-lg p-3">
                <h4 className="text-orange-400 font-medium text-sm mb-2">Current Recommendations:</h4>
                {recommendationsData && Array.isArray(recommendationsData) ? (
                  <div className="space-y-1 text-sm text-gray-300">
                    {recommendationsData.map((rec: any, index: number) => (
                      <div key={index} className="flex items-center space-x-2">
                        <span className="w-2 h-2 bg-orange-400 rounded-full"></span>
                        <span>{rec.name} - {rec.description}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="space-y-1 text-sm text-gray-300">
                    <div className="flex items-center space-x-2">
                      <span className="w-2 h-2 bg-gray-400 rounded-full"></span>
                      <span className="text-gray-400">No recommendations loaded yet</span>
                    </div>
                    <p className="text-xs text-gray-500 mt-2">
                      Get recommendations from the chat assistant first, then come back here.
                    </p>
                  </div>
                )}
              </div>
            </div>
            
            <button
              onClick={() => window.open('/', '_blank')}
              className="w-full bg-gradient-to-r from-orange-500 to-red-600 text-white px-6 py-3 rounded-lg font-medium hover:from-orange-400 hover:to-red-500 transition-all shadow-[0_0_20px_#f97316] mt-4"
            >
              💬 Modify in Chat Assistant
            </button>
          </div>

          {/* Section 2: Auto-Provision Infrastructure */}
          <div className="bg-black/70 backdrop-blur-sm rounded-xl p-6 border border-cyan-400/50 hover:border-cyan-400/70 hover:shadow-[0_0_30px_#06b6d4] transition-all">
            <div className="flex items-center space-x-3 mb-4">
              <Zap className="h-8 w-8 text-cyan-400 drop-shadow-[0_0_10px_#06b6d4]" />
              <h3 className="text-xl font-semibold text-white drop-shadow-[0_0_5px_#ffffff]">Auto-Provision Infrastructure</h3>
              <span className="px-2 py-1 rounded-full text-xs font-medium bg-cyan-500/20 text-cyan-400 border border-cyan-400/30 shadow-[0_0_10px_#06b6d4]">
                CLOUD LIVE
              </span>
            </div>
            
            <p className="text-gray-300 mb-6">
              Automatically creates cloud accounts and provisions all recommended services for your startup.
            </p>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Startup Name</label>
                <input
                  type="text"
                  value={startupName}
                  onChange={(e) => setStartupName(e.target.value)}
                  placeholder="My Amazing Startup"
                  className="w-full px-3 py-2 bg-black/50 border border-gray-600/50 rounded-lg text-white placeholder-gray-400 focus:border-cyan-400/50 focus:outline-none"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Founder Email</label>
                <input
                  type="email"
                  value={founderEmail}
                  onChange={(e) => setFounderEmail(e.target.value)}
                  placeholder="founder@startup.com"
                  className="w-full px-3 py-2 bg-black/50 border border-gray-600/50 rounded-lg text-white placeholder-gray-400 focus:border-cyan-400/50 focus:outline-none"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Founder Name</label>
                <input
                  type="text"
                  value={founderName}
                  onChange={(e) => setFounderName(e.target.value)}
                  placeholder="John Smith"
                  className="w-full px-3 py-2 bg-black/50 border border-gray-600/50 rounded-lg text-white placeholder-gray-400 focus:border-cyan-400/50 focus:outline-none"
                />
              </div>
              
              <button
                onClick={handleAutoProvision}
                disabled={provisionLoading}
                className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:from-cyan-400 hover:to-blue-500 transition-all shadow-[0_0_20px_#06b6d4] disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {provisionLoading ? '🔄 Creating Infrastructure...' : '🚀 Auto-Provision Everything'}
              </button>
            </div>
            
            <div className="mt-4 space-y-2 text-sm">
              {provisionResult && provisionResult.status === 'success' && provisionResult.result?.account_info ? (
                <>
                  <div className="flex items-center space-x-2 text-green-400">
                    <div className="h-2 w-2 bg-green-400 rounded-full shadow-[0_0_5px_#4ade80]"></div>
                    <span>✅ Account Created Successfully</span>
                  </div>
                  <div className="ml-4 space-y-1 text-xs">
                    <div className="flex items-center justify-between">
                      <span className="text-gray-400">Account ID:</span>
                      <span className="text-white font-mono">{provisionResult.result.account_info.account_id}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-400">Account Name:</span>
                      <span className="text-white">{provisionResult.result.account_info.account_name}</span>
                    </div>
                    {provisionResult.result.account_info.console_url && (
                      <div className="mt-2">
                        <a 
                          href={provisionResult.result.account_info.console_url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-green-400 hover:text-green-300 underline"
                        >
                          🔗 Open Account Console →
                        </a>
                      </div>
                    )}
                  </div>
                  <div className="flex items-center space-x-2 text-green-400">
                    <div className="h-2 w-2 bg-green-400 rounded-full shadow-[0_0_5px_#4ade80]"></div>
                    <span>Services provisioned successfully</span>
                  </div>
                </>
              ) : (
                <>
                  <div className="flex items-center space-x-2 text-gray-400">
                    <div className="h-2 w-2 bg-green-400 rounded-full shadow-[0_0_5px_#4ade80]"></div>
                    <span>Creates cloud accounts automatically</span>
                  </div>
                  <div className="flex items-center space-x-2 text-gray-400">
                    <div className="h-2 w-2 bg-green-400 rounded-full shadow-[0_0_5px_#4ade80]"></div>
                    <span>Provisions only recommended services</span>
                  </div>
                </>
              )}
            </div>
          </div>

          {/* Section 3: Service Configuration */}
          <div className={`bg-black/70 backdrop-blur-sm rounded-xl p-6 border transition-all ${
            provisionResult && provisionResult.status === 'success' && provisionResult.result?.provisioned_resources 
              ? 'border-blue-400/50 hover:border-blue-400/70 hover:shadow-[0_0_30px_#3b82f6]' 
              : 'border-gray-600/30 opacity-50'
          }`}>
            <div className="flex items-center space-x-3 mb-4">
              <Settings className={`h-8 w-8 ${
                provisionResult && provisionResult.status === 'success' && provisionResult.result?.provisioned_resources
                  ? 'text-blue-400 drop-shadow-[0_0_10px_#3b82f6]'
                  : 'text-gray-500'
              }`} />
              <h3 className={`text-xl font-semibold ${
                provisionResult && provisionResult.status === 'success' && provisionResult.result?.provisioned_resources
                  ? 'text-white drop-shadow-[0_0_5px_#ffffff]'
                  : 'text-gray-400'
              }`}>Service Configuration</h3>
              <span className={`px-2 py-1 rounded-full text-xs font-medium border ${
                provisionResult && provisionResult.status === 'success' && provisionResult.result?.provisioned_resources
                  ? 'bg-blue-500/20 text-blue-400 border-blue-400/30 shadow-[0_0_10px_#3b82f6]'
                  : 'bg-gray-500/20 text-gray-500 border-gray-600/30'
              }`}>
                {provisionResult && provisionResult.status === 'success' && provisionResult.result?.provisioned_resources
                  ? 'CONFIGURED'
                  : 'PENDING'}
              </span>
            </div>
            
            {provisionResult && provisionResult.status === 'success' && provisionResult.result?.provisioned_resources ? (
              <>
                <p className="text-green-300 mb-6">
                  Individual service configurations with connection details and console links.
                </p>
                
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  {provisionResult.result.provisioned_resources.map((resource: any, index: number) => (
                    <div key={index} className="bg-blue-500/10 border border-blue-400/30 rounded-lg p-4">
                      <div className="flex justify-between items-center mb-3">
                        <h4 className="text-blue-400 font-medium">{resource.service}</h4>
                        <div className={`text-sm font-medium px-2 py-1 rounded ${
                          resource.status === 'creating' ? 'text-yellow-400 bg-yellow-500/20' :
                          resource.status === 'available' || resource.status === 'running' ? 'text-green-400 bg-green-500/20' :
                          'text-blue-400 bg-blue-500/20'
                        }`}>
                          {resource.status === 'creating' ? '🔄 Creating' :
                           resource.status === 'available' || resource.status === 'running' ? '✅ Ready' :
                           '⚙️ Configured'}
                        </div>
                      </div>
                      
                      {/* Connection details */}
                      <div className="space-y-2 text-sm">
                        <div className="bg-black/30 p-3 rounded border border-gray-600/30">
                          <p className="text-gray-300 mb-2">Connection Details:</p>
                          <div className="font-mono text-xs space-y-1">
                            {resource.endpoint && <p><span className="text-cyan-400">Endpoint:</span> <span className="text-white">{resource.endpoint}</span></p>}
                            {resource.port && <p><span className="text-cyan-400">Port:</span> <span className="text-white">{resource.port}</span></p>}
                            {resource.database && <p><span className="text-cyan-400">Database:</span> <span className="text-white">{resource.database}</span></p>}
                            {resource.username && <p><span className="text-cyan-400">Username:</span> <span className="text-white">{resource.username}</span></p>}
                            {resource.password && <p><span className="text-cyan-400">Password:</span> <span className="text-white">{resource.password}</span></p>}
                            <p><span className="text-cyan-400">Status:</span> <span className="text-green-400">{resource.status}</span></p>
                          </div>
                          {resource.connection_string && (
                            <div className="mt-2">
                              <p className="text-gray-300 mb-1">Connection String:</p>
                              <div className="bg-black/50 p-2 rounded font-mono text-xs text-blue-300 break-all">
                                {resource.connection_string}
                              </div>
                            </div>
                          )}
                        </div>
                        
                        
                        {resource.console_url && (
                          <div className="bg-black/30 p-3 rounded border border-gray-600/30">
                            <p className="text-gray-300 mb-2">Service Console:</p>
                            <a 
                              href={resource.console_url} 
                              target="_blank" 
                              rel="noopener noreferrer"
                              className="text-blue-400 hover:text-blue-300 underline text-xs"
                            >
                              Open Console →
                            </a>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <div className="text-center py-8">
                <div className="text-gray-500 mb-4">⚙️</div>
                <p className="text-gray-400 mb-2">Service configurations will appear here</p>
                <p className="text-gray-500 text-sm">Complete auto-provisioning first to see individual service configurations like RDS, Redshift, S3, EC2, etc.</p>
              </div>
            )}
          </div>

          {/* Section 4: Packages Install */}
          <div className="bg-black/70 backdrop-blur-sm rounded-xl p-6 border border-purple-400/50 hover:border-purple-400/70 hover:shadow-[0_0_30px_#a855f7] transition-all opacity-60">
            <div className="flex items-center space-x-3 mb-4">
              <Package className="h-8 w-8 text-purple-400 drop-shadow-[0_0_10px_#a855f7]" />
              <h3 className="text-xl font-semibold text-white drop-shadow-[0_0_5px_#ffffff]">Packages Install</h3>
              <span className="px-2 py-1 rounded-full text-xs font-medium bg-purple-500/20 text-purple-400 border border-purple-400/30 shadow-[0_0_10px_#a855f7]">
                COMING SOON
              </span>
            </div>
            
            <p className="text-gray-300 mb-6">
              Automated package installation based on your recommended services. This feature is currently in development.
            </p>
            
            <div className="text-center py-8">
              <div className="text-purple-400 mb-4 text-4xl">📦</div>
              <p className="text-gray-400 mb-2">Package installation coming soon</p>
              <p className="text-gray-500 text-sm">
                This will automatically install Python packages, CLI tools, and dependencies 
                for all your provisioned services.
              </p>
            </div>
          </div>
        </div>

      </main>

      {/* Footer */}
      <footer className="container mx-auto px-6 py-8 mt-16 border-t border-cyan-400/30 relative z-10">
        <div className="text-center text-gray-400">
          <p>&copy; 2024 PlatForge.ai. Building the future of platform engineering.</p>
        </div>
      </footer>
    </div>
  )
}