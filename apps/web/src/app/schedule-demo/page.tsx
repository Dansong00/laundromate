"use client";

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
      <h1 className="text-3xl font-bold">Schedule a demo</h1>
      <p className="mt-2 text-gray-700">We’ll reach out to coordinate a time that works for you.</p>

      {submitted ? (
        <div className="mt-6 rounded border p-4 bg-green-50 text-green-800">
          Thanks! We’ll be in touch shortly at {form.email}.
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Name</label>
            <input
              className="w-full rounded border px-3 py-2"
              value={form.name}
              onChange={(e) => update("name", e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input
              type="email"
              className="w-full rounded border px-3 py-2"
              value={form.email}
              onChange={(e) => update("email", e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Business name</label>
            <input
              className="w-full rounded border px-3 py-2"
              value={form.company}
              onChange={(e) => update("company", e.target.value)}
            />
          </div>
          <button type="submit" className="rounded bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2">
            Request demo
          </button>
        </form>
      )}
    </main>
  );
}


