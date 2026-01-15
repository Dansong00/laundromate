import { NextRequest } from "next/server";
import { proxyGet, proxyPut } from "@/lib/api/server-route";

export async function GET(
  req: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  const { id } = await params;
  return proxyGet(req, `/super-admin/stores/${id}`);
}

export async function PUT(
  req: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  const { id } = await params;
  return proxyPut(req, `/super-admin/stores/${id}`);
}
