export default function Home() {
  return (
    <main>
      <section className="mx-auto max-w-6xl px-4 py-16 grid gap-8 md:grid-cols-2 items-center">
        <div>
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight">Run your laundromat, not your tools.</h1>
          <p className="mt-4 text-lg text-gray-600">LaundroMate is the modern platform for pickup & delivery and in‑store wash & fold — orders, customers, and notifications in one place.</p>
          <div className="mt-6 flex items-center gap-3">
            <a href="/auth/register" className="rounded bg-black text-white px-5 py-2">Get started</a>
            <a href="#features" className="rounded border px-5 py-2">Learn more</a>
          </div>
        </div>
        <div className="border rounded-lg p-6 bg-gray-50">
          <div className="h-48 rounded bg-white border grid place-items-center text-gray-500">Product preview</div>
          <ul className="mt-4 grid grid-cols-2 gap-2 text-sm">
            <li>• Online Pickup & Delivery</li>
            <li>• Wash & Fold POS</li>
            <li>• Customer Portal</li>
            <li>• SMS/Email Notifications</li>
          </ul>
        </div>
      </section>
      <section id="features" className="bg-white border-t">
        <div className="mx-auto max-w-6xl px-4 py-12 grid md:grid-cols-3 gap-6">
          <div>
            <h3 className="font-semibold">Pickup & Delivery</h3>
            <p className="text-gray-600 mt-2">Time slots, address validation, estimated pricing.</p>
          </div>
          <div>
            <h3 className="font-semibold">In‑store POS</h3>
            <p className="text-gray-600 mt-2">Fast order intake and status tracking.</p>
          </div>
          <div>
            <h3 className="font-semibold">Customer Accounts</h3>
            <p className="text-gray-600 mt-2">Profile, order history, and notifications.</p>
          </div>
        </div>
      </section>
    </main>
  );
}
