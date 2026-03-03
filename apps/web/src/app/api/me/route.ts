import { NextRequest } from "next/server";
import { proxyGet } from "@/lib/api/server-route";

export async function GET(req: NextRequest) {
  return proxyGet(req, "/auth/me");
}
