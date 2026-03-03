"use client";

import { useSearchParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import {
  useValidateInvitationMutation,
  useAcceptInvitationMutation,
} from "@/features/invitations/api/mutations";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { LoadingSpinner } from "@/lib/ui";
import { useToast } from "@/components/ToastProvider";
import { useAuth } from "@/components/AuthProvider";
import { Mail, Building2, Shield } from "lucide-react";

export default function AcceptInvitationPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const { notifySuccess, notifyError } = useToast();
  const { setToken } = useAuth();
  const token = searchParams.get("token");

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordError, setPasswordError] = useState<string | null>(null);

  const validateMutation = useValidateInvitationMutation();
  const acceptMutation = useAcceptInvitationMutation();

  // Validate token on mount
  useEffect(() => {
    if (token) {
      validateMutation.mutate(token, {
        onError: (error) => {
          notifyError(error.message);
        },
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setPasswordError(null);

    // Validate password
    if (password.length < 8) {
      setPasswordError("Password must be at least 8 characters long");
      return;
    }

    if (password !== confirmPassword) {
      setPasswordError("Passwords do not match");
      return;
    }

    if (!token) {
      notifyError("Invalid invitation token");
      return;
    }

    try {
      const response = await acceptMutation.mutateAsync({ token, password });

      // Store the access token
      if (response.access_token) {
        setToken(response.access_token);
        notifySuccess("Account created successfully! Welcome to LaundroMate.");
        router.push("/portal");
      }
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Failed to accept invitation";
      notifyError(message);
    }
  };

  if (!token) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>Invalid Invitation</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600">
              This invitation link is invalid or missing a token. Please check
              your email for the correct invitation link.
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (validateMutation.isPending) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <LoadingSpinner />
      </div>
    );
  }

  if (validateMutation.isError || !validateMutation.data?.valid) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>Invalid Invitation</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600">
              {validateMutation.data?.reason ||
                validateMutation.error?.message ||
                "This invitation is invalid or has expired. Please contact the organization administrator for a new invitation."}
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  const invitationData = validateMutation.data;

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4 py-12">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Accept Invitation</CardTitle>
        </CardHeader>
        <CardContent>
          {invitationData.organizationName && (
            <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
              <div className="flex items-center space-x-2 mb-2">
                <Building2 className="w-5 h-5 text-blue-600" />
                <p className="font-medium text-blue-900">
                  {invitationData.organizationName}
                </p>
              </div>
              {invitationData.email && (
                <div className="flex items-center space-x-2 text-sm text-blue-700">
                  <Mail className="w-4 h-4" />
                  <span>{invitationData.email}</span>
                </div>
              )}
              {invitationData.organizationRole && (
                <div className="flex items-center space-x-2 text-sm text-blue-700 mt-1">
                  <Shield className="w-4 h-4" />
                  <span className="capitalize">
                    {invitationData.organizationRole}
                  </span>
                </div>
              )}
            </div>
          )}

          <p className="text-gray-600 mb-6">
            Create a password to complete your account setup and join the
            organization.
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="password">Password *</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={8}
              />
              <p className="text-xs text-gray-500 mt-1">
                Password must be at least 8 characters long
              </p>
            </div>

            <div>
              <Label htmlFor="confirmPassword">Confirm Password *</Label>
              <Input
                id="confirmPassword"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                minLength={8}
              />
            </div>

            {passwordError && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-md">
                <p className="text-sm text-red-800">{passwordError}</p>
              </div>
            )}

            <Button
              type="submit"
              disabled={acceptMutation.isPending}
              className="w-full"
            >
              {acceptMutation.isPending ? (
                <>
                  <LoadingSpinner size="sm" className="mr-2" />
                  Creating Account...
                </>
              ) : (
                "Create Account"
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
