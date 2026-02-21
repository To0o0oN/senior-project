import { Routes, Route, Navigate } from 'react-router-dom';

import { AuthProvider, useAuth } from './context/AuthContext.jsx';
import Layout from './layouts/Layout.jsx';

import Login from './pages/Login.jsx';
import Register from './pages/Register.jsx';

const ProtectedRoute = ({ children }) => {
  const { user } = useAuth();
  return user ? <Layout>{children}</Layout> : <Navigate to="/login" />;
};

const App = () => {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        {/* หน้าที่ต้อง Login ก่อนถึงจะเห็น */}
        <Route path="/" element={
          <ProtectedRoute>
            <div className="text-center pt-10">
              <h1 className="text-2xl font-bold">ยินดีต้อนรับเข้าสู่ระบบ!</h1>
              <p className="text-gray-500 mt-2">ตอนนี้คุณอยู่ในหน้า Dashboard แล้วครับ</p>
            </div>
          </ProtectedRoute>
        } />

        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </AuthProvider>
  );
}

export default App;
