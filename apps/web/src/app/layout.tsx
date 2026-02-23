import { AuthProvider } from "@/components/AuthProvider";
import { ToastProvider } from "@/components/ToastProvider";
import { QueryProvider } from "@/providers/QueryProvider";
import { ClerkProvider } from "@clerk/nextjs";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "LaundroMate - Fresh Laundry Delivered",
  description: "Professional laundry service with pickup and delivery",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const publishableKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;

  return (
    <html lang="en">
      <body className={`${inter.className} antialiased`}>
        <ClerkProvider
          publishableKey={publishableKey ?? ""}
          afterSignOutUrl="/auth/login"
        >
          <QueryProvider>
            <AuthProvider>
              <ToastProvider>{children}</ToastProvider>
            </AuthProvider>
          </QueryProvider>
        </ClerkProvider>
      </body>
    </html>
  );
}
