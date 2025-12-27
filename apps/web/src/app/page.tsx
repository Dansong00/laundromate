"use client";

import { useAuth } from "@/components/AuthProvider";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { isAdminUser, isSuperAdminUser } from "@/lib/api";
import { Footer } from "@/components/Footer";
import { LandingHeader } from "@/components/landing/LandingHeader";
import { HeroSection } from "@/components/landing/HeroSection";
import { FeaturesSection } from "@/components/landing/FeaturesSection";
import { CTASection } from "@/components/landing/CTASection";

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
            const isSuperAdmin = isSuperAdminUser(user);
            const isAdmin = isAdminUser(user);

            if (isSuperAdmin) {
              router.replace("/super-admin");
            } else if (isAdmin) {
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
      <LandingHeader />
      <main className="flex-1">
        <HeroSection />
        <FeaturesSection />
        <CTASection />
      </main>
      <Footer />
    </div>
  );
}
