import { useState } from 'react'
import { X, Zap, CheckCircle, Loader } from 'lucide-react'
import apiClient from '../api/client'

export default function PaywallModal({ onClose }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleCheckout = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiClient.get('/payment/checkout')
      window.location.href = res.data.checkout_url
    } catch (err) {
      setError(err.response?.data?.detail || '결제 링크 생성에 실패했습니다.')
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 relative">
        {/* 닫기 버튼 */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* 아이콘 */}
        <div className="flex justify-center mb-6">
          <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center">
            <Zap className="w-8 h-8 text-yellow-500" />
          </div>
        </div>

        {/* 제목 */}
        <h2 className="text-2xl font-bold text-gray-900 text-center mb-2">
          무료 사용 한도 초과
        </h2>
        <p className="text-gray-500 text-center mb-6">
          5회 무료 열람을 모두 사용하셨습니다.<br />
          프리미엄으로 업그레이드하고 무제한으로 학습하세요!
        </p>

        {/* 혜택 목록 */}
        <div className="space-y-3 mb-8">
          {[
            '모든 딥러닝 섹션 무제한 열람',
            '코드 예시 다운로드',
            '향후 추가 컨텐츠 무료 제공',
            '이메일 학습 지원',
          ].map((benefit) => (
            <div key={benefit} className="flex items-center gap-3">
              <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
              <span className="text-gray-700 text-sm">{benefit}</span>
            </div>
          ))}
        </div>

        {/* 에러 메시지 */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 rounded-lg p-3 mb-4 text-sm">
            {error}
          </div>
        )}

        {/* CTA 버튼 */}
        <button
          onClick={handleCheckout}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white font-bold py-3.5 rounded-xl transition-colors flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <Loader className="w-5 h-5 animate-spin" />
              처리 중...
            </>
          ) : (
            <>
              <Zap className="w-5 h-5" />
              프리미엄 시작하기
            </>
          )}
        </button>

        <p className="text-xs text-gray-400 text-center mt-4">
          Polar.sh를 통해 안전하게 결제됩니다
        </p>
      </div>
    </div>
  )
}
