"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useCreateOrganizationMutation } from "@/features/organizations/hooks/useOrganizations";
import { useCreateStoreMutation } from "@/features/stores/hooks/useStores";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { AlertDescription } from "@/components/ui/alert";
import { LoadingSpinner } from "@/lib/ui";
import { CheckCircle2, Building2, Store, UserPlus } from "lucide-react";
import { useToast } from "@/components/ToastProvider";
import { ROUTES } from "@/lib/routes";
import type { OrganizationCreate, StoreCreate } from "@laundromate/types";

interface OrganizationWizardProps {
  onComplete?: (organizationId: string) => void;
}

type Step = "organization" | "store" | "invite";

export function OrganizationWizard({ onComplete }: OrganizationWizardProps) {
  const router = useRouter();
  const { notifySuccess, notifyError } = useToast();
  const [step, setStep] = useState<Step>("organization");
  const [organizationId, setOrganizationId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const createOrgMutation = useCreateOrganizationMutation();
  const createStoreMutation = useCreateStoreMutation();

  const [orgData, setOrgData] = useState<OrganizationCreate>({
    name: "",
    billingAddress: "",
    city: "",
    state: "",
    postalCode: "",
    country: "US",
    contactEmail: null,
    contactPhone: null,
    status: "active",
  });

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

  const updateOrgField = <K extends keyof OrganizationCreate>(
    key: K,
    value: OrganizationCreate[K],
  ) => {
    setOrgData((prev) => ({ ...prev, [key]: value }));
  };

  const updateStoreField = <K extends keyof typeof storeData>(
    key: K,
    value: (typeof storeData)[K],
  ) => {
    setStoreData((prev) => ({ ...prev, [key]: value }));
  };

  const handleCreateOrganization = async () => {
    setError(null);
    try {
      const org = await createOrgMutation.mutateAsync(orgData);
      setOrganizationId(org.id);
      setStep("store");
      notifySuccess("Organization created successfully");
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Failed to create organization";
      setError(message);
      notifyError(message);
    }
  };

  const handleCreateStore = async () => {
    if (!organizationId) {
      setError("Organization ID is required");
      return;
    }

    setError(null);
    try {
      await createStoreMutation.mutateAsync({
        ...storeData,
        organizationId,
      });
      setStep("invite");
      notifySuccess("Store created successfully");
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Failed to create store";
      setError(message);
      notifyError(message);
    }
  };

  const handleComplete = () => {
    if (onComplete && organizationId) {
      onComplete(organizationId);
    } else if (organizationId) {
      router.push(ROUTES.ADMIN_ORGANIZATION_DETAIL(organizationId));
    }
  };

  const steps = [
    { id: "organization", label: "Organization", icon: Building2 },
    { id: "store", label: "Store", icon: Store },
    { id: "invite", label: "Invite Owner", icon: UserPlus },
  ];

  const currentStepIndex = steps.findIndex((s) => s.id === step);

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Progress Indicator */}
      <div className="flex items-center justify-between">
        {steps.map((stepItem, index) => {
          const Icon = stepItem.icon;
          const isActive = stepItem.id === step;
          const isCompleted = index < currentStepIndex;

          return (
            <div key={stepItem.id} className="flex items-center flex-1">
              <div className="flex flex-col items-center">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center border-2 ${
                    isCompleted
                      ? "bg-green-500 border-green-500 text-white"
                      : isActive
                        ? "bg-blue-500 border-blue-500 text-white"
                        : "bg-gray-100 border-gray-300 text-gray-400"
                  }`}
                >
                  {isCompleted ? (
                    <CheckCircle2 className="w-6 h-6" />
                  ) : (
                    <Icon className="w-5 h-5" />
                  )}
                </div>
                <span
                  className={`mt-2 text-sm font-medium ${
                    isActive ? "text-blue-600" : "text-gray-500"
                  }`}
                >
                  {stepItem.label}
                </span>
              </div>
              {index < steps.length - 1 && (
                <div
                  className={`flex-1 h-0.5 mx-4 ${
                    isCompleted ? "bg-green-500" : "bg-gray-200"
                  }`}
                />
              )}
            </div>
          );
        })}
      </div>

      {/* Form Content */}
      <Card>
        <CardHeader>
          <CardTitle>
            {step === "organization" && "Create Organization"}
            {step === "store" && "Add First Store"}
            {step === "invite" && "Invite Organization Owner"}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
              <AlertDescription className="text-red-800">
                {error}
              </AlertDescription>
            </div>
          )}

          {step === "organization" && (
            <div className="space-y-4">
              <div>
                <Label htmlFor="name">Organization Name *</Label>
                <Input
                  id="name"
                  value={orgData.name}
                  onChange={(e) => updateOrgField("name", e.target.value)}
                  required
                />
              </div>

              <div>
                <Label htmlFor="billingAddress">Billing Address *</Label>
                <Input
                  id="billingAddress"
                  value={orgData.billingAddress}
                  onChange={(e) =>
                    updateOrgField("billingAddress", e.target.value)
                  }
                  required
                />
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="city">City *</Label>
                  <Input
                    id="city"
                    value={orgData.city}
                    onChange={(e) => updateOrgField("city", e.target.value)}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="state">State *</Label>
                  <Input
                    id="state"
                    value={orgData.state}
                    onChange={(e) => updateOrgField("state", e.target.value)}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="postalCode">Postal Code *</Label>
                  <Input
                    id="postalCode"
                    value={orgData.postalCode}
                    onChange={(e) =>
                      updateOrgField("postalCode", e.target.value)
                    }
                    required
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="country">Country *</Label>
                <Input
                  id="country"
                  value={orgData.country}
                  onChange={(e) => updateOrgField("country", e.target.value)}
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="contactEmail">Contact Email (optional)</Label>
                  <Input
                    id="contactEmail"
                    type="email"
                    value={orgData.contactEmail || ""}
                    onChange={(e) =>
                      updateOrgField("contactEmail", e.target.value || null)
                    }
                  />
                </div>
                <div>
                  <Label htmlFor="contactPhone">Contact Phone (optional)</Label>
                  <Input
                    id="contactPhone"
                    type="tel"
                    value={orgData.contactPhone || ""}
                    onChange={(e) =>
                      updateOrgField("contactPhone", e.target.value || null)
                    }
                  />
                </div>
              </div>

              <div className="flex justify-end pt-4">
                <Button
                  onClick={handleCreateOrganization}
                  disabled={createOrgMutation.isPending || !orgData.name}
                >
                  {createOrgMutation.isPending ? (
                    <>
                      <LoadingSpinner size="sm" className="mr-2" />
                      Creating...
                    </>
                  ) : (
                    "Create Organization"
                  )}
                </Button>
              </div>
            </div>
          )}

          {step === "store" && organizationId && (
            <div className="space-y-4">
              <div>
                <Label htmlFor="storeName">Store Name *</Label>
                <Input
                  id="storeName"
                  value={storeData.name}
                  onChange={(e) => updateStoreField("name", e.target.value)}
                  required
                />
              </div>

              <div>
                <Label htmlFor="streetAddress">Street Address *</Label>
                <Input
                  id="streetAddress"
                  value={storeData.streetAddress}
                  onChange={(e) =>
                    updateStoreField("streetAddress", e.target.value)
                  }
                  required
                />
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="storeCity">City *</Label>
                  <Input
                    id="storeCity"
                    value={storeData.city}
                    onChange={(e) => updateStoreField("city", e.target.value)}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="storeState">State *</Label>
                  <Input
                    id="storeState"
                    value={storeData.state}
                    onChange={(e) => updateStoreField("state", e.target.value)}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="storePostalCode">Postal Code *</Label>
                  <Input
                    id="storePostalCode"
                    value={storeData.postalCode}
                    onChange={(e) =>
                      updateStoreField("postalCode", e.target.value)
                    }
                    required
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="storeCountry">Country *</Label>
                <Input
                  id="storeCountry"
                  value={storeData.country}
                  onChange={(e) => updateStoreField("country", e.target.value)}
                  required
                />
              </div>

              <div className="flex justify-between pt-4">
                <Button
                  variant="outline"
                  onClick={() => setStep("organization")}
                >
                  Back
                </Button>
                <Button
                  onClick={handleCreateStore}
                  disabled={createStoreMutation.isPending || !storeData.name}
                >
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
            </div>
          )}

          {step === "invite" && organizationId && (
            <div className="space-y-4">
              <p className="text-gray-600">
                Organization and store created successfully! You can now invite
                an organization owner. You can also do this later from the
                organization detail page.
              </p>

              <div className="flex justify-between pt-4">
                <Button variant="outline" onClick={() => setStep("store")}>
                  Back
                </Button>
                <Button onClick={handleComplete}>
                  Complete &amp; View Organization
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
