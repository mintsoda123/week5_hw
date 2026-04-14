import { createContext, useContext, useState, useEffect } from 'react'
import apiClient from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [usageStatus, setUsageStatus] = useState(null)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      fetchUser()
    } else {
      setLoading(false)
    }
  }, [])

  const fetchUser = async () => {
    try {
      const [userRes, usageRes] = await Promise.all([
        apiClient.get('/auth/me'),
        apiClient.get('/content/usage/status')
      ])
      setUser(userRes.data)
      setUsageStatus(usageRes.data)
    } catch {
      localStorage.removeItem('access_token')
    } finally {
      setLoading(false)
    }
  }

  const refreshUsage = async () => {
    try {
      const res = await apiClient.get('/content/usage/status')
      setUsageStatus(res.data)
    } catch {
      // 무시
    }
  }

  const login = async () => {
    try {
      const res = await apiClient.get('/auth/google/login')
      window.location.href = res.data.url
    } catch {
      window.location.href = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/auth/google/login`
    }
  }

  const loginWithToken = (token) => {
    localStorage.setItem('access_token', token)
    fetchUser()
  }

  const logout = async () => {
    try {
      await apiClient.post('/auth/logout')
    } catch {
      // 무시
    } finally {
      localStorage.removeItem('access_token')
      setUser(null)
      setUsageStatus(null)
    }
  }

  return (
    <AuthContext.Provider value={{
      user,
      loading,
      usageStatus,
      login,
      loginWithToken,
      logout,
      refreshUsage
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth는 AuthProvider 안에서 사용해야 합니다.')
  }
  return context
}
