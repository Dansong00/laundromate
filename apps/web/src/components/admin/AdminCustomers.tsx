import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Avatar, AvatarFallback } from "../ui/avatar";
import { Search, Phone, Mail } from "lucide-react";

const customers = [
  {
    id: 1,
    name: "John Doe",
    email: "john@example.com",
    phone: "555-765-5439",
    orders: 24,
    initials: "JD",
  },
  {
    id: 2,
    name: "John Smith",
    email: "john@example.com",
    phone: "555-765-7318",
    orders: 12,
    initials: "JS",
  },
  {
    id: 3,
    name: "Emily Ozown",
    email: "emily@example.com",
    phone: "555-765-7318",
    orders: 8,
    initials: "EO",
  },
  {
    id: 4,
    name: "Michael Wilson",
    email: "michael@example.com",
    phone: "555-765-7318",
    orders: 15,
    initials: "MW",
  },
];

export function AdminCustomers() {
  const [selectedCustomer, setSelectedCustomer] = useState(customers[0]);
  const [searchTerm, setSearchTerm] = useState("");

  const filteredCustomers = customers.filter(
    (customer) =>
      customer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      customer.email.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Customers</h1>
        <div className="flex items-center space-x-3">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <Input
              placeholder="Search"
              className="pl-9 w-64"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <Button className="bg-blue-600 hover:bg-blue-700" size="sm">
            Customer
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Customer List */}
        <Card>
          <CardHeader>
            <CardTitle>All Customers</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="grid grid-cols-4 gap-4 text-sm font-medium text-gray-600 pb-2">
                <span>Name</span>
                <span>Email</span>
                <span>Phone</span>
                <span>Orders</span>
              </div>

              {filteredCustomers.map((customer) => (
                <div
                  key={customer.id}
                  onClick={() => setSelectedCustomer(customer)}
                  className={`grid grid-cols-4 gap-4 items-center p-3 rounded-lg cursor-pointer transition-colors ${
                    selectedCustomer.id === customer.id
                      ? "bg-blue-50 border border-blue-200"
                      : "hover:bg-gray-50"
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <Avatar className="w-8 h-8">
                      <AvatarFallback className="text-xs">
                        {customer.initials}
                      </AvatarFallback>
                    </Avatar>
                    <span className="text-sm font-medium">{customer.name}</span>
                  </div>
                  <span className="text-sm text-gray-600">
                    {customer.email}
                  </span>
                  <span className="text-sm text-gray-600">
                    {customer.phone}
                  </span>
                  <span className="text-sm">{customer.orders}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Customer Details */}
        <Card>
          <CardHeader>
            <CardTitle>{selectedCustomer.name}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-center space-x-4">
              <Avatar className="w-16 h-16">
                <AvatarFallback className="text-lg">
                  {selectedCustomer.initials}
                </AvatarFallback>
              </Avatar>
              <div>
                <h3 className="font-semibold text-lg">
                  {selectedCustomer.name}
                </h3>
                <p className="text-gray-600">Customer Account</p>
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <Phone className="w-4 h-4 text-gray-400" />
                <span className="text-sm">{selectedCustomer.phone}</span>
              </div>
              <div className="flex items-center space-x-3">
                <Mail className="w-4 h-4 text-gray-400" />
                <span className="text-sm">{selectedCustomer.email}</span>
              </div>
            </div>

            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-medium mb-2">Details</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Orders:</span>
                  <span className="font-medium">{selectedCustomer.orders}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Customer Since:</span>
                  <span>Jan 2024</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Status:</span>
                  <span className="text-green-600">Active</span>
                </div>
              </div>
            </div>

            <div className="space-y-3">
              <h4 className="font-medium">Address</h4>
              <div className="text-sm text-gray-600">
                123 Main Street
                <br />
                New York, NY 10001
              </div>
            </div>

            <div className="flex space-x-3">
              <Button className="flex-1 bg-blue-600 hover:bg-blue-700">
                View Orders
              </Button>
              <Button variant="outline" className="flex-1">
                Edit Customer
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
