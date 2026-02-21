import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserPlus, ShieldCheck } from 'lucide-react';

import api from '../services/api.js';

const Register = () => {
  const [form, setForm] = useState({ username: '', password: '', role: 'user' });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ type: '', text: '' });

    try {
      await api.post('/api/auth/register', form);
      setMessage({ type: 'success', text: 'ลงทะเบียนสำเร็จ! กำลังพากลับไปหน้า Login...' });
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.detail || 'เกิดข้อผิดพลาด หรือมีชื่อผู้ใช้นี้อยู่แล้ว' });
    } finally {
      setLoading(false);
    }
  };

  return (
    // พื้นหลังนอกกรอบมือถือ (สีเทาอมน้ำตาล)
    <div className='flex justify-center bg-stone-200 min-h-screen font-sans'>
      
      {/* 📱 กรอบมือถือ (พื้นหลังสีอกขาวนวล) */}
      <div className='w-full max-w-[480px] bg-stone-50 shadow-2xl flex flex-col min-h-screen relative overflow-x-hidden border-x border-stone-300'>
        
        {/* แถบตกแต่งด้านบนสุด (จุกดำ - โขนแดง - ทอง) */}
        <div className='h-2 w-full bg-stone-900 flex'>
          <div className='w-1/3 bg-rose-600 h-full'></div>
          <div className='w-1/3 bg-amber-500 h-full'></div>
        </div>

        <div className='flex-1 flex flex-col justify-center px-8 py-10'>
          
          {/* --- ส่วนหัว / ไอคอน --- */}
          <div className='mb-8 text-center flex flex-col items-center'>
            <div className='w-20 h-20 bg-stone-900 rounded-full flex items-center justify-center mb-6 shadow-lg shadow-stone-300 border-4 border-stone-100'>
              <UserPlus size={36} className='text-stone-50 ml-1' />
            </div>
            <h2 className='text-3xl font-black text-stone-900 uppercase tracking-tight'>
              Register <span className='text-amber-500'>New</span>
            </h2>
            <p className='text-stone-500 font-medium mt-2'>
              สร้างบัญชีสำหรับกรรมการ/แอดมิน
            </p>
          </div>

          {/* --- ฟอร์มลงทะเบียน --- */}
          <form onSubmit={handleRegister} className='w-full space-y-5'>
            
            <div className='space-y-1'>
              <label className='text-sm font-bold text-stone-700 ml-1'>ชื่อผู้ใช้งาน</label>
              <input 
                type='text' placeholder='ตั้ง Username ใหม่' required
                className='w-full p-4 bg-white border border-stone-200 rounded-2xl focus:ring-2 focus:ring-rose-500 focus:border-rose-500 outline-none transition-all shadow-sm text-stone-900 font-medium placeholder:text-stone-300'
                onChange={(e) => setForm({...form, username: e.target.value})}
              />
            </div>

            <div className='space-y-1'>
              <label className='text-sm font-bold text-stone-700 ml-1'>รหัสผ่าน</label>
              <input 
                type='password' placeholder='ตั้งรหัสผ่าน (ขั้นต่ำ 6 ตัวอักษร)' required
                className='w-full p-4 bg-white border border-stone-200 rounded-2xl focus:ring-2 focus:ring-rose-500 focus:border-rose-500 outline-none transition-all shadow-sm text-stone-900 font-medium placeholder:text-stone-300'
                onChange={(e) => setForm({...form, password: e.target.value})}
              />
            </div>
            
            {/* --- กล่องข้อความแจ้งเตือน --- */}
            {message.text && (
              <div className={`p-3 rounded-xl border text-center transition-all ${
                message.type === 'success' 
                ? 'bg-emerald-50 border-emerald-200 text-emerald-600' 
                : 'bg-rose-50 border-rose-200 text-rose-600'
              }`}>
                <p className='text-sm font-bold'>{message.text}</p>
              </div>
            )}

            {/* ปุ่มกดหลัก (สีดำจุกนก) */}
            <button 
              type='submit' disabled={loading}
              className='w-full mt-2 p-4 flex justify-center items-center gap-2 bg-stone-900 text-white font-bold text-lg rounded-2xl shadow-lg shadow-stone-300 hover:bg-stone-800 active:scale-95 transition-all disabled:bg-stone-300 disabled:shadow-none'
            >
              {loading ? (
                'กำลังบันทึกข้อมูล...'
              ) : (
                <>
                  <ShieldCheck size={22} className='text-amber-500' /> ยืนยันการลงทะเบียน
                </>
              )}
            </button>

          </form>

          {/* --- ลิงก์กลับไป Login --- */}
          <div className='mt-8 text-center'>
            <button 
              type='button'
              onClick={() => navigate('/login')}
              className='text-stone-500 text-sm font-medium hover:text-stone-800 transition-colors'
            >
              มีบัญชีอยู่แล้ว? <span className='text-rose-600 font-bold underline decoration-2 underline-offset-4'>เข้าสู่ระบบที่นี่</span>
            </button>
          </div>

        </div>
      </div>
    </div>
  );
};

export default Register;