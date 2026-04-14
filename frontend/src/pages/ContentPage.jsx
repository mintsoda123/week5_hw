import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, BookOpen, Code, FileText, Loader, AlertCircle } from 'lucide-react'
import apiClient from '../api/client'
import CodeBlock from '../components/CodeBlock'
import PaywallModal from '../components/PaywallModal'
import { useAuth } from '../context/AuthContext'

// 간단한 마크다운 렌더러 (## ### 지원)
function SimpleMarkdown({ text }) {
  const lines = text.split('\n')
  return (
    <div className="prose max-w-none">
      {lines.map((line, i) => {
        if (line.startsWith('## ')) return <h2 key={i}>{line.slice(3)}</h2>
        if (line.startsWith('### ')) return <h3 key={i}>{line.slice(4)}</h3>
        if (line.startsWith('- **')) {
          const match = line.match(/- \*\*(.+?)\*\*:?\s*(.*)/)
          return match ? (
            <p key={i} className="text-gray-600 leading-relaxed mb-1">
              • <strong>{match[1]}</strong>{match[2] ? `: ${match[2]}` : ''}
            </p>
          ) : <p key={i} className="text-gray-600">{line.slice(2)}</p>
        }
        if (line.startsWith('- ')) return (
          <p key={i} className="text-gray-600 leading-relaxed mb-1 pl-4">
            • {line.slice(2)}
          </p>
        )
        if (line.startsWith('| ') || line.startsWith('|---')) {
          return null // 테이블은 별도 처리
        }
        if (line.trim() === '') return <br key={i} />
        return <p key={i} className="text-gray-600 leading-relaxed mb-2">{line}</p>
      })}
    </div>
  )
}

// 탭 버튼 컴포넌트
function TabButton({ active, onClick, icon: Icon, label }) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${
        active
          ? 'bg-blue-600 text-white'
          : 'text-gray-600 hover:bg-gray-100'
      }`}
    >
      <Icon className="w-4 h-4" />
      {label}
    </button>
  )
}

export default function ContentPage() {
  const { sectionId } = useParams()
  const navigate = useNavigate()
  const { refreshUsage } = useAuth()
  const [section, setSection] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showPaywall, setShowPaywall] = useState(false)
  const [activeTab, setActiveTab] = useState('content')

  useEffect(() => {
    fetchSection()
  }, [sectionId])

  const fetchSection = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiClient.get(`/content/${sectionId}`)
      setSection(res.data)
      refreshUsage()
      // 열람 기록 저장
      const viewed = JSON.parse(localStorage.getItem('viewed_sections') || '[]')
      if (!viewed.includes(sectionId)) {
        localStorage.setItem('viewed_sections', JSON.stringify([...viewed, sectionId]))
      }
    } catch (err) {
      if (err.response?.status === 402) {
        setShowPaywall(true)
        setError('무료 사용 한도를 초과했습니다.')
      } else {
        setError(err.response?.data?.detail || '컨텐츠를 불러오는데 실패했습니다.')
      }
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader className="w-10 h-10 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-500">컨텐츠를 불러오는 중...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* 뒤로가기 */}
      <button
        onClick={() => navigate('/')}
        className="flex items-center gap-2 text-gray-500 hover:text-gray-700 mb-6 transition-colors group"
      >
        <ArrowLeft className="w-4 h-4 group-hover:-translate-x-0.5 transition-transform" />
        목록으로 돌아가기
      </button>

      {/* 에러 상태 (결제 필요 제외) */}
      {error && !showPaywall && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-6 flex items-center gap-3">
          <AlertCircle className="w-6 h-6 text-red-500 flex-shrink-0" />
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {/* 컨텐츠 */}
      {section && (
        <>
          {/* 헤더 */}
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-8 mb-6">
            <h1 className="text-3xl font-extrabold text-gray-900 mb-3">
              {section.title}
            </h1>
            <p className="text-gray-500 text-lg">{section.description}</p>
          </div>

          {/* 탭 네비게이션 */}
          <div className="flex gap-2 mb-6">
            <TabButton
              active={activeTab === 'content'}
              onClick={() => setActiveTab('content')}
              icon={BookOpen}
              label="개념 설명"
            />
            {section.code_example && (
              <TabButton
                active={activeTab === 'code'}
                onClick={() => setActiveTab('code')}
                icon={Code}
                label="코드 예시"
              />
            )}
            {section.result_description && (
              <TabButton
                active={activeTab === 'result'}
                onClick={() => setActiveTab('result')}
                icon={FileText}
                label="결과 해석"
              />
            )}
          </div>

          {/* 탭 내용 */}
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-8">
            {activeTab === 'content' && (
              <SimpleMarkdown text={section.content} />
            )}
            {activeTab === 'code' && section.code_example && (
              <div>
                <h2 className="text-xl font-bold text-gray-800 mb-4">코드 예시</h2>
                <CodeBlock code={section.code_example} language="python" />
              </div>
            )}
            {activeTab === 'result' && section.result_description && (
              <div>
                <h2 className="text-xl font-bold text-gray-800 mb-4">결과 해석</h2>
                <div className="bg-blue-50 border border-blue-100 rounded-lg p-5">
                  <p className="text-blue-800 leading-relaxed">{section.result_description}</p>
                </div>
              </div>
            )}
          </div>

          {/* 이전/다음 네비게이션 */}
          <div className="flex justify-between mt-6">
            <button
              onClick={() => navigate('/')}
              className="btn-secondary flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              목록으로
            </button>
          </div>
        </>
      )}

      {/* 결제 모달 */}
      {showPaywall && (
        <PaywallModal onClose={() => { setShowPaywall(false); navigate('/') }} />
      )}
    </div>
  )
}
