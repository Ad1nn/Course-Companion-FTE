import Link from 'next/link'
import Navbar from '@/components/Navbar'

const features = [
  { icon: '📚', title: '10 Structured Chapters', desc: 'From AI agent basics through advanced multi-agent systems and evals.' },
  { icon: '🧠', title: 'Quiz After Every Chapter', desc: 'Reinforce your learning with 5 multiple-choice questions per chapter.' },
  { icon: '📈', title: 'Track Your Progress', desc: 'Dashboard with streak, average score, and per-chapter completion status.' },
]

const tiers = [
  {
    name: 'Free',
    price: '$0',
    chapters: 'Chapters 1–3',
    color: 'border-green-400',
    cta: 'Start Free',
    href: '/signup',
    highlight: false,
  },
  {
    name: 'Premium',
    price: '$29/mo',
    chapters: 'Chapters 1–7',
    color: 'border-violet-500',
    cta: 'Go Premium',
    href: '/signup',
    highlight: true,
  },
  {
    name: 'Pro',
    price: '$49/mo',
    chapters: 'All 10 chapters',
    color: 'border-amber-400',
    cta: 'Go Pro',
    href: '/signup',
    highlight: false,
  },
]

export default function LandingPage() {
  return (
    <>
      <Navbar />

      {/* Hero */}
      <section className="bg-gradient-to-br from-violet-50 to-white px-6 py-24 text-center">
        <div className="mx-auto max-w-3xl">
          <span className="mb-4 inline-block rounded-full bg-violet-100 px-4 py-1 text-sm font-semibold text-violet-700">
            Agentic AI Development Course
          </span>
          <h1 className="mb-6 text-5xl font-extrabold tracking-tight text-gray-900">
            Master Agentic AI<br />
            <span className="text-violet-700">Development</span>
          </h1>
          <p className="mb-8 text-xl text-gray-600">
            10 chapters covering everything from AI agent fundamentals to production-grade
            multi-agent systems, RAG pipelines, and evaluation frameworks.
          </p>
          <Link
            href="/signup"
            className="inline-block rounded-xl bg-violet-600 px-8 py-4 text-lg font-semibold text-white shadow-lg hover:bg-violet-700"
          >
            Start Learning Free →
          </Link>
          <p className="mt-3 text-sm text-gray-400">No credit card required · 3 free chapters</p>
        </div>
      </section>

      {/* Features */}
      <section className="px-6 py-16">
        <div className="mx-auto max-w-4xl">
          <h2 className="mb-10 text-center text-3xl font-bold text-gray-900">Why Course Companion?</h2>
          <div className="grid gap-8 md:grid-cols-3">
            {features.map((f) => (
              <div key={f.title} className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
                <div className="mb-3 text-3xl">{f.icon}</div>
                <h3 className="mb-2 text-lg font-semibold text-gray-900">{f.title}</h3>
                <p className="text-sm text-gray-500">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="bg-gray-50 px-6 py-16">
        <div className="mx-auto max-w-4xl">
          <h2 className="mb-2 text-center text-3xl font-bold text-gray-900">Simple Pricing</h2>
          <p className="mb-10 text-center text-gray-500">Start free, upgrade when you're ready.</p>
          <div className="grid gap-6 md:grid-cols-3">
            {tiers.map((t) => (
              <div
                key={t.name}
                className={`rounded-xl border-2 bg-white p-8 shadow-sm ${t.color} ${t.highlight ? 'scale-105 shadow-lg' : ''}`}
              >
                {t.highlight && (
                  <span className="mb-3 inline-block rounded-full bg-violet-600 px-3 py-0.5 text-xs font-semibold text-white">
                    Most Popular
                  </span>
                )}
                <h3 className="mb-1 text-xl font-bold text-gray-900">{t.name}</h3>
                <p className="mb-4 text-3xl font-extrabold text-gray-900">{t.price}</p>
                <p className="mb-6 text-sm font-medium text-gray-600">{t.chapters}</p>
                <Link
                  href={t.href}
                  className={`block rounded-lg py-2 text-center text-sm font-semibold ${
                    t.highlight
                      ? 'bg-violet-600 text-white hover:bg-violet-700'
                      : 'border border-gray-300 text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  {t.cta}
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white px-6 py-8 text-center text-sm text-gray-400">
        © 2026 Course Companion. Built for the Agentic AI Hackathon.
      </footer>
    </>
  )
}
