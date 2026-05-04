import Link from 'next/link'
import Navbar from '@/components/Navbar'

const features = [
  { icon: '📚', title: '10 Structured Chapters', desc: 'From AI agent basics through advanced multi-agent systems, RAG pipelines, and evaluation frameworks.' },
  { icon: '🧠', title: 'Quiz After Every Chapter', desc: 'Reinforce learning with 5 multiple-choice questions per chapter. Instant feedback on every answer.' },
  { icon: '📈', title: 'Track Your Progress', desc: 'Dashboard with day streak, average score, and per-chapter completion status.' },
  { icon: '🤖', title: 'AI Adaptive Learning', desc: 'GPT-4o analyses your progress and recommends exactly what to study next. Pro tier.' },
  { icon: '✍️', title: 'AI-Graded Assessments', desc: 'Write free-form answers and get detailed AI feedback on your understanding. Pro tier.' },
  { icon: '⚡', title: '24/7 Available', desc: 'Learn at your own pace, anytime. No schedules, no waiting for a human tutor.' },
]

const tiers = [
  {
    name: 'Free',
    price: '$0',
    period: '',
    chapters: 'Chapters 1–3',
    features: ['3 free chapters', '15 quiz questions', 'Progress tracking'],
    color: 'border-gray-200 dark:border-slate-700',
    cta: 'Start Free',
    href: '/signup',
    highlight: false,
  },
  {
    name: 'Premium',
    price: '$29',
    period: '/mo',
    chapters: 'Chapters 1–7',
    features: ['7 chapters', '35 quiz questions', 'Progress tracking', 'Day streak'],
    color: 'border-violet-500',
    cta: 'Go Premium',
    href: '/upgrade?tier=premium',
    highlight: true,
  },
  {
    name: 'Pro',
    price: '$49',
    period: '/mo',
    chapters: 'All 10 chapters',
    features: ['All 10 chapters', '50 quiz questions', 'AI adaptive learning path', 'AI-graded assessments', 'Full progress tracking'],
    color: 'border-amber-400',
    cta: 'Go Pro',
    href: '/upgrade?tier=pro',
    highlight: false,
  },
]

const workflow = [
  { icon: '👤', label: 'You', desc: 'Read & learn' },
  { icon: '📚', label: 'Chapters', desc: '10 structured lessons' },
  { icon: '🤖', label: 'AI Agent', desc: 'Adapts to your pace' },
  { icon: '🧠', label: 'Knowledge', desc: 'Deep understanding' },
]

export default function LandingPage() {
  return (
    <div className="dark:bg-slate-950">
      <Navbar />

      {/* Hero */}
      <section className="relative overflow-hidden bg-slate-950 px-6 py-28 text-center">
        {/* Background gradient orbs */}
        <div className="pointer-events-none absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 left-1/4 h-96 w-96 rounded-full bg-violet-600/20 blur-3xl" />
          <div className="absolute -bottom-20 right-1/4 h-80 w-80 rounded-full bg-indigo-600/20 blur-3xl" />
          <div className="absolute top-1/2 left-1/2 h-64 w-64 -translate-x-1/2 -translate-y-1/2 rounded-full bg-purple-600/10 blur-3xl" />
        </div>

        {/* Dot grid overlay */}
        <div
          className="pointer-events-none absolute inset-0 opacity-20"
          style={{ backgroundImage: 'radial-gradient(circle, #6d28d9 1px, transparent 1px)', backgroundSize: '32px 32px' }}
        />

        <div className="relative mx-auto max-w-4xl">
          <span className="mb-6 inline-flex items-center gap-2 rounded-full border border-violet-500/30 bg-violet-500/10 px-4 py-1.5 text-sm font-medium text-violet-300">
            <span className="h-1.5 w-1.5 rounded-full bg-violet-400 animate-pulse" />
            Agentic AI Development Course
          </span>

          <h1 className="mb-6 text-5xl font-extrabold tracking-tight text-white md:text-6xl">
            Master{' '}
            <span className="bg-gradient-to-r from-violet-400 to-indigo-400 bg-clip-text text-transparent">
              Agentic AI
            </span>
            <br />Development
          </h1>

          <p className="mx-auto mb-10 max-w-2xl text-lg text-slate-400">
            10 structured chapters covering everything from AI agent fundamentals to production-grade
            multi-agent systems, RAG pipelines, and evaluation frameworks.
          </p>

          <div className="flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
            <Link
              href="/signup"
              className="rounded-xl bg-violet-600 px-8 py-4 text-base font-semibold text-white shadow-lg shadow-violet-500/25 hover:bg-violet-500 transition-all hover:shadow-violet-500/40"
            >
              Start Learning Free →
            </Link>
            <Link
              href="/login"
              className="rounded-xl border border-slate-700 px-8 py-4 text-base font-semibold text-slate-300 hover:border-slate-500 hover:text-white transition-all"
            >
              Log In
            </Link>
          </div>
          <p className="mt-4 text-sm text-slate-500">No credit card required · 3 chapters free forever</p>

          {/* Agent workflow visualization */}
          <div className="mt-16 flex items-center justify-center gap-2 md:gap-4">
            {workflow.map((item, i) => (
              <div key={item.label} className="flex items-center gap-2 md:gap-4">
                <div className="flex flex-col items-center gap-2">
                  <div className="flex h-14 w-14 items-center justify-center rounded-2xl border border-slate-700 bg-slate-900 text-2xl shadow-lg">
                    {item.icon}
                  </div>
                  <span className="text-xs font-semibold text-slate-300">{item.label}</span>
                  <span className="hidden text-xs text-slate-500 md:block">{item.desc}</span>
                </div>
                {i < workflow.length - 1 && (
                  <div className="mb-6 flex items-center gap-1 text-violet-500">
                    <div className="h-px w-6 md:w-10 bg-gradient-to-r from-violet-500/50 to-violet-500" />
                    <svg className="h-3 w-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="bg-white dark:bg-slate-900 px-6 py-20">
        <div className="mx-auto max-w-5xl">
          <h2 className="mb-3 text-center text-3xl font-bold text-gray-900 dark:text-slate-100">Everything you need to master Agentic AI</h2>
          <p className="mb-12 text-center text-gray-500 dark:text-slate-400">Structured learning with real AI-powered features</p>
          <div className="grid gap-6 md:grid-cols-3">
            {features.map((f) => (
              <div key={f.title} className="group rounded-2xl border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-950 p-6 shadow-sm hover:border-violet-300 dark:hover:border-violet-700 hover:shadow-md transition-all">
                <div className="mb-3 text-3xl">{f.icon}</div>
                <h3 className="mb-2 font-semibold text-gray-900 dark:text-slate-100">{f.title}</h3>
                <p className="text-sm text-gray-500 dark:text-slate-400">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="bg-gray-50 dark:bg-slate-950 px-6 py-20">
        <div className="mx-auto max-w-4xl">
          <h2 className="mb-3 text-center text-3xl font-bold text-gray-900 dark:text-slate-100">Simple, transparent pricing</h2>
          <p className="mb-12 text-center text-gray-500 dark:text-slate-400">Start free, upgrade when you're ready.</p>
          <div className="grid gap-6 md:grid-cols-3">
            {tiers.map((t) => (
              <div
                key={t.name}
                className={`relative rounded-2xl border-2 bg-white dark:bg-slate-900 p-8 shadow-sm transition-all ${t.color} ${t.highlight ? 'scale-105 shadow-xl shadow-violet-500/10' : ''}`}
              >
                {t.highlight && (
                  <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-violet-600 px-4 py-0.5 text-xs font-semibold text-white shadow">
                    Most Popular
                  </span>
                )}
                <h3 className="mb-1 text-xl font-bold text-gray-900 dark:text-slate-100">{t.name}</h3>
                <div className="mb-1 flex items-baseline gap-0.5">
                  <span className="text-3xl font-extrabold text-gray-900 dark:text-slate-100">{t.price}</span>
                  <span className="text-sm text-gray-400 dark:text-slate-500">{t.period}</span>
                </div>
                <p className="mb-5 text-sm font-medium text-gray-500 dark:text-slate-400">{t.chapters}</p>
                <ul className="mb-6 space-y-2">
                  {t.features.map((f) => (
                    <li key={f} className="flex items-center gap-2 text-sm text-gray-600 dark:text-slate-400">
                      <span className="text-violet-500">✓</span> {f}
                    </li>
                  ))}
                </ul>
                <Link
                  href={t.href}
                  className={`block rounded-xl py-2.5 text-center text-sm font-semibold transition-all ${
                    t.highlight
                      ? 'bg-violet-600 text-white hover:bg-violet-500 shadow-lg shadow-violet-500/20'
                      : 'border border-gray-200 dark:border-slate-700 text-gray-700 dark:text-slate-300 hover:border-violet-300 dark:hover:border-violet-600 hover:text-violet-600'
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
      <footer className="border-t border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-900 px-6 py-8 text-center text-sm text-gray-400 dark:text-slate-500">
        © 2026 Course Companion. Built for the Agentic AI Hackathon.
      </footer>
    </div>
  )
}
