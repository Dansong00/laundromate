"use client";

import { useRouter } from "next/navigation";
import { useOrganizationsQuery } from "@/features/organizations/hooks/useOrganizations";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Plus, Building2 } from "lucide-react";
import { LoadingSpinner, EmptyState } from "@/lib/ui";
import { ROUTES } from "@/lib/routes";
import type { Organization } from "@laundromate/types";

interface OrganizationListProps {
  onCreateNew?: () => void;
}

export function OrganizationList({ onCreateNew }: OrganizationListProps) {
  const router = useRouter();
  const { data: organizations, isLoading, error } = useOrganizationsQuery();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-md">
        <p className="text-red-800">
          Error loading organizations: {error.message}
        </p>
      </div>
    );
  }

  if (!organizations || organizations.length === 0) {
    return (
      <EmptyState
        icon={<Building2 className="w-12 h-12 text-gray-400" />}
        title="No organizations"
        description="Get started by creating your first organization"
        action={
          onCreateNew && (
            <Button onClick={onCreateNew} className="mt-4">
              <Plus className="w-4 h-4 mr-2" />
              Create Organization
            </Button>
          )
        }
      />
    );
  }

  const getStatusBadgeVariant = (
    status: Organization["status"],
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
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold text-gray-900">Organizations</h2>
        {onCreateNew && (
          <Button onClick={onCreateNew}>
            <Plus className="w-4 h-4 mr-2" />
            New Organization
          </Button>
        )}
      </div>

      <div className="border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>City</TableHead>
              <TableHead>State</TableHead>
              <TableHead>Country</TableHead>
              <TableHead>Contact Email</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {organizations.map((org) => (
              <TableRow
                key={org.id}
                className="cursor-pointer hover:bg-gray-50"
                onClick={() =>
                  router.push(ROUTES.ADMIN_ORGANIZATION_DETAIL(org.id))
                }
              >
                <TableCell className="font-medium">{org.name}</TableCell>
                <TableCell>{org.city}</TableCell>
                <TableCell>{org.state}</TableCell>
                <TableCell>{org.country}</TableCell>
                <TableCell>{org.contactEmail || "-"}</TableCell>
                <TableCell>
                  <Badge variant={getStatusBadgeVariant(org.status)}>
                    {org.status}
                  </Badge>
                </TableCell>
                <TableCell className="text-right">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      router.push(ROUTES.ADMIN_ORGANIZATION_DETAIL(org.id));
                    }}
                  >
                    View
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
