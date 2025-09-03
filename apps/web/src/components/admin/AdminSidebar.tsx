import { LayoutDashboard, Package, Truck, Users, BarChart3, MapPin } from 'lucide-react'

interface AdminSidebarProps {
  activeSection: string
  setActiveSection: (section: string) => void
}

export function AdminSidebar({ activeSection, setActiveSection }: AdminSidebarProps) {
  const adminMenuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'orders', label: 'Orders', icon: Package },
    { id: 'delivery', label: 'Delivery', icon: Truck },
    { id: 'customers', label: 'Customers', icon: Users }
  ]

  const analyticsMenuItems = [
    { id: 'analytics', label: 'Analytics', icon: BarChart3 }
  ]

  const MenuItem = ({ item, isActive }: { item: any, isActive: boolean }) => {
    const Icon = item.icon
    return (
      <button
        onClick={() => setActiveSection(item.id)}
        className={`w-full flex items-center space-x-3 px-4 py-3 text-left transition-colors ${
          isActive 
            ? 'bg-blue-100 text-blue-700 border-r-2 border-blue-700' 
            : 'text-gray-700 hover:bg-gray-100'
        }`}
      >
        <Icon className="w-5 h-5" />
        <span>{item.label}</span>
      </button>
    )
  }

  return (
    <div className="w-64 bg-white shadow-sm border-r border-gray-200 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <MapPin className="w-4 h-4 text-white" />
          </div>
          <div>
            <div className="font-semibold text-gray-900">Admin</div>
            <div className="text-sm text-gray-500">LaundroMate</div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex-1 py-4">
        {/* Admin Section */}
        <div className="px-4 mb-6">
          <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-3">
            Admin
          </div>
          <div className="space-y-1">
            {adminMenuItems.map((item) => (
              <MenuItem 
                key={item.id} 
                item={item} 
                isActive={activeSection === item.id} 
              />
            ))}
          </div>
        </div>

        {/* Analytics Section */}
        <div className="px-4">
          <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-3">
            Analytics
          </div>
          <div className="space-y-1">
            {analyticsMenuItems.map((item) => (
              <MenuItem 
                key={item.id} 
                item={item} 
                isActive={activeSection === item.id} 
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}