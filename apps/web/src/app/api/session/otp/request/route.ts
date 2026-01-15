import { NextRequest } from "next/server";
import { proxyPost } from "@/lib/api/server-route";

export async function POST(req: NextRequest) {
  return proxyPost(req, "/auth/otp/request");
}
