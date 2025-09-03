import React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "../utils/cn";

const progressBarVariants = cva(
  "relative h-2 bg-gray-200 rounded-full overflow-hidden transition-all duration-1000 ease-out",
  {
    variants: {
      size: {
        sm: "h-1",
        default: "h-2",
        lg: "h-3",
      },
    },
    defaultVariants: {
      size: "default",
    },
  }
);

const progressFillVariants = cva(
  "absolute top-0 left-0 h-full rounded-full transition-all duration-1000 ease-out",
  {
    variants: {
      variant: {
        default: "bg-blue-600",
        success: "bg-green-600",
        warning: "bg-yellow-600",
        error: "bg-red-600",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

export interface ProgressBarProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof progressBarVariants> {
  progress: number; // 0-100
  variant?: VariantProps<typeof progressFillVariants>["variant"];
  showIndicator?: boolean;
  children?: React.ReactNode;
}

const ProgressBar = React.forwardRef<HTMLDivElement, ProgressBarProps>(
  (
    {
      className,
      size,
      progress,
      variant,
      showIndicator = false,
      children,
      ...props
    },
    ref
  ) => {
    const clampedProgress = Math.max(0, Math.min(100, progress));

    return (
      <div className="space-y-2">
        <div
          ref={ref}
          className={cn(progressBarVariants({ size, className }))}
          {...props}
        >
          <div
            className={cn(progressFillVariants({ variant }))}
            style={{ width: `${clampedProgress}%` }}
          />
          {showIndicator && (
            <div
              className="absolute top-0 w-4 h-4 bg-blue-600 rounded-full -mt-1 animate-pulse"
              style={{ left: `calc(${clampedProgress}% - 8px)` }}
            />
          )}
        </div>
        {children}
      </div>
    );
  }
);

ProgressBar.displayName = "ProgressBar";

export { ProgressBar, progressBarVariants, progressFillVariants };
