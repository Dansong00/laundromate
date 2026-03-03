import type { AxiosError } from "axios";

export type ApiErrorDetails = unknown;

export class ApiError extends Error {
  readonly status?: number;
  readonly details?: ApiErrorDetails;
  readonly code?: string;

  constructor(args: {
    message: string;
    status?: number;
    details?: ApiErrorDetails;
    code?: string;
    cause?: unknown;
  }) {
    super(args.message);
    this.name = "ApiError";
    this.status = args.status;
    this.details = args.details;
    this.code = args.code;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (this as any).cause = args.cause;
  }
}

function pickMessageFromDetails(details: unknown): string | undefined {
  if (!details || typeof details !== "object") return undefined;
  const d = details as Record<string, unknown>;
  const msg =
    (typeof d.detail === "string" && d.detail) ||
    (typeof d.message === "string" && d.message) ||
    undefined;
  return msg;
}

export function toApiError(err: unknown): ApiError {
  if (err instanceof ApiError) return err;

  // AxiosError
  if (typeof err === "object" && err !== null && "isAxiosError" in err) {
    const axiosErr = err as AxiosError;
    const status = axiosErr.response?.status;
    const details = axiosErr.response?.data;
    const extracted = pickMessageFromDetails(details);
    const message =
      extracted ||
      (status
        ? `Request failed with ${status}`
        : axiosErr.message || "Request failed");

    return new ApiError({
      message,
      status,
      details,
      code: axiosErr.code,
      cause: err,
    });
  }

  // Fallback
  if (err instanceof Error) {
    return new ApiError({ message: err.message, cause: err });
  }

  return new ApiError({ message: "Request failed", cause: err });
}
