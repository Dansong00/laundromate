import { Header } from "./Header";
import { NavigationHeader } from "./NavigationHeader";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";

const orders = [
  {
    id: 1,
    service: "Wash & Fold",
    date: "April 20",
    status: "In Progress",
    statusColor: "bg-blue-100 text-blue-800",
  },
  {
    id: 2,
    service: "Wash & Fold",
    date: "April 20",
    status: "Out for Delivery",
    statusColor: "bg-yellow-100 text-yellow-800",
  },
  {
    id: 3,
    service: "Wash & Fold",
    date: "April 15",
    status: "Delivered",
    statusColor: "bg-green-100 text-green-800",
  },
  {
    id: 4,
    service: "Wash & Fold",
    date: "April 15",
    status: "Delivered",
    statusColor: "bg-green-100 text-green-800",
  },
];

export function MyOrders() {
  return (
    <div className="bg-gray-50 min-h-screen">
      <Header />
      <NavigationHeader title="My Orders" />

      <div className="px-4 py-4">
        <div className="flex items-center justify-between mb-6">
          <Select defaultValue="all">
            <SelectTrigger className="w-20 border-0 bg-transparent text-blue-500">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All</SelectItem>
              <SelectItem value="active">Active</SelectItem>
              <SelectItem value="delivered">Delivered</SelectItem>
            </SelectContent>
          </Select>

          <span className="text-blue-500 text-sm">3</span>
        </div>

        <div className="space-y-3">
          {orders.map((order) => (
            <div
              key={order.id}
              className="bg-white rounded-lg p-4 flex items-center justify-between"
            >
              <div className="flex-1">
                <div className="text-gray-900 mb-1">{order.service}</div>
                <div className="text-gray-900 mb-1">{order.service}</div>
                <div className="text-gray-500 text-sm">{order.date}</div>
              </div>

              <Badge
                className={`${order.statusColor} border-0 px-3 py-1 rounded-full text-xs`}
              >
                {order.status}
              </Badge>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
