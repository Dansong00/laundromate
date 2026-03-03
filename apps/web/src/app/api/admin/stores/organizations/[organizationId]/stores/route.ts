import { NextRequest } from "next/server";
import { proxyGet, proxyPost } from "@/lib/api/server-route";

export async function GET(
  req: NextRequest,
  { params }: { params: Promise<{ organizationId: string }> },
) {
  const { organizationId } = await params;
  return proxyGet(
    req,
    `/super-admin/stores/organizations/${organizationId}/stores`,
  );
}

export async function POST(
  req: NextRequest,
  { params }: { params: Promise<{ organizationId: string }> },
) {
  const { organizationId } = await params;
  return proxyPost(
    req,
    `/super-admin/stores/organizations/${organizationId}/stores`,
  );
}
