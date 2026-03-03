import { NextRequest } from "next/server";
import { proxyPost } from "@/lib/api/server-route";

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
