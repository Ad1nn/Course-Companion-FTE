'use client'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { getSession, clearSession } from '@/lib/auth'

export default function Navbar() {
  const [authenticated, setAuthenticated] = useState(false)
  const router = useRouter()

  useEffect(() => {
    setAuthenticated(!!getSession())
  }, [])

  function handleLogout() {
    clearSession()
    router.push('/login')
  }

  return (
    <nav className="border-b border-gray-200 bg-white px-6 py-4">
      <div className="mx-auto flex max-w-6xl items-center justify-between">
        <Link href="/" className="text-xl font-bold text-violet-700">
          Course Companion
        </Link>
        <div className="flex items-center gap-4">
          {authenticated ? (
            <>
              <Link href="/dashboard" className="text-sm font-medium text-gray-600 hover:text-violet-700">
                Dashboard
              </Link>
              <Link href="/chapters" className="text-sm font-medium text-gray-600 hover:text-violet-700">
                Chapters
              </Link>
              <Link href="/progress" className="text-sm font-medium text-gray-600 hover:text-violet-700">
                Progress
              </Link>
              <button
                onClick={handleLogout}
                className="rounded-lg bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200"
              >
                Log out
              </button>
            </>
          ) : (
            <>
              <Link href="/login" className="text-sm font-medium text-gray-600 hover:text-violet-700">
                Log in
              </Link>
              <Link
                href="/signup"
                className="rounded-lg bg-violet-600 px-4 py-2 text-sm font-medium text-white hover:bg-violet-700"
              >
                Sign up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
