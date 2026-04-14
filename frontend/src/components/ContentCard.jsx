import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { BookOpen, Lock, CheckCircle, ChevronRight } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

const SECTION_EMOJIS = {
  regularization: '🛡️',
  overfitting: '⚖️',
  data_augmentation: '🖼️',
  transfer_learning: '🧠',
  mnist_cnn: '✍️',
  early_stopping: '⏹️',
  hyperparameter_tuning: '🔧',
  model_evaluation: '📊',
}

const SECTION_COLORS = {
  regularization: 'blue',
  overfitting: 'purple',
  data_augmentation: 'green',
  transfer_learning: 'orange',
  mnist_cnn: 'pink',
  early_stopping: 'blue',
  hyperparameter_tuning: 'purple',
  model_evaluation: 'green',
}

const COLOR_CLASSES = {
  blue: { bg: 'bg-blue-50', border: 'border-blue-100', btn: 'bg-blue-600 hover:bg-blue-700', tag: 'bg-blue-100 text-blue-700' },
  purple: { bg: 'bg-purple-50', border: 'border-purple-100', btn: 'bg-purple-600 hover:bg-purple-700', tag: 'bg-purple-100 text-purple-700' },
  green: { bg: 'bg-green-50', border: 'border-green-100', btn: 'bg-green-600 hover:bg-green-700', tag: 'bg-green-100 text-green-700' },
  orange: { bg: 'bg-orange-50', border: 'border-orange-100', btn: 'bg-orange-600 hover:bg-orange-700', tag: 'bg-orange-100 text-orange-700' },
  pink: { bg: 'bg-pink-50', border: 'border-pink-100', btn: 'bg-pink-600 hover:bg-pink-700', tag: 'bg-pink-100 text-pink-700' },
}

export default function ContentCard({ section, index, isViewed, onPaywallTrigger }) {
  const navigate = useNavigate()
  const { usageStatus } = useAuth()
  const color = SECTION_COLORS[section.id] || 'blue'
  const colors = COLOR_CLASSES[color]

  const isLocked = !usageStatus?.is_premium &&
    !isViewed &&
    usageStatus?.usage_count >= usageStatus?.free_limit

  const handleClick = () => {
    if (isLocked) {
      onPaywallTrigger()
    } else {
      navigate(`/content/${section.id}`)
    }
  }

  return (
    <div
      className={`relative bg-white rounded-xl border ${colors.border} shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden group cursor-pointer`}
      onClick={handleClick}
    >
      {/* 상단 색상 바 */}
      <div className={`h-1.5 ${colors.btn.split(' ')[0]}`} />

      <div className="p-6">
        {/* 헤더 */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-3">
            <span className={`w-9 h-9 flex items-center justify-center rounded-lg text-lg ${colors.bg}`}>
              {SECTION_EMOJIS[section.id]}
            </span>
            <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${colors.tag}`}>
              섹션 {index + 1}
            </span>
          </div>

          {/* 상태 아이콘 */}
          {isViewed ? (
            <CheckCircle className="w-5 h-5 text-green-500" />
          ) : isLocked ? (
            <Lock className="w-5 h-5 text-gray-400" />
          ) : (
            <ChevronRight className="w-5 h-5 text-gray-400 group-hover:text-gray-600 group-hover:translate-x-0.5 transition-transform" />
          )}
        </div>

        {/* 제목 */}
        <h3 className="font-bold text-gray-900 text-lg mb-2 leading-tight">
          {section.title}
        </h3>

        {/* 설명 */}
        <p className="text-gray-500 text-sm leading-relaxed mb-4">
          {section.description}
        </p>

        {/* 버튼 */}
        <div
          className={`flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-semibold text-white transition-colors ${
            isLocked ? 'bg-gray-400' : colors.btn
          }`}
        >
          {isLocked ? (
            <>
              <Lock className="w-4 h-4" />
              잠금됨 (프리미엄 필요)
            </>
          ) : (
            <>
              <BookOpen className="w-4 h-4" />
              {isViewed ? '다시 보기' : '학습하기'}
            </>
          )}
        </div>
      </div>
    </div>
  )
}
