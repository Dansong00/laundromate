import React from "react";
import { cn } from "../utils/cn";

export interface EmptyStateProps extends React.HTMLAttributes<HTMLDivElement> {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: React.ReactNode;
  size?: "sm" | "default" | "lg";
}

const EmptyState = React.forwardRef<HTMLDivElement, EmptyStateProps>(
  (
    { className, icon, title, description, action, size = "default", ...props },
    ref
  ) => {
    const sizeClasses = {
      sm: "py-8",
      default: "py-12",
      lg: "py-16",
    };

    return (
      <div
        ref={ref}
        className={cn(
          "flex flex-col items-center justify-center text-center",
          sizeClasses[size],
          className
        )}
        {...props}
      >
        {icon && <div className="mb-4 text-gray-400">{icon}</div>}
        <h3 className="text-lg font-medium text-gray-900 mb-2">{title}</h3>
        {description && (
          <p className="text-sm text-gray-500 mb-6 max-w-sm">{description}</p>
        )}
        {action && <div className="flex justify-center">{action}</div>}
      </div>
    );
  }
);

EmptyState.displayName = "EmptyState";

export { EmptyState };
