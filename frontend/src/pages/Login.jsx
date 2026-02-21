import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LogIn, Fingerprint } from 'lucide-react';

import api from '../services/api.js';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // FastAPI มักจะรับข้อมูลแบบ Form Data สำหรับ Login
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await api.post('/api/auth/login', formData);
      
      // เรียกใช้ฟังก์ชัน login จาก Context
      login({ username: username, role: response.data.role }, response.data.access_token);
      
      // เมื่อสำเร็จ ให้ไปที่หน้าหลัก
      navigate('/');
    } catch (err) {
      setError('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center bg-stone-200 min-h-screen font-sans">
      
      {/* 📱 กรอบมือถือ (พื้นหลังสีอกขาวนวล) */}
      <div className="w-full max-w-[480px] bg-stone-50 shadow-2xl flex flex-col min-h-screen relative overflow-x-hidden border-x border-stone-300">
        
        {/* แถบตกแต่งด้านบนสุด (จุกดำ - โขนแดง) */}
        <div className="h-2 w-full bg-stone-900 flex">
          <div className="w-1/3 bg-rose-600 h-full"></div>
          <div className="w-1/3 bg-amber-500 h-full"></div>
        </div>

        <div className="flex-1 flex flex-col justify-center px-8 py-12">
          
          {/* --- ส่วนหัว / โลโก้ --- */}
          <div className="mb-10 text-center flex flex-col items-center">
            <div className="w-20 h-20 bg-stone-900 rounded-full flex items-center justify-center mb-6 shadow-lg shadow-stone-300 border-4 border-stone-100">
              <span className="text-4xl">🐦</span>
            </div>
            <h2 className="text-3xl font-black text-stone-900 uppercase tracking-tight">
              Bird Score <span className="text-rose-600">AI</span>
            </h2>
            <p className="text-stone-500 font-medium mt-2">
              ระบบผู้ช่วยตัดสินนกปรอดหัวโขน
            </p>
          </div>

          {/* --- ฟอร์มล็อกอิน --- */}
          <form onSubmit={handleLogin} className="w-full space-y-5">
            
            <div className="space-y-1">
              <label className="text-sm font-bold text-stone-700 ml-1">ชื่อผู้ใช้งาน</label>
              <input 
                type="text" placeholder="ระบุ Username"
                className="w-full p-4 bg-white border border-stone-200 rounded-2xl focus:ring-2 focus:ring-rose-500 focus:border-rose-500 outline-none transition-all shadow-sm text-stone-900 font-medium placeholder:text-stone-300"
                value={username} onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>

            <div className="space-y-1">
              <label className="text-sm font-bold text-stone-700 ml-1">รหัสผ่าน</label>
              <input 
                type="password" placeholder="••••••••"
                className="w-full p-4 bg-white border border-stone-200 rounded-2xl focus:ring-2 focus:ring-rose-500 focus:border-rose-500 outline-none transition-all shadow-sm text-stone-900 font-medium placeholder:text-stone-300"
                value={password} onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            
            {error && (
              <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-center">
                <p className="text-rose-600 text-sm font-bold">{error}</p>
              </div>
            )}

            {/* ปุ่มกด (สีโขนแดง) */}
            <button 
              type="submit" disabled={loading}
              className="w-full mt-4 p-4 flex justify-center items-center gap-2 bg-rose-600 text-white font-bold text-lg rounded-2xl shadow-lg shadow-rose-200 hover:bg-rose-700 active:scale-95 transition-all disabled:bg-stone-300 disabled:shadow-none"
            >
              {loading ? (
                'กำลังตรวจสอบ...'
              ) : (
                <>
                  <LogIn size={22} /> เข้าสู่ระบบ
                </>
              )}
            </button>

          </form>

          {/* --- ลิงก์ลงทะเบียน --- */}
          <div className="mt-8 text-center">
            <button 
              type="button"
              onClick={() => navigate('/register')}
              className="text-stone-500 text-sm font-medium transition-colors"
            >
              ผู้ใช้ใหม่? <span className="text-amber-600 hover:text-amber-700 font-bold underline decoration-2 underline-offset-4 cursor-pointer">ลงทะเบียนที่นี่</span>
            </button>
          </div>

        </div>

        {/* --- กิมมิคลายนิ้วมือด้านล่าง --- */}
        <div className="py-6 flex justify-center text-stone-300">
          <Fingerprint size={32} opacity={0.5} />
        </div>

      </div>
    </div>
  );
};

export default Login;