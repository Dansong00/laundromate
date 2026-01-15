import { NextRequest } from "next/server";
import { proxyToBackend } from "@/lib/api/server-route";

export async function PUT(
  req: NextRequest,
  { params }: { params: { orderId: string } },
) {
  const { status } = await req.json();

  return proxyToBackend(req, `/orders/${params.orderId}/status`, {
    method: "PUT",
    searchParams: { status_value: status },
  });
}
