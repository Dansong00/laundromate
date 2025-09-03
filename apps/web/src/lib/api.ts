const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface RegisterPayload {
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
}

export interface UserRead {
  id: string;
  email: string;
  first_name?: string | null;
  last_name?: string | null;
  phone?: string | null;
  role?: string | null; // Add role field for admin detection
}

export interface CustomerCreatePayload {
  user_id: string;
  preferred_pickup_time?: string;
  special_instructions?: string;
  email_notifications?: boolean;
  sms_notifications?: boolean;
}

export interface CustomerRead extends Record<string, unknown> {
  id: number;
  user_id: string;
}

export interface AddressRead {
  id: number;
  customer_id: number;
  address_line_1: string;
  address_line_2?: string | null;
  city: string;
  state: string;
  zip_code: string;
  address_type: string;
  is_default: boolean;
}

export interface AddressCreatePayload {
  customer_id: number;
  address_line_1: string;
  address_line_2?: string;
  city: string;
  state: string;
  zip_code: string;
  address_type: string;
  is_default?: boolean;
}

export interface ServiceRead {
  id: number;
  name: string;
  base_price: number;
  price_per_pound?: number | null;
  price_per_item?: number | null;
}

export interface OrderItemCreatePayload {
  service_id: number;
  item_name: string;
  item_type: string;
  quantity: number;
  unit_price: number;
}

export interface OrderCreatePayload {
  customer_id: number;
  pickup_address_id: number;
  delivery_address_id: number;
  pickup_date: string;
  pickup_time_slot: string;
  delivery_date: string;
  delivery_time_slot: string;
  items: OrderItemCreatePayload[];
}

export interface OrderRead {
  id: number;
  order_number: string;
  status: string;
  total_amount: number;
  created_at: string;
}

function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return sessionStorage.getItem("access_token");
}

export function getAuthHeader(): Record<string, string> {
  const token = getAccessToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function apiFetch<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_URL}${path.startsWith("/") ? path : `/${path}`}`;
  const headers = new Headers(options.headers || {});
  if (!headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  // Attach bearer token on the client when available
  const authHeader = getAuthHeader();
  if (authHeader.Authorization && !headers.has("Authorization")) {
    headers.set("Authorization", authHeader.Authorization);
  }
  const res = await fetch(url, { ...options, headers });
  if (!res.ok) {
    let message = `Request failed with ${res.status}`;
    try {
      const data = await res.json();
      message = (data && (data.detail || data.message)) || message;
    } catch (_) {
      // ignore
    }
    throw new Error(message);
  }
  // Some endpoints may return no content
  const text = await res.text();
  return text ? (JSON.parse(text) as T) : (undefined as unknown as T);
}

export async function login(
  email: string,
  password: string
): Promise<LoginResponse> {
  return apiFetch<LoginResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function register(payload: RegisterPayload): Promise<UserRead> {
  return apiFetch<UserRead>("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getApiBaseUrl(): string {
  return API_URL;
}

export async function getMe(): Promise<UserRead> {
  return apiFetch<UserRead>("/auth/me", { method: "GET" });
}

export async function createCustomer(
  payload: CustomerCreatePayload
): Promise<CustomerRead> {
  return apiFetch<CustomerRead>("/customers", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function listServices(): Promise<ServiceRead[]> {
  return apiFetch<ServiceRead[]>("/services", { method: "GET" });
}

export async function createOrder(payload: OrderCreatePayload) {
  return apiFetch("/orders", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function listOrders(): Promise<OrderRead[]> {
  return apiFetch<OrderRead[]>("/orders", { method: "GET" });
}

export async function listAddresses(
  customerId: number
): Promise<AddressRead[]> {
  return apiFetch<AddressRead[]>(`/addresses?customer_id=${customerId}`, {
    method: "GET",
  });
}

export async function createAddress(
  payload: AddressCreatePayload
): Promise<AddressRead> {
  return apiFetch<AddressRead>("/addresses", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getMyCustomer(): Promise<any> {
  return apiFetch("/customers/me", { method: "GET" });
}

// Role-based access control utilities
export function isAdminUser(user: any): boolean {
  return user?.role === "admin" || user?.role === "staff";
}

export function isCustomerUser(user: any): boolean {
  return !isAdminUser(user);
}
