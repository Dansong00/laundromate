import { NextRequest, NextResponse } from "next/server";

export async function GET(
  req: NextRequest,
  { params }: { params: { orderId: string } },
) {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const cookieToken = req.cookies.get("access_token")?.value;
  const res = await fetch(`${apiUrl}/orders/${params.orderId}/detail`, {
    headers: {
      "Content-Type": "application/json",
      ...(cookieToken ? { Authorization: `Bearer ${cookieToken}` } : {}),
    },
    cache: "no-store",
  });
  const text = await res.text();
  const data = text ? JSON.parse(text) : {};
  return NextResponse.json(data, { status: res.status });
}
