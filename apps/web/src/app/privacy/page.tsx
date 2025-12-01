export default function PrivacyPage() {
  return (
    <main className="mx-auto max-w-3xl px-4 py-12">
      <h1 className="text-3xl font-bold">Privacy Policy</h1>
      <p className="mt-2 text-gray-700">
        Last updated: {new Date().getFullYear()}
      </p>
      <div className="prose prose-sm mt-6 text-gray-700">
        <p>
          This privacy policy is a placeholder and will be updated before
          launch.
        </p>
        <p>We value your privacy and will outline our data practices here.</p>
      </div>
    </main>
  );
}
