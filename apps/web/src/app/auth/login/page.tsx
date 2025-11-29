"use client";

import { useToast } from "@/components/ToastProvider";
import { useAuth } from "@/components/AuthProvider";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function LoginPage() {
  const router = useRouter();
  const { notifySuccess, notifyError } = useToast();
  const { setToken } = useAuth();

  const [step, setStep] = useState<"phone" | "otp">("phone");
  const [phone, setPhone] = useState("");
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleRequestOTP(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch("/api/session/otp/request", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone }),
      });

      if (!res.ok) throw new Error("Failed to send OTP");

      notifySuccess("OTP sent to your phone");
      setStep("otp");
    } catch (err) {
      notifyError("Could not send OTP. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  async function handleVerifyOTP(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch("/api/session/otp/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone, code }),
      });

      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || "Invalid code");

      if (data.access_token) {
        sessionStorage.setItem("access_token", data.access_token);
        setToken(data.access_token);
        notifySuccess("Signed in successfully");
        router.push("/portal");
      }
    } catch (err) {
      notifyError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-sm py-12 px-4">
      <h1 className="text-2xl font-semibold mb-2">
        {step === "phone" ? "Welcome Back" : "Check your phone"}
      </h1>
      <p className="text-gray-500 mb-6 text-sm">
        {step === "phone"
          ? "Enter your phone number to sign in or create an account."
          : `We sent a code to ${phone}. Enter it below.`}
      </p>

      {step === "phone" ? (
        <form onSubmit={handleRequestOTP} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Phone Number</label>
            <input
              type="tel"
              placeholder="+1 (555) 000-0000"
              className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-black focus:border-transparent outline-none transition"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              required
            />
          </div>
          <button
            type="submit"
            className="w-full rounded-lg bg-black text-white py-2.5 font-medium disabled:opacity-50 hover:bg-gray-900 transition"
            disabled={loading || !phone}
          >
            {loading ? "Sending..." : "Continue"}
          </button>
        </form>
      ) : (
        <form onSubmit={handleVerifyOTP} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Verification Code</label>
            <input
              type="text"
              placeholder="123456"
              className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-black focus:border-transparent outline-none transition text-center tracking-widest text-lg"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              maxLength={6}
              required
            />
          </div>
          <button
            type="submit"
            className="w-full rounded-lg bg-black text-white py-2.5 font-medium disabled:opacity-50 hover:bg-gray-900 transition"
            disabled={loading || code.length < 6}
          >
            {loading ? "Verifying..." : "Verify & Sign In"}
          </button>
          <button
            type="button"
            onClick={() => setStep("phone")}
            className="w-full text-sm text-gray-500 hover:text-black transition"
          >
            Change phone number
          </button>
        </form>
      )}
    </div>
  );
}
