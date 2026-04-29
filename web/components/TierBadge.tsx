import type { Tier } from '@/lib/api'

const styles: Record<Tier, string> = {
  free: 'bg-green-100 text-green-800',
  premium: 'bg-violet-100 text-violet-800',
  pro: 'bg-amber-100 text-amber-800',
}

export default function TierBadge({ tier }: { tier: Tier }) {
  return (
    <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-semibold capitalize ${styles[tier]}`}>
      {tier}
    </span>
  )
}
