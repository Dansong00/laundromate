import { NextResponse } from "next/server";

// Simple placeholder: rely on client-side token for now.
// In the future, move JWT to httpOnly cookie and validate here.
export function middleware() {
  return NextResponse.next();
}

export const config = {
  matcher: ["/portal/:path*", "/super-admin/:path*"],
};
