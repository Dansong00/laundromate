import { Header } from "./Header";
import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";
import { Progress } from "./ui/progress";
import { ChevronRight } from "lucide-react";

interface HomeProps {
  onNewOrder: () => void;
}

export function Home({ onNewOrder }: HomeProps) {
  return (
    <div className="bg-gray-50 min-h-screen">
      <Header />

      <div className="px-6 py-6">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl">LaundroMate</h1>
          <p className="text-lg text-gray-600">Hi Dee</p>
        </div>

        <div className="space-y-4 mb-8">
          <h2 className="text-2xl mb-6">New Order</h2>

          <Button
            onClick={onNewOrder}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white py-4 rounded-2xl"
          >
            New Order
          </Button>

          <Button
            variant="outline"
            className="w-full py-4 rounded-2xl border-gray-300 text-gray-900 hover:bg-gray-50"
          >
            Track Order
          </Button>
        </div>

        <Card className="rounded-2xl border-0 shadow-sm">
          <CardContent className="p-6">
            <h3 className="text-lg mb-4">Active Order</h3>

            <div className="mb-6">
              <h4 className="text-lg mb-1">Wash & Fold</h4>
              <p className="text-gray-500 text-sm">
                Estimated Delivery: Tomorrow, 10:00 AM
              </p>
            </div>

            <div className="mb-4">
              <Progress value={33} className="h-2 mb-3" />
              <div className="flex justify-between text-sm">
                <span className="text-blue-600">In Progress</span>
                <span className="text-gray-400">Out for Delivery</span>
                <span className="text-gray-400">Delivered</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="mt-6 text-center">
          <button className="text-blue-500 flex items-center justify-center space-x-1 mx-auto">
            <span>Past Orders</span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
