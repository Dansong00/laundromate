"use client";

import { use } from "react";
import { useRouter } from "next/navigation";
import { useStoreQuery } from "@/features/stores/hooks/useStores";
import { useOrganizationQuery } from "@/features/organizations/hooks/useOrganizations";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { LoadingSpinner } from "@/lib/ui";
import { ROUTES } from "@/lib/routes";
import { ArrowLeft, Edit, MapPin, Building2 } from "lucide-react";

export default function StoreDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const router = useRouter();
  const { data: store, isLoading, error } = useStoreQuery(id);
  const { data: organization } = useOrganizationQuery(
    store?.organizationId || "",
  );

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <LoadingSpinner />
      </div>
    );
  }

  if (error || !store) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-md">
        <p className="text-red-800">
          Error loading store: {error?.message || "Store not found"}
        </p>
        <Button
          variant="outline"
          onClick={() => router.push(ROUTES.ADMIN_ORGANIZATIONS)}
          className="mt-4"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Organizations
        </Button>
      </div>
    );
  }

  const getStatusBadgeVariant = (
    status: typeof store.status,
  ): "default" | "secondary" => {
    return status === "active" ? "default" : "secondary";
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button
            variant="outline"
            onClick={() =>
              router.push(
                ROUTES.ADMIN_ORGANIZATION_DETAIL(store.organizationId),
              )
            }
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{store.name}</h1>
            <p className="text-gray-500">Store Details</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <Badge variant={getStatusBadgeVariant(store.status)}>
            {store.status}
          </Badge>
          <Button variant="outline">
            <Edit className="w-4 h-4 mr-2" />
            Edit
          </Button>
        </div>
      </div>

      {/* Organization Link */}
      {organization && (
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-2 text-sm">
              <Building2 className="w-4 h-4 text-gray-400" />
              <span className="text-gray-500">Organization:</span>
              <Button
                variant="link"
                className="p-0 h-auto"
                onClick={() =>
                  router.push(ROUTES.ADMIN_ORGANIZATION_DETAIL(organization.id))
                }
              >
                {organization.name}
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Store Details */}
      <Card>
        <CardHeader>
          <CardTitle>Store Information</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-500">
                  Name
                </label>
                <p className="mt-1 text-gray-900">{store.name}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500 flex items-center">
                  <MapPin className="w-4 h-4 mr-1" />
                  Address
                </label>
                <p className="mt-1 text-gray-900">{store.streetAddress}</p>
              </div>
            </div>
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-500">
                  Location
                </label>
                <p className="mt-1 text-gray-900">
                  {store.city}, {store.state} {store.postalCode}
                </p>
                <p className="text-gray-900">{store.country}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">
                  Created
                </label>
                <p className="mt-1 text-gray-900">
                  {new Date(store.createdAt).toLocaleDateString()}
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
