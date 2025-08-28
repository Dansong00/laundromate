import { NextRequest, NextResponse } from "next/server";

export async function PUT(
  req: NextRequest,
  { params }: { params: { orderId: string } }
) {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const cookieToken = req.cookies.get("access_token")?.value;
  const { status } = await req.json();

  const res = await fetch(
    `${apiUrl}/orders/${encodeURIComponent(
      params.orderId
    )}/status?status_value=${encodeURIComponent(status)}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...(cookieToken ? { Authorization: `Bearer ${cookieToken}` } : {}),
      },
    }
  );

  const text = await res.text();
  const data = text ? JSON.parse(text) : {};
  return NextResponse.json(data, { status: res.status });
}
