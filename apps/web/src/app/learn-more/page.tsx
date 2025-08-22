export default function LearnMorePage() {
  return (
    <main className="mx-auto max-w-6xl px-4 py-12">
      <h1 className="text-3xl font-bold">Learn more</h1>
      <p className="mt-2 text-gray-700">A closer look at LaundroMate’s features.</p>

      <section className="mt-8 grid md:grid-cols-2 gap-6">
        <div className="rounded-lg border p-5">
          <h2 className="font-semibold">Pickup & Delivery</h2>
          <ul className="mt-2 list-disc list-inside text-gray-700">
            <li>Address validation and saved addresses</li>
            <li>Time slots and route planning</li>
            <li>Order summaries and estimates</li>
          </ul>
        </div>
        <div className="rounded-lg border p-5">
          <h2 className="font-semibold">Wash & Fold POS</h2>
          <ul className="mt-2 list-disc list-inside text-gray-700">
            <li>Fast order intake</li>
            <li>Status tracking from Received → Completed</li>
            <li>Weight, itemization, and notes</li>
          </ul>
        </div>
        <div className="rounded-lg border p-5">
          <h2 className="font-semibold">Customer Accounts</h2>
          <ul className="mt-2 list-disc list-inside text-gray-700">
            <li>Profile and preferences</li>
            <li>Order history and receipts</li>
            <li>Saved payment methods (future)</li>
          </ul>
        </div>
        <div className="rounded-lg border p-5">
          <h2 className="font-semibold">Notifications</h2>
          <ul className="mt-2 list-disc list-inside text-gray-700">
            <li>SMS and email updates</li>
            <li>Proactive delay alerts</li>
            <li>Agent-assisted replies (AI)</li>
          </ul>
        </div>
      </section>

      <section className="mt-10 grid md:grid-cols-2 gap-6">
        <div className="rounded-lg border p-6 bg-white">
          <h2 className="text-xl font-semibold">Analytics (Coming soon)</h2>
          <p className="text-gray-700 mt-2">Dashboards for orders, revenue, retention, and route efficiency.</p>
        </div>
        <div className="rounded-lg border p-6 bg-white">
          <h2 className="text-xl font-semibold">Accounting (Coming soon)</h2>
          <p className="text-gray-700 mt-2">Integrations with QuickBooks and Xero for reconciliation.</p>
        </div>
        <div className="rounded-lg border p-6 bg-white">
          <h2 className="text-xl font-semibold">Integrations (Coming soon)</h2>
          <p className="text-gray-700 mt-2">Square and Shopify to unify catalog, POS, and online orders.</p>
        </div>
        <div className="rounded-lg border p-6 bg-white">
          <h2 className="text-xl font-semibold">AI Voice Assistant (Coming soon)</h2>
          <p className="text-gray-700 mt-2">Voice‑powered customer service and call summaries.</p>
        </div>
      </section>

      <section className="mt-10 rounded-lg border p-6 bg-white">
        <h2 className="text-xl font-semibold">Ready to see it in action?</h2>
        <p className="text-gray-700 mt-2">Schedule a 30‑minute walkthrough tailored to your store.</p>
        <a href="/schedule-demo" className="inline-flex mt-4 rounded bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2">Schedule a demo</a>
      </section>
    </main>
  );
}


