import { NextRequest } from "next/server";
import { proxyGet, proxyPost } from "@/lib/api/server-route";

export async function GET(req: NextRequest) {
  return proxyGet(req, "/super-admin/organizations");
}

export async function POST(req: NextRequest) {
  return proxyPost(req, "/super-admin/organizations");
}
