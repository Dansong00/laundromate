import { cva, type VariantProps } from "class-variance-authority";
import React from "react";
import { cn } from "../utils/cn";

const spinnerVariants = cva(
  "animate-spin rounded-full border-solid border-current border-r-transparent",
  {
    variants: {
      size: {
        sm: "h-4 w-4 border-2",
        default: "h-6 w-6 border-2",
        lg: "h-8 w-8 border-3",
        xl: "h-12 w-12 border-4",
      },
      color: {
        default: "text-gray-600",
        primary: "text-blue-600",
        secondary: "text-gray-500",
        white: "text-white",
      },
    },
    defaultVariants: {
      size: "default",
      color: "default",
    },
  }
);

export interface LoadingSpinnerProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof spinnerVariants> {
  text?: string;
  overlay?: boolean;
}

const LoadingSpinner = React.forwardRef<HTMLDivElement, LoadingSpinnerProps>(
  ({ className, size, color, text, overlay = false, ...props }, ref) => {
    const content = (
      <div
        ref={ref}
        className={cn("flex flex-col items-center justify-center", className)}
        {...props}
      >
        <div className={cn(spinnerVariants({ size, color }))} />
        {text && <p className="mt-2 text-sm text-gray-600">{text}</p>}
      </div>
    );

    if (overlay) {
      return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-white bg-opacity-75">
          {content}
        </div>
      );
    }

    return content;
  }
);

LoadingSpinner.displayName = "LoadingSpinner";

export { LoadingSpinner, spinnerVariants };
