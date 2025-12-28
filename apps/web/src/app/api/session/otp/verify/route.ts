import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  // Use internal Docker service name when running in Docker, otherwise localhost
  const apiUrl =
    process.env.API_URL_INTERNAL ||
    process.env.NEXT_PUBLIC_API_URL ||
    "http://localhost:8000";
  const body = await req.json();

  const res = await fetch(`${apiUrl}/auth/otp/verify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  const data = await res.json();
  const response = NextResponse.json(data, { status: res.status });

  if (res.ok && data.access_token) {
    // Store token in httpOnly cookie
    response.cookies.set("access_token", data.access_token, {
      httpOnly: true,
      sameSite: "lax",
      path: "/",
      secure: process.env.NODE_ENV === "production",
      maxAge: 60 * 60 * 24 * 7, // 7 days
    });
    return response;
  }

  return response;
}
