'use client'
import { useEffect, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '@/lib/useAuth'
import { setSession } from '@/lib/auth'
import { apiUpgradeTier, type Tier } from '@/lib/api'

const TIER_DETAILS: Record<string, { label: string; price: string; chapters: string; features: string[]; color: string }> = {
  premium: {
    label: 'Premium',
    price: '$29/mo',
    chapters: 'Chapters 1–7',
    features: ['All 7 core chapters', '35 quiz questions', 'Progress tracking', 'Day streak'],
    color: 'border-violet-500',
  },
  pro: {
    label: 'Pro',
    price: '$49/mo',
    chapters: 'All 10 chapters',
    features: ['All 10 chapters', '50 quiz questions', 'AI adaptive learning path', 'AI-graded assessments', 'Progress tracking', 'Day streak'],
    color: 'border-amber-400',
  },
}

export default function UpgradePage() {
  const { session, loading } = useAuth()
  const router = useRouter()
  const searchParams = useSearchParams()
  const tier = searchParams.get('tier') ?? 'pro'
  const details = TIER_DETAILS[tier]

  const [upgrading, setUpgrading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!loading && !session) {
      router.push(`/login?redirect=/upgrade?tier=${tier}`)
    }
  }, [loading, session, router, tier])

  if (loading || !session) return null

  if (!details) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-500">Invalid tier. <Link href="/" className="text-violet-600">Go home</Link></p>
      </div>
    )
  }

  // Already on this tier or higher
  const TIER_ORDER: Record<string, number> = { free: 0, premium: 1, pro: 2 }
  if (TIER_ORDER[session.tier] >= TIER_ORDER[tier]) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4">
        <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-lg text-center">
          <div className="mb-4 text-5xl">✅</div>
          <h1 className="mb-2 text-2xl font-bold text-gray-900">You&apos;re already on {session.tier}!</h1>
          <p className="mb-6 text-gray-500">You already have access to all {details.label} features.</p>
          <Link
            href="/chapters"
            className="inline-block rounded-lg bg-violet-600 px-6 py-2.5 font-semibold text-white hover:bg-violet-700"
          >
            Go to Chapters →
          </Link>
        </div>
      </div>
    )
  }

  async function handleUpgrade() {
    setError('')
    setUpgrading(true)
    try {
      const result = await apiUpgradeTier(session!.access_token, tier as Tier)
      setSession({ ...session!, tier: result.tier })
      router.push('/dashboard')
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Upgrade failed. Please try again.')
    } finally {
      setUpgrading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md">
        <div className={`rounded-2xl border-2 bg-white p-8 shadow-lg ${details.color}`}>
          <div className="mb-6 text-center">
            <Link href="/" className="text-2xl font-bold text-violet-700">Course Companion</Link>
            <h1 className="mt-4 text-2xl font-bold text-gray-900">Upgrade to {details.label}</h1>
            <p className="mt-1 text-3xl font-extrabold text-gray-900">{details.price}</p>
            <p className="mt-1 text-sm text-gray-500">{details.chapters}</p>
          </div>

          <ul className="mb-6 space-y-2">
            {details.features.map((f) => (
              <li key={f} className="flex items-center gap-2 text-sm text-gray-700">
                <span className="text-green-500 font-bold">✓</span> {f}
              </li>
            ))}
          </ul>

          {error && (
            <p className="mb-4 rounded-lg bg-red-50 px-4 py-2 text-sm text-red-600">{error}</p>
          )}

          <button
            onClick={handleUpgrade}
            disabled={upgrading}
            className="w-full rounded-lg bg-violet-600 py-2.5 text-sm font-semibold text-white hover:bg-violet-700 disabled:opacity-60"
          >
            {upgrading ? 'Upgrading…' : `Upgrade to ${details.label} →`}
          </button>

          <p className="mt-4 text-center text-xs text-gray-400">
            Demo mode — no payment required
          </p>
        </div>

        <p className="mt-4 text-center text-sm text-gray-500">
          <Link href="/dashboard" className="text-violet-600 hover:text-violet-700">← Back to Dashboard</Link>
        </p>
      </div>
    </div>
  )
}
