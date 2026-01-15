"use client";

import { use } from "react";
import { useRouter } from "next/navigation";
import { useOrganizationQuery } from "@/features/organizations/hooks/useOrganizations";
import { useCreateStoreMutation } from "@/features/stores/hooks/useStores";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { LoadingSpinner } from "@/lib/ui";
import { ArrowLeft } from "lucide-react";
import { useToast } from "@/components/ToastProvider";
import { ROUTES } from "@/lib/routes";
import { useState } from "react";
import type { StoreCreate } from "@laundromate/types";

export default function NewStorePage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id: organizationId } = use(params);
  const router = useRouter();
  const { notifySuccess, notifyError } = useToast();
  const { data: organization, isLoading: orgLoading } =
    useOrganizationQuery(organizationId);
  const createStoreMutation = useCreateStoreMutation();

  const [storeData, setStoreData] = useState<
    Omit<StoreCreate, "organizationId">
  >({
    name: "",
    streetAddress: "",
    city: "",
    state: "",
    postalCode: "",
    country: "US",
    status: "active",
  });

  const [error, setError] = useState<string | null>(null);

  const updateField = <K extends keyof typeof storeData>(
    key: K,
    value: (typeof storeData)[K],
  ) => {
    setStoreData((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      const store = await createStoreMutation.mutateAsync({
        ...storeData,
        organizationId,
      });
      notifySuccess("Store created successfully");
      router.push(ROUTES.ADMIN_STORE_DETAIL(store.id));
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Failed to create store";
      setError(message);
      notifyError(message);
    }
  };

  if (orgLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-6">
        <Button
          variant="outline"
          onClick={() =>
            router.push(ROUTES.ADMIN_ORGANIZATION_DETAIL(organizationId))
          }
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Organization
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>
            Create New Store{organization ? ` for ${organization.name}` : ""}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="name">Store Name *</Label>
              <Input
                id="name"
                value={storeData.name}
                onChange={(e) => updateField("name", e.target.value)}
                required
              />
            </div>

            <div>
              <Label htmlFor="streetAddress">Street Address *</Label>
              <Input
                id="streetAddress"
                value={storeData.streetAddress}
                onChange={(e) => updateField("streetAddress", e.target.value)}
                required
              />
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div>
                <Label htmlFor="city">City *</Label>
                <Input
                  id="city"
                  value={storeData.city}
                  onChange={(e) => updateField("city", e.target.value)}
                  required
                />
              </div>
              <div>
                <Label htmlFor="state">State *</Label>
                <Input
                  id="state"
                  value={storeData.state}
                  onChange={(e) => updateField("state", e.target.value)}
                  required
                />
              </div>
              <div>
                <Label htmlFor="postalCode">Postal Code *</Label>
                <Input
                  id="postalCode"
                  value={storeData.postalCode}
                  onChange={(e) => updateField("postalCode", e.target.value)}
                  required
                />
              </div>
            </div>

            <div>
              <Label htmlFor="country">Country *</Label>
              <Input
                id="country"
                value={storeData.country}
                onChange={(e) => updateField("country", e.target.value)}
                required
              />
            </div>

            <div className="flex justify-end space-x-4 pt-4">
              <Button
                type="button"
                variant="outline"
                onClick={() =>
                  router.push(ROUTES.ADMIN_ORGANIZATION_DETAIL(organizationId))
                }
              >
                Cancel
              </Button>
              <Button type="submit" disabled={createStoreMutation.isPending}>
                {createStoreMutation.isPending ? (
                  <>
                    <LoadingSpinner size="sm" className="mr-2" />
                    Creating...
                  </>
                ) : (
                  "Create Store"
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
