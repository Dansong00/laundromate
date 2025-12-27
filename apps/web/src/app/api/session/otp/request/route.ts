import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  // Use internal Docker service name when running in Docker, otherwise localhost
  const apiUrl =
    process.env.API_URL_INTERNAL ||
    process.env.NEXT_PUBLIC_API_URL ||
    "http://localhost:8000";
  const body = await req.json();

  const res = await fetch(`${apiUrl}/auth/otp/request`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}
