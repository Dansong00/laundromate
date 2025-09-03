import { Header } from './Header'
import { NavigationHeader } from './NavigationHeader'
import { Switch } from './ui/switch'

export function MyAccount() {
  return (
    <div className="bg-gray-50 min-h-screen">
      <Header />
      <NavigationHeader title="My Account" />
      
      <div className="px-4 py-4">
        <div className="bg-white rounded-lg p-4 mb-4">
          <h3 className="text-gray-900 mb-3">Profile</h3>
          <div className="text-gray-900 mb-1">Dee</div>
          <div className="text-gray-500 text-sm mb-1">dee@example.com</div>
          <div className="text-gray-500 text-sm">123-456-7890</div>
        </div>
        
        <div className="bg-white rounded-lg p-4 mb-4">
          <h3 className="text-gray-900 mb-4">Notifications</h3>
          
          <div className="flex items-center justify-between mb-4">
            <span className="text-gray-900">SMS Notifications</span>
            <Switch defaultChecked />
          </div>
          
          <div className="flex items-center justify-between">
            <span className="text-gray-900">Email Notifications</span>
            <Switch defaultChecked />
          </div>
        </div>
        
        <div className="bg-white rounded-lg p-4 mb-4">
          <h3 className="text-gray-900 mb-3">Security</h3>
          <button className="text-gray-900 text-left w-full">
            Change Password
          </button>
        </div>
        
        {/* Legal Links */}
        <div className="flex items-center justify-center space-x-6 py-4">
          <button className="text-gray-500 text-sm hover:text-gray-700 transition-colors">
            Terms of Service
          </button>
          <button className="text-gray-500 text-sm hover:text-gray-700 transition-colors">
            Privacy Policy
          </button>
        </div>

      </div>
    </div>
  )
}