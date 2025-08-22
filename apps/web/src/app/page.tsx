export default function Home() {
  return (
    <main>
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-sky-50 to-indigo-50" />
        <div className="relative mx-auto max-w-6xl px-4 py-16 grid gap-8 md:grid-cols-2 items-center">
          <div>
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center rounded-full bg-blue-100 text-blue-800 px-3 py-1 text-xs font-medium">New: LaundroAgent</span>
              <span className="inline-flex items-center rounded-full bg-indigo-100 text-indigo-800 px-3 py-1 text-xs font-medium">Built‑in AI automations</span>
            </div>
            <h1 className="mt-3 text-4xl md:text-5xl font-bold tracking-tight text-gray-900">The operating system for modern laundromats — now AI‑powered</h1>
            <p className="mt-4 text-lg text-gray-700">Smart scheduling, order triage, and customer messaging—handled by AI.</p>
            <p className="mt-2 text-gray-600">Orchestrate orders, staff, and comms with AI agents.</p>
            <div className="mt-6 flex items-center gap-3">
              <a href="/auth/register" className="rounded bg-blue-600 hover:bg-blue-700 text-white px-5 py-2">Get started</a>
              <a href="/learn-more" className="rounded border border-blue-200 text-blue-800 hover:bg-blue-50 px-5 py-2">Learn more</a>
              <a href="/schedule-demo" className="rounded bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2">Schedule a demo</a>
              <a href="/auth/login" className="text-sm text-gray-600 underline">Log in</a>
            </div>
          </div>
          <div className="border rounded-lg p-6 bg-white/80 backdrop-blur">
            <div className="h-48 rounded bg-gradient-to-br from-indigo-50 to-blue-50 border grid place-items-center text-gray-500">Product preview</div>
            <ul className="mt-4 grid grid-cols-2 gap-2 text-sm text-gray-700">
              <li>• Online Pickup & Delivery</li>
              <li>• Wash & Fold POS</li>
              <li>• Customer Portal</li>
              <li>• SMS/Email Notifications</li>
            </ul>
          </div>
        </div>
      </section>
      <section id="how-ai-helps" className="bg-white border-t">
        <div className="mx-auto max-w-6xl px-4 py-12">
          <h2 className="text-2xl font-semibold">How AI helps</h2>
          <div className="mt-6 grid md:grid-cols-3 gap-6">
            <div className="rounded-lg border p-5">
              <h3 className="font-medium">Smart scheduling</h3>
              <p className="text-gray-600 mt-2">Auto-assign pickup windows, balance routes, and flag conflicts.</p>
            </div>
            <div className="rounded-lg border p-5">
              <h3 className="font-medium">Order triage</h3>
              <p className="text-gray-600 mt-2">Detect delays, escalate issues, and suggest next actions.</p>
            </div>
            <div className="rounded-lg border p-5">
              <h3 className="font-medium">Customer messaging</h3>
              <p className="text-gray-600 mt-2">Proactive updates and replies across SMS and email.</p>
            </div>
          </div>
          <div className="mt-8">
            <a href="/schedule-demo" className="inline-flex rounded bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2">Schedule a demo</a>
          </div>
        </div>
      </section>
      <section id="features" className="bg-white border-t">
        <div className="mx-auto max-w-6xl px-4 py-12 grid md:grid-cols-3 gap-6">
          <div className="rounded-lg border p-5 hover:shadow-sm transition">
            <h3 className="font-semibold">Pickup & Delivery</h3>
            <p className="text-gray-600 mt-2">Time slots, address validation, estimated pricing.</p>
          </div>
          <div className="rounded-lg border p-5 hover:shadow-sm transition">
            <h3 className="font-semibold">In‑store POS</h3>
            <p className="text-gray-600 mt-2">Fast order intake and status tracking.</p>
          </div>
          <div className="rounded-lg border p-5 hover:shadow-sm transition">
            <h3 className="font-semibold">Customer Accounts</h3>
            <p className="text-gray-600 mt-2">Profile, order history, and notifications.</p>
          </div>
        </div>
      </section>
    </main>
  );
}
