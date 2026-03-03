"use client";

import { SignIn } from "@clerk/nextjs";
import Link from "next/link";

export default function LoginPage() {
  return (
    <div className="mx-auto max-w-sm py-12 px-4">
      <div className="flex flex-col items-center gap-6">
        <SignIn
          afterSignInUrl="/portal"
          afterSignUpUrl="/portal"
          signUpUrl="/auth/sign-up"
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
