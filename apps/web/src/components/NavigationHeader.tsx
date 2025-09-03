import { ChevronLeft, MapPin } from 'lucide-react'

interface NavigationHeaderProps {
  title: string
  showBackButton?: boolean
  onBack?: () => void
}

export function NavigationHeader({ title, showBackButton = true, onBack }: NavigationHeaderProps) {
  return (
    <div className="bg-white px-4 py-4 flex items-center justify-between border-b border-gray-100">
      <div className="flex items-center space-x-3">
        {showBackButton && (
          <button onClick={onBack} className="p-1">
            <ChevronLeft className="w-5 h-5 text-gray-600" />
          </button>
        )}
        <div className="flex items-center space-x-2">
          <div className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
            <MapPin className="w-3 h-3 text-white" />
          </div>
          <span className="text-blue-600 font-medium">LaundroMate</span>
        </div>
      </div>
      
      <h1 className="font-medium text-gray-900">{title}</h1>
      <div className="w-8"></div>
    </div>
  )
}