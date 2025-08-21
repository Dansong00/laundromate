"use client";

import React, { createContext, useContext, useEffect, useMemo, useState } from "react";

type AuthContextValue = {
  token: string | null;
  isAuthenticated: boolean;
  setToken: (token: string | null) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const stored = typeof window !== "undefined" ? sessionStorage.getItem("access_token") : null;
    if (stored) setToken(stored);
  }, []);

  const logout = () => {
    sessionStorage.removeItem("access_token");
    setToken(null);
  };

  const value = useMemo<AuthContextValue>(
    () => ({ token, isAuthenticated: Boolean(token), setToken, logout }),
    [token]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}


