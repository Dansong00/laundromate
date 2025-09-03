"use client";

import {
  Alert,
  AlertDescription,
  Button,
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  Input,
} from "@/lib/ui";
import { useState } from "react";

export default function ScheduleDemoPage() {
  const [form, setForm] = useState({ name: "", email: "", company: "" });
  const [submitted, setSubmitted] = useState(false);

  function update<K extends keyof typeof form>(k: K, v: string) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitted(true);
  }

  return (
    <main className="mx-auto max-w-xl px-4 py-12">
      <Card>
        <CardHeader>
          <CardTitle className="text-3xl">Schedule a Demo</CardTitle>
          <p className="text-gray-700">
            We'll reach out to coordinate a time that works for you.
          </p>
        </CardHeader>
        <CardContent>
          {submitted ? (
            <Alert variant="success" className="mb-6">
              <AlertDescription>
                Thanks! We'll be in touch shortly at{" "}
                <strong>{form.email}</strong>.
              </AlertDescription>
            </Alert>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6">
              <Input
                label="Full Name"
                value={form.name}
                onChange={(e) => update("name", e.target.value)}
                required
                placeholder="Your full name"
              />
              <Input
                label="Email Address"
                type="email"
                value={form.email}
                onChange={(e) => update("email", e.target.value)}
                required
                placeholder="your@email.com"
              />
              <Input
                label="Business Name"
                value={form.company}
                onChange={(e) => update("company", e.target.value)}
                placeholder="Your company or business name"
              />
              <Button type="submit" className="w-full">
                Request Demo
              </Button>
            </form>
          )}
        </CardContent>
      </Card>
    </main>
  );
}
