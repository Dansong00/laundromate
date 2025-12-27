import Link from "next/link";
import { Button } from "@/components/ui/button";

export function CTASection() {
  return (
    <section className="py-24">
      <div className="mx-auto max-w-4xl px-4 text-center">
        <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl mb-6">
          Ready to modernize your laundry business?
        </h2>
        <p className="text-lg text-gray-600 mb-10">
          Join hundreds of laundromats using LaundroMate to save time and
          increase revenue.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link href="/auth/login">
            <Button
              size="lg"
              className="h-12 px-8 text-base bg-black text-white hover:bg-gray-900"
            >
              Get Started
            </Button>
          </Link>
          <Link href="/auth/login">
            <Button variant="outline" size="lg" className="h-12 px-8 text-base">
              Log In
            </Button>
          </Link>
        </div>
      </div>
    </section>
  );
}
