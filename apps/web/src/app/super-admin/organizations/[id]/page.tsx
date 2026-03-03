"use client";

import { use } from "react";
import { useRouter } from "next/navigation";
import { useOrganizationQuery } from "@/features/organizations/hooks/useOrganizations";
import { useStoresByOrganizationQuery } from "@/features/stores/hooks/useStores";
import { StoreList } from "@/components/admin/StoreList";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { LoadingSpinner } from "@/lib/ui";
import { ArrowLeft, Edit, Mail, Phone, MapPin } from "lucide-react";

export default function OrganizationDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const router = useRouter();
  const { data: organization, isLoading, error } = useOrganizationQuery(id);
  useStoresByOrganizationQuery(id);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <LoadingSpinner />
      </div>
    );
  }

  if (error || !organization) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-md">
        <p className="text-red-800">
          Error loading organization:{" "}
          {error?.message || "Organization not found"}
        </p>
        <Button
          variant="outline"
          onClick={() => router.push("/super-admin/organizations")}
          className="mt-4"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Organizations
        </Button>
      </div>
    );
  }

  const getStatusBadgeVariant = (
    status: typeof organization.status,
  ): "default" | "secondary" | "destructive" => {
    switch (status) {
      case "active":
        return "default";
      case "inactive":
        return "secondary";
      case "suspended":
        return "destructive";
      default:
        return "secondary";
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button
            variant="outline"
            onClick={() => router.push("/super-admin/organizations")}
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              {organization.name}
            </h1>
            <p className="text-gray-500">Organization Details</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <Badge variant={getStatusBadgeVariant(organization.status)}>
            {organization.status}
          </Badge>
          <Button variant="outline">
            <Edit className="w-4 h-4 mr-2" />
            Edit
          </Button>
        </div>
      </div>

      {/* Organization Details */}
      <Card>
        <CardHeader>
          <CardTitle>Organization Information</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-500">
                  Name
                </label>
                <p className="mt-1 text-gray-900">{organization.name}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500 flex items-center">
                  <MapPin className="w-4 h-4 mr-1" />
                  Billing Address
                </label>
                <p className="mt-1 text-gray-900">
                  {organization.billingAddress}
                </p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">
                  Location
                </label>
                <p className="mt-1 text-gray-900">
                  {organization.city}, {organization.state}{" "}
                  {organization.postalCode}
                </p>
                <p className="text-gray-900">{organization.country}</p>
              </div>
            </div>
            <div className="space-y-4">
              {organization.contactEmail && (
                <div>
                  <label className="text-sm font-medium text-gray-500 flex items-center">
                    <Mail className="w-4 h-4 mr-1" />
                    Contact Email
                  </label>
                  <p className="mt-1 text-gray-900">
                    {organization.contactEmail}
                  </p>
                </div>
              )}
              {organization.contactPhone && (
                <div>
                  <label className="text-sm font-medium text-gray-500 flex items-center">
                    <Phone className="w-4 h-4 mr-1" />
                    Contact Phone
                  </label>
                  <p className="mt-1 text-gray-900">
                    {organization.contactPhone}
                  </p>
                </div>
              )}
              <div>
                <label className="text-sm font-medium text-gray-500">
                  Created
                </label>
                <p className="mt-1 text-gray-900">
                  {new Date(organization.createdAt).toLocaleDateString()}
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Stores Section */}
      <Card>
        <CardHeader>
          <CardTitle>Stores</CardTitle>
        </CardHeader>
        <CardContent>
          <StoreList
            organizationId={id}
            onCreateNew={() =>
              router.push(`/super-admin/organizations/${id}/stores/new`)
            }
          />
        </CardContent>
      </Card>
    </div>
  );
}
