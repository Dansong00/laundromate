import { NextRequest, NextResponse } from "next/server";
import { proxyGet } from "@/lib/api/server-route";

export async function GET(req: NextRequest) {
  const searchParams = req.nextUrl.searchParams;
  const organizationId = searchParams.get("organization_id");

  if (!organizationId) {
    return NextResponse.json(
      { detail: "organization_id query parameter is required" },
      { status: 400 },
    );
  }

  return proxyGet(
    req,
    `/super-admin/stores/organizations/${organizationId}/stores`,
  );
}
