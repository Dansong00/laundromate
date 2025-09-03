import { useState } from 'react'
import { AdminSidebar } from './AdminSidebar'
import { AdminDashboard } from './AdminDashboard'
import { AdminServices } from './AdminServices'
import { AdminCustomers } from './AdminCustomers'
import { AdminAnalytics } from './AdminAnalytics'
import { Button } from '../ui/button'
import { ArrowLeft } from 'lucide-react'

interface AdminPortalProps {
  onBackToMobile: () => void
}

export function AdminPortal({ onBackToMobile }: AdminPortalProps) {
  const [activeSection, setActiveSection] = useState('dashboard')

  const renderActiveSection = () => {
    switch (activeSection) {
      case 'dashboard':
        return <AdminDashboard />
      case 'orders':
        return <AdminServices />
      case 'customers':
        return <AdminCustomers />
      case 'analytics':
        return <AdminAnalytics />
      default:
        return <AdminDashboard />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Mobile App Button */}
      <div className="fixed top-4 right-4 z-50">
        <Button 
          onClick={onBackToMobile} 
          variant="outline"
          className="flex items-center space-x-2"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Mobile App</span>
        </Button>
      </div>

      <AdminSidebar activeSection={activeSection} setActiveSection={setActiveSection} />
      
      <div className="flex-1 overflow-auto">
        {renderActiveSection()}
      </div>
    </div>
  )
}