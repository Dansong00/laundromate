"use client";

import { useAuth } from "@/components/AuthProvider";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { isAdminUser } from "@/lib/api";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, CheckCircle2, LayoutDashboard, ShoppingBag, Store, Truck, Users } from "lucide-react";
import { Footer } from "@/components/Footer";

export default function Home() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated) {
      const checkUserRole = async () => {
        try {
          const res = await fetch("/api/me", {
            headers: {
              Authorization: `Bearer ${sessionStorage.getItem("access_token")}`,
            },
          });

          if (res.ok) {
            const user = await res.json();
            const isAdmin = isAdminUser(user);

            if (isAdmin) {
              router.replace("/admin");
            } else {
              router.replace("/portal");
            }
          } else {
            router.replace("/portal");
          }
        } catch (error) {
          console.error("Error checking user role:", error);
          router.replace("/portal");
        }
      };

      checkUserRole();
    }
  }, [isAuthenticated, router]);

  if (isAuthenticated) {
    return null;
  }

  return (
    <div className="flex min-h-screen flex-col bg-white">
      {/* Navigation */}
      <header className="sticky top-0 z-50 w-full border-b bg-white/80 backdrop-blur-md">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
          <div className="flex items-center gap-2 font-bold text-xl tracking-tight">
            <span className="text-blue-600">Laundro</span>Mate
          </div>
          <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-gray-600">
            <Link href="#features" className="hover:text-blue-600 transition-colors">Features</Link>
            <Link href="#how-it-works" className="hover:text-blue-600 transition-colors">How it Works</Link>
            <Link href="#portals" className="hover:text-blue-600 transition-colors">Portals</Link>
          </nav>
          <div className="flex items-center gap-4">
            <Link href="/auth/login">
              <Button variant="ghost" size="sm">Log in</Button>
            </Link>
            <Link href="/auth/register">
              <Button size="sm" className="bg-blue-600 hover:bg-blue-700 text-white">Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative overflow-hidden pt-16 pb-24 lg:pt-32">
          <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-blue-100 via-white to-white"></div>
          <div className="mx-auto max-w-6xl px-4 text-center">
            <div className="inline-flex items-center rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-sm text-blue-800 mb-8">
              <span className="flex h-2 w-2 rounded-full bg-blue-600 mr-2"></span>
              Now with AI-Powered Scheduling
            </div>
            <h1 className="mx-auto max-w-4xl text-5xl font-bold tracking-tight text-gray-900 sm:text-7xl">
              The Operating System for <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Modern Laundromats</span>
            </h1>
            <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600 leading-relaxed">
              Streamline your laundry business with our all-in-one platform. From pickup & delivery to in-store POS,
              LaundroMate handles the logistics so you can focus on growth.
            </p>
            <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link href="/auth/register">
                <Button size="lg" className="h-12 px-8 text-base bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-600/20">
                  Start for Free
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
              <Link href="/schedule-demo">
                <Button variant="outline" size="lg" className="h-12 px-8 text-base">
                  Schedule Demo
                </Button>
              </Link>
            </div>

            {/* Hero Image / Dashboard Preview */}
            <div className="mt-20 relative mx-auto max-w-5xl rounded-xl border bg-white/50 p-2 shadow-2xl backdrop-blur-sm lg:rounded-2xl lg:p-4">
              <div className="aspect-[16/9] rounded-lg bg-gradient-to-br from-gray-100 to-gray-50 border overflow-hidden relative group">
                {/* Placeholder for actual dashboard screenshot */}
                <div className="absolute inset-0 flex items-center justify-center text-gray-400">
                  <div className="text-center">
                    <LayoutDashboard className="h-16 w-16 mx-auto mb-4 opacity-50" />
                    <p className="font-medium">Dashboard Preview</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features Grid */}
        <section id="features" className="py-24 bg-gray-50">
          <div className="mx-auto max-w-6xl px-4">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Everything you need to run your shop</h2>
              <p className="mt-4 text-lg text-gray-600">Powerful tools designed specifically for the laundry industry.</p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {[
                {
                  icon: Truck,
                  title: "Pickup & Delivery",
                  description: "Automated route optimization, driver app, and real-time customer tracking."
                },
                {
                  icon: Store,
                  title: "In-Store POS",
                  description: "Fast, easy-to-use point of sale for walk-in customers and wash & fold orders."
                },
                {
                  icon: Users,
                  title: "Customer Management",
                  description: "CRM with order history, preferences, and automated SMS/Email notifications."
                },
                {
                  icon: ShoppingBag,
                  title: "Online Ordering",
                  description: "Branded web and mobile app for your customers to schedule pickups easily."
                },
                {
                  icon: LayoutDashboard,
                  title: "Business Analytics",
                  description: "Real-time reporting on revenue, orders, and staff performance."
                },
                {
                  icon: CheckCircle2,
                  title: "Quality Control",
                  description: "Track every garment with digital tagging and photo proof of delivery."
                }
              ].map((feature, i) => (
                <div key={i} className="bg-white p-8 rounded-2xl border shadow-sm hover:shadow-md transition-shadow">
                  <div className="h-12 w-12 rounded-lg bg-blue-50 flex items-center justify-center mb-6 text-blue-600">
                    <feature.icon className="h-6 w-6" />
                  </div>
                  <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                  <p className="text-gray-600 leading-relaxed">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Portals Section */}
        <section id="portals" className="py-24">
          <div className="mx-auto max-w-6xl px-4">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div className="relative overflow-hidden rounded-3xl bg-blue-600 p-8 md:p-12 text-white shadow-xl">
                <div className="relative z-10">
                  <h3 className="text-2xl font-bold mb-4">For Customers</h3>
                  <p className="text-blue-100 mb-8 text-lg">
                    Schedule pickups, track your laundry, and manage your account.
                    Fresh clothes are just a tap away.
                  </p>
                  <Link href="/auth/login?type=customer">
                    <Button className="bg-white text-blue-600 hover:bg-blue-50 border-0">
                      Customer Login
                    </Button>
                  </Link>
                </div>
                <div className="absolute right-0 bottom-0 opacity-10 transform translate-x-1/4 translate-y-1/4">
                  <ShoppingBag className="h-64 w-64" />
                </div>
              </div>

              <div className="relative overflow-hidden rounded-3xl bg-gray-900 p-8 md:p-12 text-white shadow-xl">
                <div className="relative z-10">
                  <h3 className="text-2xl font-bold mb-4">For Business Operators</h3>
                  <p className="text-gray-300 mb-8 text-lg">
                    Manage your fleet, staff, and orders from one central dashboard.
                    Take control of your operations.
                  </p>
                  <Link href="/auth/login?type=business">
                    <Button className="bg-white text-gray-900 hover:bg-gray-100 border-0">
                      Operator Login
                    </Button>
                  </Link>
                </div>
                <div className="absolute right-0 bottom-0 opacity-10 transform translate-x-1/4 translate-y-1/4">
                  <LayoutDashboard className="h-64 w-64" />
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-24 bg-blue-50">
          <div className="mx-auto max-w-4xl px-4 text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl mb-6">
              Ready to modernize your laundry business?
            </h2>
            <p className="text-lg text-gray-600 mb-10">
              Join hundreds of laundromats using LaundroMate to save time and increase revenue.
            </p>
            <Link href="/auth/register">
              <Button size="lg" className="h-12 px-8 text-base bg-blue-600 hover:bg-blue-700 text-white">
                Get Started Now
              </Button>
            </Link>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
