"use client";

import { useState } from "react";
import { AdminUsers } from "./AdminUsers";
import { Button } from "../ui/button";
import { Shield, Users, ArrowLeft, LogOut } from "lucide-react";
import { UserRead } from "@/lib/api";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";

interface SuperAdminPortalProps {
  currentUser?: UserRead | null;
}

export function SuperAdminPortal({ currentUser }: SuperAdminPortalProps) {
  const [activeSection, setActiveSection] = useState("users");
  const router = useRouter();
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
    router.push("/auth/login");
  };

  const renderActiveSection = () => {
    switch (activeSection) {
      case "users":
        return <AdminUsers />;
      default:
        return <AdminUsers />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <Shield className="w-8 h-8 text-black" />
              <div>
                <h1 className="text-xl font-semibold text-gray-900">
                  Super Admin Portal
                </h1>
                <p className="text-sm text-gray-500">
                  User Access Provisioning & Management
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              {currentUser && (
                <span className="text-sm text-gray-600">
                  {currentUser.first_name} {currentUser.last_name || ""}
                </span>
              )}
              <Button
                onClick={() => router.push("/admin")}
                variant="outline"
                size="sm"
                className="flex items-center space-x-2"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Admin Portal</span>
              </Button>
              <Button
                onClick={handleLogout}
                variant="outline"
                size="sm"
                className="flex items-center space-x-2"
              >
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className="w-64 bg-white border-r border-gray-200">
          <nav className="p-4 space-y-2">
            <button
              onClick={() => setActiveSection("users")}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left transition-colors ${
                activeSection === "users"
                  ? "bg-black text-white"
                  : "text-gray-700 hover:bg-gray-100"
              }`}
            >
              <Users className="w-5 h-5" />
              <span className="font-medium">User Management</span>
            </button>
          </nav>

          {/* Info Card */}
          <div className="mx-4 mt-8 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <h3 className="text-sm font-semibold text-gray-900 mb-2">
              Super Admin Access
            </h3>
            <p className="text-xs text-gray-600 mb-3">
              You have full access to provision and manage user accounts,
              including admin privileges.
            </p>
            <div className="flex items-center space-x-2 text-xs text-gray-500">
              <Shield className="w-4 h-4" />
              <span>Highest permission level</span>
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6">
          <div className="max-w-7xl mx-auto">{renderActiveSection()}</div>
        </main>
      </div>
    </div>
  );
}
