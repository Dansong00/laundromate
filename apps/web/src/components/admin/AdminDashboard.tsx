import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Badge } from '../ui/badge'
import { Button } from '../ui/button'
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer } from 'recharts'

const revenueData = [
  { name: 'Jan', value: 2500 },
  { name: 'Feb', value: 3200 },
  { name: 'Mar', value: 2800 },
  { name: 'Apr', value: 4200 },
  { name: 'May', value: 3800 },
  { name: 'Jun', value: 5200 },
  { name: 'Jul', value: 4800 },
  { name: 'Aug', value: 5500 }
]

const recentOrders = [
  { id: '#006', customer: 'Emily Doe', service: 'Wash & Fold', status: 'Completed', statusColor: 'bg-green-100 text-green-800' },
  { id: '#007', customer: 'Michael Wilson', service: 'Dry Cleaning', status: 'In Progress', statusColor: 'bg-blue-100 text-blue-800' },
  { id: '#008', customer: 'Jane Doe', service: 'Pressing', status: 'Pending', statusColor: 'bg-yellow-100 text-yellow-800' }
]

export function AdminDashboard() {
  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
        <div className="flex items-center space-x-3">
          <Button variant="outline" size="sm">New</Button>
          <Button className="bg-blue-600 hover:bg-blue-700" size="sm">Dashboard</Button>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Total Orders</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">128</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Service Revenue</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$5,220</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">New Customers</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">32</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Previous Orders</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">5</div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Orders */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Orders</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="grid grid-cols-4 gap-4 text-sm font-medium text-gray-600 pb-2 border-b">
                <span>ID</span>
                <span>Customer</span>
                <span>Service</span>
                <span>Status</span>
              </div>
              {recentOrders.map((order) => (
                <div key={order.id} className="grid grid-cols-4 gap-4 items-center text-sm">
                  <span className="font-medium">{order.id}</span>
                  <span>{order.customer}</span>
                  <span>{order.service}</span>
                  <Badge className={`${order.statusColor} border-0 justify-center`}>
                    {order.status}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Revenue Analytics */}
        <Card>
          <CardHeader>
            <CardTitle>Revenue Analytics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={revenueData}>
                  <XAxis 
                    dataKey="name" 
                    axisLine={false}
                    tickLine={false}
                    className="text-xs"
                  />
                  <YAxis hide />
                  <Bar 
                    dataKey="value" 
                    fill="#3B82F6" 
                    radius={[4, 4, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recently Analytics */}
      <Card>
        <CardHeader>
          <CardTitle>Recently Analytics</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-lg font-semibold">#003</div>
              <div className="text-sm text-gray-600">Service</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-semibold">Wellington</div>
              <div className="text-sm text-gray-600">Hubs</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-semibold">$60.25</div>
              <div className="text-sm text-gray-600">Amount</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Status */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>Status</CardTitle>
          <Button variant="link" className="text-blue-600 p-0">Add Service</Button>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm">Wash & Fold</span>
              <Badge className="bg-green-100 text-green-800 border-0">Delivered</Badge>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm">Ironing</span>
              <Badge className="bg-green-100 text-green-800 border-0">Delivered</Badge>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}