import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select'
import { Button } from '../ui/button'
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts'

const turnaroundData = [
  { name: 'Mon', value: 12 },
  { name: 'Tue', value: 19 },
  { name: 'Wed', value: 15 },
  { name: 'Thu', value: 25 },
  { name: 'Fri', value: 22 },
  { name: 'Sat', value: 30 },
  { name: 'Sun', value: 18 }
]

const orderStatusData = [
  { name: 'Completed', value: 70, color: '#10B981' },
  { name: 'Pending', value: 24, color: '#F59E0B' },
  { name: 'Cancelled', value: 6, color: '#EF4444' }
]

const monthlyOrdersData = [
  { name: 'Jan', orders: 150 },
  { name: 'Feb', orders: 180 },
  { name: 'Mar', orders: 200 },
  { name: 'Apr', orders: 170 },
  { name: 'May', orders: 220 },
  { name: 'Jun', orders: 350 }
]

export function AdminAnalytics() {
  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Order Analytics</h1>
        <Button className="bg-blue-600 hover:bg-blue-700" size="sm">
          Click Here
        </Button>
      </div>

      {/* Date Range Selectors */}
      <div className="flex items-center space-x-4">
        <Select defaultValue="jan-17-2022">
          <SelectTrigger className="w-40">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="jan-17-2022">Jan 17, 2022</SelectItem>
            <SelectItem value="feb-17-2022">Feb 17, 2022</SelectItem>
            <SelectItem value="mar-17-2022">Mar 17, 2022</SelectItem>
          </SelectContent>
        </Select>
        <span className="text-gray-500">-</span>
        <Select defaultValue="jun-17-2026">
          <SelectTrigger className="w-40">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="jun-17-2026">Jun 17, 2026</SelectItem>
            <SelectItem value="jul-17-2026">Jul 17, 2026</SelectItem>
            <SelectItem value="aug-17-2026">Aug 17, 2026</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Total Orders */}
        <Card>
          <CardHeader>
            <CardTitle>Total Orders</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-3 gap-4 mb-6">
              <div className="text-center">
                <div className="text-2xl font-bold">15.2k</div>
                <div className="text-sm text-gray-600">Total Revenue</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">350</div>
                <div className="text-sm text-gray-600">Orders</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">433</div>
                <div className="text-sm text-gray-600">Average Order Value</div>
              </div>
            </div>
            
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={monthlyOrdersData}>
                  <XAxis 
                    dataKey="name" 
                    axisLine={false}
                    tickLine={false}
                    className="text-xs"
                  />
                  <YAxis hide />
                  <Bar 
                    dataKey="orders" 
                    fill="#3B82F6" 
                    radius={[4, 4, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Orders Status */}
        <Card>
          <CardHeader>
            <CardTitle>Orders Status</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-center mb-6">
              <div className="relative w-48 h-48">
                <PieChart width={192} height={192}>
                  <Pie
                    data={orderStatusData}
                    cx={96}
                    cy={96}
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {orderStatusData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                </PieChart>
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <div className="text-2xl font-bold">100%</div>
                    <div className="text-xs text-gray-600">Total</div>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="space-y-3">
              {orderStatusData.map((item) => (
                <div key={item.name} className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div 
                      className="w-3 h-3 rounded-full" 
                      style={{ backgroundColor: item.color }}
                    />
                    <span className="text-sm">{item.name}</span>
                  </div>
                  <span className="text-sm font-medium">{item.value}%</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Turnaround Time */}
      <Card>
        <CardHeader>
          <CardTitle>Turnaround Time</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={turnaroundData}>
                <XAxis 
                  dataKey="name" 
                  axisLine={false}
                  tickLine={false}
                  className="text-xs"
                />
                <YAxis hide />
                <Line 
                  type="monotone" 
                  dataKey="value" 
                  stroke="#3B82F6" 
                  strokeWidth={2}
                  dot={{ fill: '#3B82F6', strokeWidth: 2, r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}