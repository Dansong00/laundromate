import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Badge } from "../ui/badge";
import { Button } from "../ui/button";
import { Input } from "../ui/input";

import { Search, Filter } from "lucide-react";

const orders = [
  {
    id: "#1005",
    customer: "Emily Dorn",
    service: "Wash & Fold",
    status: "Delivered",
    statusColor: "bg-green-100 text-green-800",
  },
  {
    id: "#1006",
    customer: "Michael Wilson",
    service: "Dry Cleaning",
    status: "Delivered",
    statusColor: "bg-green-100 text-green-800",
  },
  {
    id: "#1007",
    customer: "Sarah Lee",
    service: "Pressing",
    status: "Delivered",
    statusColor: "bg-green-100 text-green-800",
  },
  {
    id: "#1008",
    customer: "John Davis",
    service: "Wash & Fold",
    status: "Delivered",
    statusColor: "bg-green-100 text-green-800",
  },
  {
    id: "#1009",
    customer: "Alex Cox",
    service: "Mending",
    status: "In Progress",
    statusColor: "bg-blue-100 text-blue-800",
  },
];

export function AdminServices() {
  const [selectedOrder, setSelectedOrder] = useState(orders[0]);

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Services</h1>
        <Button className="bg-blue-600 hover:bg-blue-700" size="sm">
          Add Service
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Orders List */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Orders</CardTitle>
              <div className="flex items-center space-x-3">
                <div className="relative">
                  <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                  <Input placeholder="Filter" className="pl-9 w-32" />
                </div>
                <Button variant="outline" size="sm">
                  <Filter className="w-4 h-4 mr-2" />
                  Sort by
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="grid grid-cols-4 gap-4 text-sm font-medium text-gray-600 pb-2">
                <span>Order ID</span>
                <span>Customer</span>
                <span>Service</span>
                <span>Status</span>
              </div>

              {orders.map((order) => (
                <div
                  key={order.id}
                  onClick={() => setSelectedOrder(order)}
                  className={`grid grid-cols-4 gap-4 items-center p-3 rounded-lg cursor-pointer transition-colors ${
                    selectedOrder.id === order.id
                      ? "bg-blue-50 border border-blue-200"
                      : "hover:bg-gray-50"
                  }`}
                >
                  <span className="font-medium text-blue-600">{order.id}</span>
                  <span className="text-sm">{order.customer}</span>
                  <span className="text-sm">{order.service}</span>
                  <Badge className={`${order.statusColor} border-0 text-xs`}>
                    {order.status}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Order Details */}
        <Card>
          <CardHeader>
            <CardTitle>Order {selectedOrder.id}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <h3 className="font-medium mb-2">Order Info</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Order ID:</span>
                  <span>{selectedOrder.id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Customer:</span>
                  <span>{selectedOrder.customer}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Service:</span>
                  <span>{selectedOrder.service}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Status:</span>
                  <Badge
                    className={`${selectedOrder.statusColor} border-0 text-xs`}
                  >
                    {selectedOrder.status}
                  </Badge>
                </div>
              </div>
            </div>

            <div>
              <h3 className="font-medium mb-2">Customer</h3>
              <div className="text-sm text-gray-600">
                Contact: 1234-567-8910
              </div>
            </div>

            <div>
              <h3 className="font-medium mb-2">Address</h3>
              <div className="text-sm text-gray-600">56/5612, Southford</div>
            </div>

            <div>
              <h3 className="font-medium mb-2">Email</h3>
              <div className="text-sm text-gray-600">customer@example.com</div>
            </div>

            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span>Wash & Fold</span>
                <span>Total</span>
              </div>
              <div className="flex justify-between items-center">
                <span>Total</span>
                <span className="font-semibold">$50</span>
              </div>
            </div>

            <Button className="w-full bg-blue-600 hover:bg-blue-700">
              Update Order
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
