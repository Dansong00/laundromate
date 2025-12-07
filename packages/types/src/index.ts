// User and Authentication Types
export interface User {
  id: string;
  email?: string | null;
  firstName?: string | null;
  lastName?: string | null;
  phone?: string | null;
  isActive: boolean;
  isAdmin: boolean;
  isSuperAdmin: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface Customer extends User {
  addresses: Address[];
  preferences: CustomerPreferences;
}

export interface Address {
  id: string;
  customerId: string;
  type: 'home' | 'work' | 'other';
  street: string;
  city: string;
  state: string;
  zipCode: string;
  isDefault: boolean;
}

export interface CustomerPreferences {
  id: string;
  customerId: string;
  detergent: 'standard' | 'free' | 'sensitive';
  fabricSoftener: boolean;
  starch: 'none' | 'light' | 'medium' | 'heavy';
  specialInstructions?: string;
}

// Order Types
export interface Order {
  id: string;
  customerId: string;
  type: 'wash_fold' | 'pickup_delivery';
  status: OrderStatus;
  totalAmount: number;
  createdAt: Date;
  updatedAt: Date;
  items: OrderItem[];
  pickupDetails?: PickupDetails;
  deliveryDetails?: DeliveryDetails;
}

export type OrderStatus =
  | 'pending'
  | 'confirmed'
  | 'received'
  | 'washing'
  | 'drying'
  | 'folding'
  | 'ready'
  | 'completed'
  | 'cancelled';

export interface OrderItem {
  id: string;
  orderId: string;
  serviceType: ServiceType;
  quantity: number;
  unitPrice: number;
  totalPrice: number;
  weight?: number; // for wash & fold
  description?: string;
}

export type ServiceType =
  | 'wash_fold'
  | 'dry_clean'
  | 'press_only'
  | 'starch'
  | 'fabric_softener';

export interface PickupDetails {
  id: string;
  orderId: string;
  addressId: string;
  scheduledDate: Date;
  scheduledTime: string;
  actualDate?: Date;
  actualTime?: string;
  notes?: string;
}

export interface DeliveryDetails {
  id: string;
  orderId: string;
  addressId: string;
  scheduledDate: Date;
  scheduledTime: string;
  actualDate?: Date;
  actualTime?: string;
  notes?: string;
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

// Form Types
export interface OrderFormData {
  customerId: string;
  type: 'wash_fold' | 'pickup_delivery';
  items: OrderItemForm[];
  pickupDetails?: PickupDetailsForm;
  deliveryDetails?: DeliveryDetailsForm;
  specialInstructions?: string;
}

export interface OrderItemForm {
  serviceType: ServiceType;
  quantity: number;
  weight?: number;
  description?: string;
}

export interface PickupDetailsForm {
  addressId: string;
  scheduledDate: string;
  scheduledTime: string;
  notes?: string;
}

export interface DeliveryDetailsForm {
  addressId: string;
  scheduledDate: string;
  scheduledTime: string;
  notes?: string;
}
