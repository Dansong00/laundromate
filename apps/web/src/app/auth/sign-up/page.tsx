"use client";

import { SignUp } from "@clerk/nextjs";
import Link from "next/link";

export default function SignUpPage() {
  return (
    <div className="mx-auto max-w-sm py-12 px-4">
      <div className="flex flex-col items-center gap-6">
        <SignUp
          afterSignUpUrl="/portal"
          afterSignInUrl="/portal"
          signInUrl="/auth/login"
        />
        <p className="text-sm text-gray-500">
          <Link href="/" className="text-black underline hover:no-underline">
            ← Back to home
          </Link>
        </p>
      </div>
    </div>
  );
}
