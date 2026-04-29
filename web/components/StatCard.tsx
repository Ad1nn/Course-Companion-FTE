export default function StatCard({
  label,
  value,
  icon,
}: {
  label: string
  value: string | number
  icon?: string
}) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      {icon && <div className="mb-2 text-2xl">{icon}</div>}
      <p className="text-sm font-medium text-gray-500">{label}</p>
      <p className="mt-1 text-3xl font-bold text-gray-900">{value}</p>
    </div>
  )
}
