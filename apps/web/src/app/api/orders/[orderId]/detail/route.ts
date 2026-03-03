import { NextRequest } from "next/server";
import { proxyGet } from "@/lib/api/server-route";

export async function GET(
  req: NextRequest,
  { params }: { params: { orderId: string } },
) {
  return proxyGet(req, `/orders/${params.orderId}/detail`);
}
