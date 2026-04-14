import { useAuth } from '../context/AuthContext'
import { Zap, Lock } from 'lucide-react'

export default function UsageBar() {
  const { usageStatus, user } = useAuth()

  if (!user || !usageStatus) return null
  if (usageStatus.is_premium) return null

  const percentage = (usageStatus.usage_count / usageStatus.free_limit) * 100

  return (
    <div className="bg-blue-50 border border-blue-100 rounded-xl p-4">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <Lock className="w-4 h-4 text-blue-500" />
          <span className="text-sm font-semibold text-blue-700">무료 사용량</span>
        </div>
        <span className="text-sm text-blue-600 font-medium">
          {usageStatus.usage_count} / {usageStatus.free_limit}회
        </span>
      </div>
      <div className="w-full bg-blue-100 rounded-full h-2.5">
        <div
          className={`h-2.5 rounded-full transition-all duration-500 ${
            percentage >= 100 ? 'bg-red-500' : percentage >= 80 ? 'bg-orange-500' : 'bg-blue-500'
          }`}
          style={{ width: `${Math.min(percentage, 100)}%` }}
        />
      </div>
      {usageStatus.usage_count >= usageStatus.free_limit ? (
        <p className="text-xs text-red-600 mt-2 font-medium">
          ⚠️ 무료 한도를 모두 사용했습니다. 프리미엄으로 업그레이드하세요!
        </p>
      ) : (
        <p className="text-xs text-blue-500 mt-2">
          남은 무료 열람: <strong>{usageStatus.remaining}회</strong>
        </p>
      )}
    </div>
  )
}
