'use client'

import { useState } from 'react'
import Link from 'next/link'
import { MessageSquare, Zap, Workflow, CheckCircle } from 'lucide-react'

interface Recommendation {
  name: string;
  category: string;
  description: string;
  packages?: string[];
}

interface Message {
  type: 'bot' | 'user';
  content: string;
  recommendations?: Recommendation[] | null;
}

export default function ChatAssistant() {
  const [messages, setMessages] = useState<Message[]>([
    {
      type: 'bot',
      content: "Hello! I'm your PlatForge.ai assistant. I'll help you design the perfect platform architecture for your project. What are you looking to build?",
      recommendations: null
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [showRecommendationForm, setShowRecommendationForm] = useState(false)

  const getRecommendations = async (useCase: string, companyStage: string, cloudPreference: string) => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';
      const response = await fetch(`${apiUrl}/recommendations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          use_case: useCase,
          company_stage: companyStage,
          cloud_preference: cloudPreference
        })
      })
      
      if (!response.ok) {
        throw new Error('Failed to get recommendations')
      }
      
      const data = await response.json()
      return data.recommendations
    } catch (error) {
      console.error('Failed to get recommendations:', error)
      return null
    }
  }

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return
    
    const newMessage: Message = { type: 'user', content: inputValue }
    setMessages(prev => [...prev, newMessage])
    const userInput = inputValue
    setInputValue('')
    setIsTyping(true)
    
    // Simple keyword-based recommendation logic
    let useCase = 'startup_mvp'
    let companyStage = 'startup'
    let cloudPreference = 'any'
    
    const input = userInput.toLowerCase()
    
    // Detect use case from user input
    if (input.includes('saas') || input.includes('platform')) {
      useCase = 'saas_platform'
    } else if (input.includes('ecommerce') || input.includes('shop') || input.includes('store')) {
      useCase = 'ecommerce'
    } else if (input.includes('data') || input.includes('analytics') || input.includes('warehouse')) {
      useCase = 'data_analytics'
    } else if (input.includes('real-time') || input.includes('realtime') || input.includes('streaming')) {
      useCase = 'real_time_app'
    } else if (input.includes('mobile') || input.includes('app')) {
      useCase = 'mobile_backend'
    } else if (input.includes('enterprise')) {
      useCase = 'enterprise_data'
      companyStage = 'enterprise'
    } else if (input.includes('machine learning') || input.includes('ml') || input.includes('ai')) {
      useCase = 'ml_platform'
    }
    
    // Detect cloud preference
    if (input.includes('aws') || input.includes('amazon')) {
      cloudPreference = 'aws'
    } else if (input.includes('gcp') || input.includes('google')) {
      cloudPreference = 'gcp'
    }
    
    // Detect company stage
    if (input.includes('enterprise') || input.includes('large company')) {
      companyStage = 'enterprise'
    }
    
    // Get recommendations
    const recommendations = await getRecommendations(useCase, companyStage, cloudPreference)
    
    setTimeout(() => {
      const botResponse: Message = {
        type: 'bot',
        content: recommendations 
          ? `Based on your requirements, I've identified this as a ${useCase.replace('_', ' ')} use case. Here are my platform recommendations for a ${companyStage} company:` 
          : "I understand you're looking to build that platform. Let me provide some general recommendations.",
        recommendations: recommendations
      }
      setMessages(prev => [...prev, botResponse])
      setIsTyping(false)
    }, 2000)
  }

  const handleRecommendationRequest = () => {
    setShowRecommendationForm(true)
  }

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const formData = new FormData(e.target as HTMLFormElement)
    const useCase = formData.get('useCase') as string
    const companyStage = formData.get('companyStage') as string
    const cloudPreference = formData.get('cloudPreference') as string
    
    setShowRecommendationForm(false)
    setIsTyping(true)
    
    const recommendations = await getRecommendations(useCase, companyStage, cloudPreference)
    
    setTimeout(() => {
      const botResponse: Message = {
        type: 'bot',
        content: `Here are my platform recommendations for your ${useCase.replace('_', ' ')} project:`,
        recommendations: recommendations
      }
      setMessages(prev => [...prev, botResponse])
      setIsTyping(false)
    }, 1500)
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
            <MessageSquare className="h-8 w-8 text-cyan-400 drop-shadow-[0_0_10px_#06b6d4]" />
            <h1 className="text-3xl font-bold text-white drop-shadow-[0_0_10px_#06b6d4]">PlatForge.ai</h1>
          </div>
          <nav className="flex space-x-6">
            <Link href="/services" className="text-green-400 hover:text-green-300 font-medium border border-green-400/30 px-4 py-2 rounded-lg hover:shadow-[0_0_15px_#4ade80] transition-all">Services</Link>
          </nav>
        </div>
        <p className="text-green-300 mt-2 drop-shadow-[0_0_5px_#4ade80]">AI-powered platform design and deployment</p>
      </header>

      <main className="container mx-auto px-6 py-8 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Chat Interface */}
          <div className="lg:col-span-2">
            <div className="bg-black/70 backdrop-blur-sm rounded-xl border border-cyan-400/30 shadow-[0_0_30px_#06b6d4] h-[600px] flex flex-col">
              {/* Chat Header */}
              <div className="p-6 border-b border-cyan-400/30">
                <h2 className="text-xl font-bold text-white drop-shadow-[0_0_5px_#ffffff]">Platform Design Assistant</h2>
                <p className="text-green-300 text-sm mt-1">Powered by AI • Currently in development</p>
              </div>

              {/* Messages Area */}
              <div className="flex-1 p-6 overflow-y-auto space-y-4">
                {messages.map((message, index) => (
                  <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[90%] p-4 rounded-lg ${
                      message.type === 'user' 
                        ? 'bg-cyan-500/20 border border-cyan-400/50 text-white' 
                        : 'bg-green-500/20 border border-green-400/50 text-green-100'
                    }`}>
                      <p className="mb-2">{message.content}</p>
                      {message.recommendations && (
                        <div className="mt-4 space-y-3">
                          <h4 className="text-green-400 font-medium text-sm">Recommended Platform Tools:</h4>
                          <div className="grid gap-3">
                            {message.recommendations.map((rec: Recommendation, recIndex: number) => (
                              <div key={recIndex} className="bg-black/30 p-3 rounded-lg border border-green-400/30">
                                <div className="flex justify-between items-start mb-2">
                                  <h5 className="text-cyan-400 font-medium text-sm">{rec.name}</h5>
                                  <span className="text-xs px-2 py-1 bg-green-500/20 text-green-400 rounded">
                                    {rec.category}
                                  </span>
                                </div>
                                <p className="text-green-300 text-xs mb-2">{rec.description}</p>
                                <div className="flex flex-wrap gap-1">
                                  {rec.packages?.slice(0, 3).map((pkg: string, pkgIndex: number) => (
                                    <span key={pkgIndex} className="text-xs px-2 py-1 bg-cyan-500/20 text-cyan-400 rounded">
                                      {pkg}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            ))}
                          </div>
                          <div className="mt-4 flex gap-2">
                            <button 
                              onClick={() => {
                                // Store recommendations in localStorage and navigate to services
                                localStorage.setItem('platforge_recommendations', JSON.stringify(message.recommendations))
                                window.location.href = '/services'
                              }}
                              className="bg-green-500/20 hover:bg-green-500/30 text-green-400 px-3 py-1 rounded text-xs border border-green-400/30 hover:shadow-[0_0_10px_#4ade80] transition-all"
                            >
                              ✓ Confirm & Proceed to Setup
                            </button>
                            <button 
                              onClick={() => {
                                const botResponse: Message = {
                                  type: 'bot',
                                  content: "I'd be happy to provide different recommendations! Please describe what you're looking for or use the form below to get more specific suggestions.",
                                  recommendations: null
                                }
                                setMessages(prev => [...prev, botResponse])
                                setShowRecommendationForm(true)
                              }}
                              className="bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-400 px-3 py-1 rounded text-xs border border-cyan-400/30 hover:shadow-[0_0_10px_#06b6d4] transition-all"
                            >
                              Get Different Recommendations
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                {isTyping && (
                  <div className="flex justify-start">
                    <div className="bg-green-500/20 border border-green-400/50 text-green-100 p-4 rounded-lg">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-green-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-green-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                        <div className="w-2 h-2 bg-green-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Input Area */}
              <div className="p-6 border-t border-cyan-400/30">
                {showRecommendationForm ? (
                  <form onSubmit={handleFormSubmit} className="space-y-4">
                    <div className="grid grid-cols-3 gap-4">
                      <select name="useCase" className="bg-black/50 border border-cyan-400/30 rounded-lg px-3 py-2 text-white text-sm">
                        <option value="startup_mvp">Startup MVP</option>
                        <option value="saas_platform">SaaS Platform</option>
                        <option value="ecommerce">E-commerce</option>
                        <option value="data_analytics">Data Analytics</option>
                        <option value="real_time_app">Real-time App</option>
                        <option value="mobile_backend">Mobile Backend</option>
                        <option value="enterprise_data">Enterprise Data</option>
                        <option value="ml_platform">ML Platform</option>
                      </select>
                      <select name="companyStage" className="bg-black/50 border border-cyan-400/30 rounded-lg px-3 py-2 text-white text-sm">
                        <option value="startup">Startup</option>
                        <option value="enterprise">Enterprise</option>
                      </select>
                      <select name="cloudPreference" className="bg-black/50 border border-cyan-400/30 rounded-lg px-3 py-2 text-white text-sm">
                        <option value="any">Any Cloud</option>
                        <option value="aws">AWS</option>
                        <option value="gcp">Google Cloud</option>
                      </select>
                    </div>
                    <div className="flex gap-2">
                      <button
                        type="submit"
                        className="bg-green-500 hover:bg-green-400 text-black font-bold px-4 py-2 rounded-lg border border-green-400/50 hover:shadow-[0_0_20px_#4ade80] transition-all"
                      >
                        Get Recommendations
                      </button>
                      <button
                        type="button"
                        onClick={() => setShowRecommendationForm(false)}
                        className="bg-gray-600 hover:bg-gray-500 text-white font-bold px-4 py-2 rounded-lg border border-gray-500/50 transition-all"
                      >
                        Cancel
                      </button>
                    </div>
                  </form>
                ) : (
                  <div className="space-y-3">
                    <div className="flex space-x-2">
                      <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                        placeholder="Describe your platform needs... (e.g., 'I need a data analytics platform with AWS')"
                        className="flex-1 bg-black/50 border border-cyan-400/30 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:border-cyan-400/50 focus:outline-none focus:shadow-[0_0_15px_#06b6d4]"
                      />
                      <button
                        onClick={handleSendMessage}
                        disabled={!inputValue.trim() || isTyping}
                        className="bg-cyan-500 hover:bg-cyan-400 disabled:bg-cyan-500/30 text-black font-bold px-6 py-3 rounded-lg border border-cyan-400/50 hover:shadow-[0_0_20px_#06b6d4] transition-all"
                      >
                        Send
                      </button>
                    </div>
                    <div className="text-center">
                      <button
                        onClick={handleRecommendationRequest}
                        className="text-green-400 hover:text-green-300 text-sm font-medium border border-green-400/30 px-4 py-2 rounded-lg hover:shadow-[0_0_15px_#4ade80] transition-all"
                      >
                        Or get specific recommendations →
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Info Panel */}
          <div className="space-y-6">
            {/* What This Does */}
            <div className="bg-black/70 backdrop-blur-sm rounded-xl p-6 border border-green-400/30 shadow-[0_0_20px_#4ade80]">
              <h3 className="text-xl font-bold text-white mb-4 drop-shadow-[0_0_5px_#ffffff]">How It Works</h3>
              <div className="space-y-3">
                <div className="flex items-start space-x-3">
                  <MessageSquare className="w-5 h-5 text-green-400 mt-0.5 drop-shadow-[0_0_5px_#4ade80]" />
                  <p className="text-green-300 text-sm">Tell me about your project requirements</p>
                </div>
                <div className="flex items-start space-x-3">
                  <Zap className="w-5 h-5 text-cyan-400 mt-0.5 drop-shadow-[0_0_5px_#06b6d4]" />
                  <p className="text-green-300 text-sm">AI analyzes and suggests optimal infrastructure</p>
                </div>
                <div className="flex items-start space-x-3">
                  <Workflow className="w-5 h-5 text-green-400 mt-0.5 drop-shadow-[0_0_5px_#4ade80]" />
                  <p className="text-green-300 text-sm">Generate complete infrastructure flow diagram</p>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircle className="w-5 h-5 text-cyan-400 mt-0.5 drop-shadow-[0_0_5px_#06b6d4]" />
                  <p className="text-green-300 text-sm">Approve and move to installation phase</p>
                </div>
              </div>
            </div>

            {/* Example Flows */}
            <div className="bg-black/70 backdrop-blur-sm rounded-xl p-6 border border-cyan-400/30">
              <h3 className="text-xl font-bold text-white mb-4 drop-shadow-[0_0_5px_#ffffff]">Example Flows</h3>
              <div className="space-y-3">
                <div className="p-3 bg-green-500/10 border border-green-400/30 rounded-lg">
                  <p className="text-green-400 font-medium text-sm">Data Pipeline</p>
                  <p className="text-green-300 text-xs">AWS Lambda → Redshift → Tableau</p>
                </div>
                <div className="p-3 bg-cyan-500/10 border border-cyan-400/30 rounded-lg">
                  <p className="text-cyan-400 font-medium text-sm">Web Application</p>
                  <p className="text-green-300 text-xs">React → API Gateway → DynamoDB</p>
                </div>
                <div className="p-3 bg-green-500/10 border border-green-400/30 rounded-lg">
                  <p className="text-green-400 font-medium text-sm">ML Pipeline</p>
                  <p className="text-green-300 text-xs">S3 → SageMaker → API Endpoint</p>
                </div>
              </div>
            </div>

          </div>
        </div>
      </main>
    </div>
  )
}