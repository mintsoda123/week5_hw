import { useAuth } from '../context/AuthContext'
import { LogOut, Brain, Zap } from 'lucide-react'

export default function Navbar() {
  const { user, usageStatus, login, logout } = useAuth()

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-40">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* 로고 */}
          <div className="flex items-center gap-2">
            <Brain className="w-7 h-7 text-blue-600" />
            <div>
              <span className="font-bold text-gray-900 text-lg">Week 5</span>
              <span className="text-gray-500 text-sm ml-2 hidden sm:inline">딥러닝 핵심 개념</span>
            </div>
          </div>

          {/* 우측 영역 */}
          <div className="flex items-center gap-3">
            {user ? (
              <>
                {/* 사용량 표시 */}
                {usageStatus && !usageStatus.is_premium && (
                  <div className="hidden sm:flex items-center gap-2 bg-gray-100 rounded-full px-3 py-1.5">
                    <div className="flex gap-1">
                      {Array.from({ length: usageStatus.free_limit }).map((_, i) => (
                        <div
                          key={i}
                          className={`w-2 h-2 rounded-full ${
                            i < usageStatus.usage_count
                              ? 'bg-blue-500'
                              : 'bg-gray-300'
                          }`}
                        />
                      ))}
                    </div>
                    <span className="text-xs text-gray-600 font-medium">
                      {usageStatus.usage_count}/{usageStatus.free_limit}
                    </span>
                  </div>
                )}

                {/* 프리미엄 뱃지 */}
                {usageStatus?.is_premium && (
                  <div className="flex items-center gap-1 bg-yellow-100 text-yellow-700 rounded-full px-3 py-1.5">
                    <Zap className="w-3.5 h-3.5" />
                    <span className="text-xs font-semibold">프리미엄</span>
                  </div>
                )}

                {/* 사용자 정보 */}
                <div className="flex items-center gap-2">
                  {user.picture && (
                    <img
                      src={user.picture}
                      alt={user.name}
                      className="w-8 h-8 rounded-full border border-gray-200"
                    />
                  )}
                  <span className="text-sm text-gray-700 font-medium hidden sm:block">
                    {user.name}
                  </span>
                </div>

                {/* 로그아웃 */}
                <button
                  onClick={logout}
                  className="flex items-center gap-1.5 text-gray-500 hover:text-gray-700 text-sm transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  <span className="hidden sm:block">로그아웃</span>
                </button>
              </>
            ) : (
              <button
                onClick={login}
                className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
              >
                <svg className="w-4 h-4" viewBox="0 0 24 24">
                  <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                  <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                Google로 로그인
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
