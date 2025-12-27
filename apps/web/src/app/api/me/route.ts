import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  // Use internal Docker service name when running in Docker, otherwise localhost
  const apiUrl =
    process.env.API_URL_INTERNAL ||
    process.env.NEXT_PUBLIC_API_URL ||
    "http://localhost:8000";
  const cookieToken = req.cookies.get("access_token")?.value;
  const headerAuth = req.headers.get("authorization");

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (cookieToken) {
    headers.Authorization = `Bearer ${cookieToken}`;
  } else if (headerAuth) {
    headers.Authorization = headerAuth;
  }

  const res = await fetch(`${apiUrl}/auth/me`, {
    headers,
    cache: "no-store",
  });

  const text = await res.text();
  const body = text ? JSON.parse(text) : {};
  return NextResponse.json(body, { status: res.status });
}
