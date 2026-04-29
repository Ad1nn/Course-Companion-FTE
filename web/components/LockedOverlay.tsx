// Constitution Principle IV + SC-003: This component REPLACES ChapterContent.
// It never receives or renders chapter content — the raw content string is never passed here.
export default function LockedOverlay({ requiredTier }: { requiredTier: string }) {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border-2 border-dashed border-gray-200 bg-white p-16 text-center">
      <div className="mb-4 text-5xl">🔒</div>
      <h2 className="mb-2 text-2xl font-bold text-gray-800">Chapter Locked</h2>
      <p className="mb-6 max-w-sm text-gray-500">
        This chapter requires a{' '}
        <span className="font-semibold capitalize text-violet-700">{requiredTier}</span> plan.
        Upgrade to unlock this chapter and all content at this tier.
      </p>
      <a
        href="mailto:admin@coursecompanion.ai?subject=Upgrade Request"
        className="rounded-lg bg-violet-600 px-6 py-3 text-sm font-semibold text-white hover:bg-violet-700"
      >
        Contact to Upgrade
      </a>
      <p className="mt-3 text-xs text-gray-400">
        For demo: use the admin API to upgrade your tier.
      </p>
    </div>
  )
}
