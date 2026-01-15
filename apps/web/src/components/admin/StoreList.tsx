"use client";

import { useRouter } from "next/navigation";
import { useStoresByOrganizationQuery } from "@/features/stores/hooks/useStores";
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
import { Plus, Store } from "lucide-react";
import { LoadingSpinner, EmptyState } from "@/lib/ui";
import { ROUTES } from "@/lib/routes";
import type { Store as StoreType } from "@laundromate/types";

interface StoreListProps {
  organizationId: string;
  onCreateNew?: () => void;
}

export function StoreList({ organizationId, onCreateNew }: StoreListProps) {
  const router = useRouter();
  const {
    data: stores,
    isLoading,
    error,
  } = useStoresByOrganizationQuery(organizationId);

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
        <p className="text-red-800">Error loading stores: {error.message}</p>
      </div>
    );
  }

  if (!stores || stores.length === 0) {
    return (
      <EmptyState
        icon={<Store className="w-12 h-12 text-gray-400" />}
        title="No stores"
        description="Get started by creating your first store for this organization"
        action={
          onCreateNew && (
            <Button onClick={onCreateNew} className="mt-4">
              <Plus className="w-4 h-4 mr-2" />
              Create Store
            </Button>
          )
        }
      />
    );
  }

  const getStatusBadgeVariant = (
    status: StoreType["status"],
  ): "default" | "secondary" | "destructive" => {
    switch (status) {
      case "active":
        return "default";
      case "inactive":
        return "secondary";
      default:
        return "secondary";
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold text-gray-900">Stores</h2>
        {onCreateNew && (
          <Button onClick={onCreateNew}>
            <Plus className="w-4 h-4 mr-2" />
            New Store
          </Button>
        )}
      </div>

      <div className="border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Street Address</TableHead>
              <TableHead>City</TableHead>
              <TableHead>State</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {stores.map((store) => (
              <TableRow
                key={store.id}
                className="cursor-pointer hover:bg-gray-50"
                onClick={() => router.push(ROUTES.ADMIN_STORE_DETAIL(store.id))}
              >
                <TableCell className="font-medium">{store.name}</TableCell>
                <TableCell>{store.streetAddress}</TableCell>
                <TableCell>{store.city}</TableCell>
                <TableCell>{store.state}</TableCell>
                <TableCell>
                  <Badge variant={getStatusBadgeVariant(store.status)}>
                    {store.status}
                  </Badge>
                </TableCell>
                <TableCell className="text-right">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      router.push(ROUTES.ADMIN_STORE_DETAIL(store.id));
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
