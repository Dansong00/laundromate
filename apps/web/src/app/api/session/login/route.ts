import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const body = await req.json();
  const res = await fetch(`${apiUrl}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const text = await res.text();
  const data = text ? JSON.parse(text) : {};
  const response = NextResponse.json(data, { status: res.status });
  if (res.ok && data.access_token) {
    // Store token in both httpOnly cookie (for security) and response body (for client-side access)
    response.cookies.set("access_token", data.access_token, {
      httpOnly: true,
      sameSite: "lax",
      path: "/",
      secure: true,
      maxAge: 60 * 60 * 24 * 7,
    });
    // Also return the token in the response body so the client can store it in sessionStorage
    return NextResponse.json(
      { ...data, access_token: data.access_token },
      { status: res.status }
    );
  }
  return response;
}
