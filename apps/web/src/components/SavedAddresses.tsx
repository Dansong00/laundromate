import { Header } from "./Header";
import { NavigationHeader } from "./NavigationHeader";
import { Button } from "./ui/button";
import { Plus } from "lucide-react";

const addresses = [
  {
    id: 1,
    name: "Dee",
    address: "123 Main St",
    city: "Anytown, NY 12345",
  },
  {
    id: 2,
    name: "",
    address: "456 Elm St",
    city: "Anytown, NY 12345",
  },
];

export function SavedAddresses() {
  return (
    <div className="bg-gray-50 min-h-screen">
      <Header />
      <NavigationHeader title="Saved Addresses" />

      <div className="px-4 py-4">
        <div className="space-y-4 mb-6">
          {addresses.map((address) => (
            <div key={address.id} className="bg-white rounded-lg p-4">
              <div className="flex justify-between items-start mb-2">
                {address.name && (
                  <div className="text-gray-900 mb-1">{address.name}</div>
                )}
                <button className="text-blue-500 text-sm">Edit</button>
              </div>
              <div className="text-gray-900">{address.address}</div>
              <div className="text-gray-500 text-sm">{address.city}</div>
            </div>
          ))}
        </div>

        <Button className="w-full bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-lg">
          <Plus className="w-4 h-4 mr-2" />
          Add Address
        </Button>
      </div>
    </div>
  );
}
