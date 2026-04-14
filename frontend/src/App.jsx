import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import Navbar from './components/Navbar'
import HomePage from './pages/HomePage'
import ContentPage from './pages/ContentPage'
import AuthCallbackPage from './pages/AuthCallbackPage'
import PaymentSuccessPage from './pages/PaymentSuccessPage'

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <main>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/content/:sectionId" element={<ContentPage />} />
              <Route path="/auth/callback" element={<AuthCallbackPage />} />
              <Route path="/payment/success" element={<PaymentSuccessPage />} />
            </Routes>
          </main>
        </div>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
