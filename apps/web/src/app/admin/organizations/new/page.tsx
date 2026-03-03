"use client";

import { OrganizationWizard } from "@/components/admin/OrganizationWizard";
import { useRouter } from "next/navigation";
import { ROUTES } from "@/lib/routes";

export default function NewOrganizationPage() {
  const router = useRouter();

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <OrganizationWizard
        onComplete={(organizationId) => {
          router.push(ROUTES.ADMIN_ORGANIZATION_DETAIL(organizationId));
        }}
      />
    </div>
  );
}
