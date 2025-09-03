"use client";

import { useAuth } from "@/components/AuthProvider";
import { useToast } from "@/components/ToastProvider";
import { createCustomer, getAuthHeader } from "@/lib/api";
import {
  Alert,
  AlertDescription,
  Button,
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  Input,
  LoadingSpinner,
  Textarea,
} from "@/lib/ui";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function NewCustomerPage() {
  const { isAuthenticated } = useAuth();
  const { notifySuccess, notifyError } = useToast();
  const router = useRouter();
  const [userId, setUserId] = useState<string | null>(null);
  const [preferred_pickup_time, setPreferredPickupTime] = useState("");
  const [special_instructions, setSpecialInstructions] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace("/auth/login");
      return;
    }
    (async () => {
      try {
        const res = await fetch("/api/me", {
          headers: { ...getAuthHeader() },
          cache: "no-store",
        });
        if (!res.ok) throw new Error("Failed to load user");
        const data = await res.json();
        setUserId(data.id);
      } catch (e) {
        setError((e as Error).message);
      }
    })();
  }, [isAuthenticated, router]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!userId) return;
    setLoading(true);
    setError(null);
    try {
      await createCustomer({
        user_id: userId,
        preferred_pickup_time,
        special_instructions,
      });
      notifySuccess("Profile created");
      router.push("/portal");
    } catch (e) {
      const msg = (e as Error).message;
      setError(msg);
      notifyError(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-xl px-4 py-8">
      <Card>
        <CardHeader>
          <CardTitle>Create Your Customer Profile</CardTitle>
        </CardHeader>
        <CardContent>
          {error && (
            <Alert variant="destructive" className="mb-6">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <Input
              label="Preferred Pickup Time"
              value={preferred_pickup_time}
              onChange={(e) => setPreferredPickupTime(e.target.value)}
              placeholder="morning / afternoon / evening"
            />
            <Textarea
              label="Special Instructions"
              value={special_instructions}
              onChange={(e) => setSpecialInstructions(e.target.value)}
              placeholder="Any special handling requirements..."
            />
            <Button
              type="submit"
              disabled={loading || !userId}
              className="w-full"
            >
              {loading ? (
                <>
                  <LoadingSpinner size="sm" className="mr-2" />
                  Saving...
                </>
              ) : (
                "Save Profile"
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </main>
  );
}
