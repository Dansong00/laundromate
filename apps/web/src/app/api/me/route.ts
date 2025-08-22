import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const auth = req.headers.get("authorization");
  const res = await fetch(`${apiUrl}/auth/me`, {
    headers: {
      "Content-Type": "application/json",
      ...(auth ? { Authorization: auth } : {}),
    },
    cache: "no-store",
  });

  const text = await res.text();
  const body = text ? JSON.parse(text) : {};
  return NextResponse.json(body, { status: res.status });
}


