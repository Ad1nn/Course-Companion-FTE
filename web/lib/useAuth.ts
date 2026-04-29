'use client'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { getSession, type AuthSession } from './auth'

export function useAuth() {
  const [session, setSession] = useState<AuthSession | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const s = getSession()
    if (!s) {
      router.replace('/login')
    } else {
      setSession(s)
    }
    setLoading(false)
  }, [router])

  return { session, loading }
}
