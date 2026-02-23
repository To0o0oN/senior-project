import { Routes, Route, Navigate } from 'react-router-dom';

import { AuthProvider, useAuth } from './context/AuthContext.jsx';
import Layout from './layouts/Layout.jsx';

import Login from './pages/Login.jsx';
import Register from './pages/Register.jsx';
import Home from './pages/Home.jsx';
import SessionSetup from './pages/SessionSetup.jsx';
import Competition from './pages/Competition.jsx';

// จำลอง
const Sandbox = () => <div>Sandbox</div>
const History = () => <div>History</div>
const Admin = () => <div>Admin</div>

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
        <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />

        <Route path="/setup" element={<ProtectedRoute><SessionSetup /></ProtectedRoute>} />
        <Route path="/competition" element={<ProtectedRoute><Competition /></ProtectedRoute>} />
        <Route path="/sandbox" element={<ProtectedRoute><Sandbox /></ProtectedRoute>} />
        <Route path="/history" element={<ProtectedRoute><History /></ProtectedRoute>} />

        <Route path="/admin" element={<ProtectedRoute><Admin /></ProtectedRoute>} />

        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </AuthProvider>
  );
}

export default App;
