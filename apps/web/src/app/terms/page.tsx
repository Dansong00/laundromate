export default function TermsPage() {
  return (
    <main className="mx-auto max-w-3xl px-4 py-12">
      <h1 className="text-3xl font-bold">Terms of Service</h1>
      <p className="mt-2 text-gray-700">Last updated: {new Date().getFullYear()}</p>
      <div className="prose prose-sm mt-6 text-gray-700">
        <p>These terms are a placeholder and will be updated before launch.</p>
        <p>By using LaundroMate, you agree to our terms and policies.</p>
      </div>
    </main>
  );
}


