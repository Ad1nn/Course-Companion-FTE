export interface AuthSession {
  access_token: string
  user_id: string
  email: string
  tier: 'free' | 'premium' | 'pro'
}

const KEY = 'cc_session'

export function getSession(): AuthSession | null {
  if (typeof window === 'undefined') return null
  try {
    const raw = localStorage.getItem(KEY)
    return raw ? (JSON.parse(raw) as AuthSession) : null
  } catch {
    return null
  }
}

export function setSession(session: AuthSession) {
  localStorage.setItem(KEY, JSON.stringify(session))
  // Set a cookie so Next.js middleware can detect authenticated state
  document.cookie = `cc_auth=1; path=/; max-age=86400; SameSite=Lax`
}

export function clearSession() {
  localStorage.removeItem(KEY)
  document.cookie = 'cc_auth=; path=/; max-age=0'
}
