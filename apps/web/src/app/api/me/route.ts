import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const cookieToken = req.cookies.get("access_token")?.value;
  const headerAuth = req.headers.get("authorization");
  const authHeader = cookieToken
    ? { Authorization: `Bearer ${cookieToken}` }
    : headerAuth
    ? { Authorization: headerAuth }
    : {};

  const res = await fetch(`${apiUrl}/auth/me`, {
    headers: {
      "Content-Type": "application/json",
      ...authHeader,
    },
    cache: "no-store",
  });

  const text = await res.text();
  const body = text ? JSON.parse(text) : {};
  return NextResponse.json(body, { status: res.status });
}
