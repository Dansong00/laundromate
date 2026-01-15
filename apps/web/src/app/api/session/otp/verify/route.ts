import { NextRequest, NextResponse } from "next/server";
import axios from "axios";
import { getApiUrl } from "@/lib/api/server-route";

export async function POST(req: NextRequest) {
  const apiUrl = getApiUrl();
  const body = await req.json();

  const res = await axios.post(`${apiUrl}/auth/otp/verify`, body, {
    headers: { "Content-Type": "application/json" },
    validateStatus: () => true,
  });

  const data = res.data;
  const response = NextResponse.json(data, { status: res.status });

  if (res.status >= 200 && res.status < 300 && data?.access_token) {
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
