interface Feature {
  title: string;
  description: string;
}

const features: Feature[] = [
  {
    title: "Pickup & Delivery",
    description:
      "Automated route optimization, driver app, and real-time customer tracking.",
  },
  {
    title: "In-Store POS",
    description:
      "Fast, easy-to-use point of sale for walk-in customers and wash & fold orders.",
  },
  {
    title: "Customer Management",
    description:
      "CRM with order history, preferences, and automated SMS/Email notifications.",
  },
  {
    title: "Business Analytics",
    description:
      "Real-time reporting on revenue, orders, and staff performance.",
  },
];

export function FeaturesSection() {
  return (
    <section className="py-24 bg-gray-50">
      <div className="mx-auto max-w-6xl px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Everything you need to run your shop
          </h2>
          <p className="mt-4 text-lg text-gray-600">
            Powerful tools designed specifically for the laundry industry.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, i) => (
            <div
              key={i}
              className="bg-white p-8 rounded-lg border border-gray-200"
            >
              <h3 className="text-xl font-semibold mb-3 text-gray-900">
                {feature.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
