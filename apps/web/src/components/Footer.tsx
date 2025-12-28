import Image from "next/image";
import Link from "next/link";

export function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="border-t mt-12">
      <div className="mx-auto max-w-6xl px-4 py-8 grid gap-6 md:grid-cols-3 items-start">
        <div className="flex items-start gap-3">
          <Link href="/" className="shrink-0" aria-label="LaundroMate home">
            <Image
              src="/logo-mark.svg"
              alt="LaundroMate logo"
              width={28}
              height={28}
            />
          </Link>
          <div>
            <Link href="/" className="font-semibold text-lg">
              LaundroMate
            </Link>
            <p className="mt-2 text-sm text-gray-600">
              Modern operations for pickup & delivery and in‑store wash & fold.
            </p>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <div className="font-medium mb-2">Product</div>
            <ul className="space-y-1">
              <li>
                <Link
                  href="/learn-more"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Learn more
                </Link>
              </li>
              <li>
                <Link
                  href="/schedule-demo"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Schedule a demo
                </Link>
              </li>
              <li>
                <Link
                  href="/portal"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Portal
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <div className="font-medium mb-2">Company</div>
            <ul className="space-y-1">
              <li>
                <Link
                  href="/terms"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Terms of Service
                </Link>
              </li>
              <li>
                <Link
                  href="/privacy"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Privacy Policy
                </Link>
              </li>
              <li>
                <a
                  href="mailto:danger091@gmail.com"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Contact Us
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div className="text-sm text-gray-600 md:text-right">
          <div>© {year} LaundroMate. All rights reserved.</div>
          <div className="mt-2">Made with ❤️ for laundromats operators.</div>
        </div>
      </div>
    </footer>
  );
}
