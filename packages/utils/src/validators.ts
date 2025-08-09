export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

export function validatePhone(phone: string): boolean {
  const phoneRegex = /^\+?[\d\s\-\(\)]{10,}$/;
  return phoneRegex.test(phone);
}

export function validateZipCode(zipCode: string): boolean {
  const zipRegex = /^\d{5}(-\d{4})?$/;
  return zipRegex.test(zipCode);
}

export function validateAddress(address: {
  street: string;
  city: string;
  state: string;
  zipCode: string;
}): { isValid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (!address.street.trim()) {
    errors.push('Street address is required');
  }

  if (!address.city.trim()) {
    errors.push('City is required');
  }

  if (!address.state.trim()) {
    errors.push('State is required');
  }

  if (!validateZipCode(address.zipCode)) {
    errors.push('Valid ZIP code is required');
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}
