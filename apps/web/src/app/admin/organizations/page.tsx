"use client";

import { OrganizationList } from "@/components/admin/OrganizationList";
import { useRouter } from "next/navigation";
import { ROUTES } from "@/lib/routes";

export default function OrganizationsPage() {
  const router = useRouter();

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <OrganizationList
        onCreateNew={() => router.push(ROUTES.ADMIN_ORGANIZATION_NEW)}
      />
    </div>
  );
}
