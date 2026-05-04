'use client'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { useTheme } from 'next-themes'
import { getSession } from '@/lib/auth'

function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)
  useEffect(() => setMounted(true), [])
  if (!mounted) return <div className="w-8 h-8" />
  return (
    <button
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      className="rounded-lg p-2 text-gray-500 hover:bg-gray-100 dark:text-slate-400 dark:hover:bg-slate-800 transition-colors"
      aria-label="Toggle theme"
    >
      {theme === 'dark' ? (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707M17.657 17.657l-.707-.707M6.343 6.343l-.707-.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
      ) : (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
      )}
    </button>
  )
}

export default function Navbar() {
  const [authenticated, setAuthenticated] = useState(false)
  const [tier, setTier] = useState<string>('free')
  const router = useRouter()

  useEffect(() => {
    const s = getSession()
    setAuthenticated(!!s)
    if (s) setTier(s.tier)
  }, [])

  return (
    <nav className="sticky top-0 z-50 border-b border-gray-200 dark:border-slate-800 bg-white/80 dark:bg-slate-950/80 backdrop-blur-md px-6 py-3">
      <div className="mx-auto flex max-w-6xl items-center">
        {/* Logo — left */}
        <div className="flex-1">
          <Link href="/" className="text-xl font-bold text-violet-700 dark:text-violet-400">
            Course Companion
          </Link>
        </div>

        {/* Nav links — center */}
        {authenticated && (
          <div className="flex items-center gap-1">
            <Link href="/dashboard" className="rounded-lg px-3 py-2 text-sm font-medium text-gray-600 dark:text-slate-300 hover:bg-gray-100 dark:hover:bg-slate-800 hover:text-violet-700 dark:hover:text-violet-400 transition-colors">
              Dashboard
            </Link>
            <Link href="/chapters" className="rounded-lg px-3 py-2 text-sm font-medium text-gray-600 dark:text-slate-300 hover:bg-gray-100 dark:hover:bg-slate-800 hover:text-violet-700 dark:hover:text-violet-400 transition-colors">
              Chapters
            </Link>
            <Link href="/progress" className="rounded-lg px-3 py-2 text-sm font-medium text-gray-600 dark:text-slate-300 hover:bg-gray-100 dark:hover:bg-slate-800 hover:text-violet-700 dark:hover:text-violet-400 transition-colors">
              Progress
            </Link>
            <Link href="/adaptive" className="rounded-lg px-3 py-2 text-sm font-medium text-amber-600 dark:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-950 transition-colors">
              AI Tutor ✦
            </Link>
          </div>
        )}

        {/* Right side */}
        <div className="flex flex-1 items-center justify-end gap-2">
          <ThemeToggle />
          {authenticated ? (
            <Link
              href="/profile"
              className="flex items-center gap-2 rounded-lg border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-1.5 text-sm font-medium text-gray-700 dark:text-slate-300 hover:border-violet-300 dark:hover:border-violet-600 transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              {tier === 'pro' && <span className="rounded-full bg-amber-100 dark:bg-amber-900 px-1.5 py-0.5 text-xs font-semibold text-amber-700 dark:text-amber-300">Pro</span>}
              {tier === 'premium' && <span className="rounded-full bg-violet-100 dark:bg-violet-900 px-1.5 py-0.5 text-xs font-semibold text-violet-700 dark:text-violet-300">Premium</span>}
            </Link>
          ) : (
            <>
              <Link href="/login" className="rounded-lg px-3 py-2 text-sm font-medium text-gray-600 dark:text-slate-300 hover:text-violet-700 transition-colors">
                Log in
              </Link>
              <Link href="/signup" className="rounded-lg bg-violet-600 px-4 py-2 text-sm font-medium text-white hover:bg-violet-700 transition-colors">
                Sign up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
