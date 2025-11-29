import React from "react";
import { Badge, BadgeProps } from "./Badge";

export type OrderStatus =
  | "pending"
  | "confirmed"
  | "received"
  | "washing"
  | "drying"
  | "folding"
  | "ready"
  | "completed"
  | "cancelled";

export interface StatusBadgeProps
  extends Omit<BadgeProps, "variant" | "children"> {
  status: OrderStatus;
  showIcon?: boolean;
}

const statusConfig: Record<
  OrderStatus,
  { label: string; variant: BadgeProps["variant"]; color: string }
> = {
  pending: { label: "Pending", variant: "warning", color: "text-yellow-800" },
  confirmed: { label: "Confirmed", variant: "info", color: "text-blue-800" },
  received: { label: "Received", variant: "secondary", color: "text-gray-800" },
  washing: { label: "Washing", variant: "info", color: "text-blue-800" },
  drying: { label: "Drying", variant: "info", color: "text-blue-800" },
  folding: { label: "Folding", variant: "info", color: "text-blue-800" },
  ready: { label: "Ready", variant: "success", color: "text-green-800" },
  completed: {
    label: "Completed",
    variant: "success",
    color: "text-green-800",
  },
  cancelled: {
    label: "Cancelled",
    variant: "destructive",
    color: "text-red-800",
  },
};

const StatusBadge = React.forwardRef<HTMLDivElement, StatusBadgeProps>(
  ({ status, showIcon = false, className, ...props }, ref) => {
    const config = statusConfig[status];

    if (!config) {
      return null;
    }

    return (
      <Badge
        ref={ref}
        variant={config.variant}
        className={cn("capitalize", className)}
        {...props}
      >
        {showIcon && getStatusIcon(status)}
        {config.label}
      </Badge>
    );
  }
);

StatusBadge.displayName = "StatusBadge";

// Helper function to get status icons
const getStatusIcon = (status: OrderStatus) => {
  switch (status) {
    case "pending":
      return "⏳";
    case "confirmed":
      return "✅";
    case "received":
      return "📦";
    case "washing":
      return "🧺";
    case "drying":
      return "🌬️";
    case "folding":
      return "👕";
    case "ready":
      return "🎯";
    case "completed":
      return "🎉";
    case "cancelled":
      return "❌";
    default:
      return "";
  }
};

// Helper function for className concatenation
const cn = (...classes: (string | undefined | null | false)[]) => {
  return classes.filter(Boolean).join(" ");
};

export { StatusBadge };
