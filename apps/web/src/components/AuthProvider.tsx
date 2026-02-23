"use client";

import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { useAuth as useClerkAuth } from "@clerk/nextjs";
import { setApiTokenGetter } from "@/lib/api";

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
  const { isLoaded, isSignedIn, getToken, signOut } = useClerkAuth();
  const [legacyToken, setLegacyToken] = useState<string | null>(null);

  useEffect(() => {
    const stored =
      typeof window !== "undefined"
        ? sessionStorage.getItem("access_token")
        : null;
    if (stored) setLegacyToken(stored);
  }, []);

  useEffect(() => {
    if (!isLoaded) return;
    if (isSignedIn && getToken) {
      setApiTokenGetter(() => getToken());
    } else {
      setApiTokenGetter(() => Promise.resolve(null));
    }
    return () => {
      setApiTokenGetter(() => Promise.resolve(null));
    };
  }, [isLoaded, isSignedIn, getToken]);

  const setToken = useCallback((token: string | null) => {
    if (typeof window !== "undefined") {
      if (token) sessionStorage.setItem("access_token", token);
      else sessionStorage.removeItem("access_token");
    }
    setLegacyToken(token);
  }, []);

  const logout = useCallback(async () => {
    if (typeof window !== "undefined")
      sessionStorage.removeItem("access_token");
    setLegacyToken(null);
    setApiTokenGetter(() => Promise.resolve(null));
    await signOut();
  }, [signOut]);

  const isAuthenticated = Boolean(isSignedIn || legacyToken);

  const value = useMemo<AuthContextValue>(
    () => ({
      token: legacyToken,
      isAuthenticated,
      setToken,
      logout,
    }),
    [legacyToken, isAuthenticated, setToken, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
