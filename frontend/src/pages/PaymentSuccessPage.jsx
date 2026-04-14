import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { CheckCircle } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

export default function PaymentSuccessPage() {
  const navigate = useNavigate()
  const { refreshUsage } = useAuth()

  useEffect(() => {
    refreshUsage()
    const timer = setTimeout(() => navigate('/'), 4000)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <CheckCircle className="w-12 h-12 text-green-500" />
        </div>
        <h1 className="text-3xl font-extrabold text-gray-900 mb-3">결제 완료!</h1>
        <p className="text-gray-500 mb-6">
          프리미엄 멤버십이 활성화되었습니다.<br />
          이제 모든 컨텐츠를 무제한으로 이용할 수 있습니다!
        </p>
        <p className="text-sm text-gray-400">4초 후 홈으로 이동합니다...</p>
        <button
          onClick={() => navigate('/')}
          className="mt-4 btn-primary"
        >
          지금 바로 시작하기
        </button>
      </div>
    </div>
  )
}
