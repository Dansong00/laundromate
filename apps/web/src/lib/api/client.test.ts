import { describe, it, expect, beforeEach, vi } from "vitest";

type AxiosRequestConfigLike = {
  url?: string;
  method?: string;
  headers?: Record<string, string>;
  data?: unknown;
};

let apiFetch: <T>(path: string, options?: RequestInit) => Promise<T>;
let getAuthHeader: () => Record<string, string>;
let buildQueryString: (
  params: Record<string, string | number | boolean | undefined>,
) => string;

let requestInterceptor:
  | ((config: AxiosRequestConfigLike) => AxiosRequestConfigLike)
  | null = null;
let responseErrorHandler: ((err: unknown) => unknown) | null = null;

// Keep this loosely typed; Vitest's generic typing for vi.fn differs across versions.
const mockRequestImpl = vi.fn();

const mockAxiosInstance = {
  interceptors: {
    request: {
      use: vi.fn((fn: typeof requestInterceptor) => {
        requestInterceptor = fn;
      }),
    },
    response: {
      use: vi.fn((_ok: unknown, errFn: typeof responseErrorHandler) => {
        responseErrorHandler = errFn;
      }),
    },
  },
  request: vi.fn(async (config: AxiosRequestConfigLike) => {
    const finalConfig = requestInterceptor
      ? requestInterceptor(config)
      : config;
    try {
      return await mockRequestImpl(finalConfig);
    } catch (e) {
      if (responseErrorHandler) {
        return responseErrorHandler(e) as Promise<never>;
      }
      throw e;
    }
  }),
};

const mockAxiosCreate = vi.fn(() => mockAxiosInstance);

vi.mock("axios", () => ({
  default: {
    create: mockAxiosCreate,
  },
}));

describe("getAuthHeader", () => {
  beforeEach(async () => {
    vi.clearAllMocks();
    vi.resetModules();
    requestInterceptor = null;
    responseErrorHandler = null;
    mockRequestImpl.mockReset();
    // Reset sessionStorage mock
    (window.sessionStorage.getItem as ReturnType<typeof vi.fn>).mockReturnValue(
      null,
    );
    const mod = await import("./client");
    getAuthHeader = mod.getAuthHeader;
  });

  it("returns Authorization header when token exists", () => {
    (window.sessionStorage.getItem as ReturnType<typeof vi.fn>).mockReturnValue(
      "test-token",
    );
    const header = getAuthHeader();
    expect(header).toEqual({ Authorization: "Bearer test-token" });
  });

  it("returns empty object when no token exists", () => {
    (window.sessionStorage.getItem as ReturnType<typeof vi.fn>).mockReturnValue(
      null,
    );
    const header = getAuthHeader();
    expect(header).toEqual({});
  });

  it("returns empty object when token is empty string", () => {
    (window.sessionStorage.getItem as ReturnType<typeof vi.fn>).mockReturnValue(
      "",
    );
    const header = getAuthHeader();
    expect(header).toEqual({});
  });
});

describe("buildQueryString", () => {
  beforeEach(async () => {
    vi.resetModules();
    requestInterceptor = null;
    responseErrorHandler = null;
    mockRequestImpl.mockReset();
    const mod = await import("./client");
    apiFetch = mod.apiFetch;
    getAuthHeader = mod.getAuthHeader;
    buildQueryString = mod.buildQueryString;
  });

  it("builds query string from params", () => {
    expect(buildQueryString({ foo: "bar", baz: "qux" })).toBe(
      "?foo=bar&baz=qux",
    );
  });

  it("handles numbers", () => {
    expect(buildQueryString({ page: 1, limit: 10 })).toBe("?page=1&limit=10");
  });

  it("handles booleans", () => {
    expect(buildQueryString({ active: true, deleted: false })).toBe(
      "?active=true&deleted=false",
    );
  });

  it("filters out undefined values", () => {
    expect(buildQueryString({ foo: "bar", baz: undefined })).toBe("?foo=bar");
  });

  it("filters out null values", () => {
    expect(
      buildQueryString({ foo: "bar", baz: null as unknown as undefined }),
    ).toBe("?foo=bar");
  });

  it("returns empty string for empty params", () => {
    expect(buildQueryString({})).toBe("");
  });

  it("handles mixed types", () => {
    expect(buildQueryString({ name: "test", age: 25, active: true })).toBe(
      "?name=test&age=25&active=true",
    );
  });
});

describe("apiFetch", () => {
  beforeEach(async () => {
    vi.clearAllMocks();
    vi.resetModules();
    requestInterceptor = null;
    responseErrorHandler = null;
    mockRequestImpl.mockReset();
    (window.sessionStorage.getItem as ReturnType<typeof vi.fn>).mockReturnValue(
      null,
    );

    const mod = await import("./client");
    apiFetch = mod.apiFetch;
    getAuthHeader = mod.getAuthHeader;
    buildQueryString = mod.buildQueryString;
  });

  it("makes successful GET request and returns JSON data", async () => {
    const mockData = { id: "1", name: "Test" };
    mockRequestImpl.mockResolvedValueOnce({ data: mockData });

    const result = await apiFetch<typeof mockData>("/api/test");
    expect(result).toEqual(mockData);
    expect(mockRequestImpl).toHaveBeenCalledWith(
      expect.objectContaining({
        url: "/test",
        method: "GET",
      }),
    );
    const callArgs = (mockRequestImpl as ReturnType<typeof vi.fn>).mock
      .calls[0]?.[0] as AxiosRequestConfigLike;
    expect(callArgs.headers?.["Content-Type"]).toBe("application/json");
  });

  it("normalizes path that starts with /api/", async () => {
    const mockData = { id: "1" };
    mockRequestImpl.mockResolvedValueOnce({ data: mockData });

    await apiFetch("/api/test");
    expect(mockRequestImpl).toHaveBeenCalledWith(
      expect.objectContaining({ url: "/test" }),
    );
  });

  it("normalizes path that starts with / but not /api/", async () => {
    const mockData = { id: "1" };
    mockRequestImpl.mockResolvedValueOnce({ data: mockData });

    await apiFetch("/test");
    expect(mockRequestImpl).toHaveBeenCalledWith(
      expect.objectContaining({ url: "/test" }),
    );
  });

  it("normalizes path that doesn't start with /", async () => {
    const mockData = { id: "1" };
    mockRequestImpl.mockResolvedValueOnce({ data: mockData });

    await apiFetch("test");
    expect(mockRequestImpl).toHaveBeenCalledWith(
      expect.objectContaining({ url: "/test" }),
    );
  });

  it("adds Authorization header when token exists", async () => {
    (window.sessionStorage.getItem as ReturnType<typeof vi.fn>).mockReturnValue(
      "test-token",
    );
    const mockData = { id: "1" };
    mockRequestImpl.mockResolvedValueOnce({ data: mockData });

    await apiFetch("/api/test");
    const callArgs = (mockRequestImpl as ReturnType<typeof vi.fn>).mock
      .calls[0]?.[0] as AxiosRequestConfigLike;
    expect(callArgs.headers?.Authorization).toBe("Bearer test-token");
    expect(callArgs.headers?.["Content-Type"]).toBe("application/json");
  });

  it("does not override existing Authorization header", async () => {
    (window.sessionStorage.getItem as ReturnType<typeof vi.fn>).mockReturnValue(
      "test-token",
    );
    const mockData = { id: "1" };
    mockRequestImpl.mockResolvedValueOnce({ data: mockData });

    await apiFetch("/api/test", {
      headers: {
        Authorization: "Bearer custom-token",
      },
    });
    const callArgs = (mockRequestImpl as ReturnType<typeof vi.fn>).mock
      .calls[0]?.[0] as AxiosRequestConfigLike;
    expect(callArgs.headers?.Authorization).toBe("Bearer custom-token");
  });

  it("sets Content-Type to application/json by default", async () => {
    const mockData = { id: "1" };
    mockRequestImpl.mockResolvedValueOnce({ data: mockData });

    await apiFetch("/api/test");
    const callArgs = (mockRequestImpl as ReturnType<typeof vi.fn>).mock
      .calls[0]?.[0] as AxiosRequestConfigLike;
    expect(callArgs.headers?.["Content-Type"]).toBe("application/json");
  });

  it("does not override existing Content-Type header", async () => {
    const mockData = { id: "1" };
    mockRequestImpl.mockResolvedValueOnce({ data: mockData });

    await apiFetch("/api/test", {
      headers: {
        "Content-Type": "application/xml",
      },
    });
    const callArgs = (mockRequestImpl as ReturnType<typeof vi.fn>).mock
      .calls[0]?.[0] as AxiosRequestConfigLike;
    expect(callArgs.headers?.["Content-Type"]).toBe("application/xml");
  });

  it("handles POST request with body", async () => {
    const mockData = { id: "1", name: "Created" };
    mockRequestImpl.mockResolvedValueOnce({ data: mockData });

    const body = { name: "Test" };
    await apiFetch("/api/test", {
      method: "POST",
      body: JSON.stringify(body),
    });

    expect(mockRequestImpl).toHaveBeenCalledWith(
      expect.objectContaining({
        method: "POST",
        data: JSON.stringify(body),
      }),
    );
  });

  it("handles empty response (no content)", async () => {
    mockRequestImpl.mockResolvedValueOnce({ data: "" });

    const result = await apiFetch<void>("/api/test");
    expect(result).toBeUndefined();
  });

  it("throws error on HTTP error response with detail message", async () => {
    mockRequestImpl.mockRejectedValueOnce({
      isAxiosError: true,
      response: { status: 404, data: { detail: "Not found" } },
      message: "Request failed with status code 404",
    });

    await expect(apiFetch("/api/test")).rejects.toThrow("Not found");
  });

  it("throws error on HTTP error response with message field", async () => {
    mockRequestImpl.mockRejectedValueOnce({
      isAxiosError: true,
      response: { status: 400, data: { message: "Bad request" } },
      message: "Request failed with status code 400",
    });

    await expect(apiFetch("/api/test")).rejects.toThrow("Bad request");
  });

  it("throws error with status code when no error message in response", async () => {
    mockRequestImpl.mockRejectedValueOnce({
      isAxiosError: true,
      response: { status: 500, data: {} },
      message: "Request failed with status code 500",
    });

    await expect(apiFetch("/api/test")).rejects.toThrow(
      "Request failed with 500",
    );
  });

  it("throws error with status code when response payload is not an object", async () => {
    mockRequestImpl.mockRejectedValueOnce({
      isAxiosError: true,
      response: { status: 500, data: "not-json" },
      message: "Request failed with status code 500",
    });

    await expect(apiFetch("/api/test")).rejects.toThrow(
      "Request failed with 500",
    );
  });
});
