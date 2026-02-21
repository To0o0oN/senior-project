import { useNavigate } from 'react-router-dom';
import { PlayCircle, Beaker, ClipboardList, ShieldAlert } from 'lucide-react';

import { useAuth } from '../context/AuthContext.jsx';

const Home = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  return (
    <div className='flex flex-col h-full animate-in fade-in duration-500 pb-6'>
      
      {/* --- ส่วนต้อนรับ --- */}
      <div className='mb-8 mt-2'>
        <h2 className='text-2xl font-black text-stone-900 tracking-tight'>
          สวัสดี, <span className='text-rose-600'>{user?.username || 'กรรมการ'}</span>
        </h2>
        <p className='text-stone-500 font-medium mt-1'>
          เลือกเมนูที่ต้องการเพื่อเริ่มการทำงาน
        </p>
      </div>

      {/* --- เมนูหลัก (Card Buttons) --- */}
      <div className='flex flex-col gap-4'>
        
        {/* 1. ปุ่มเริ่มการแข่งขัน (เด่นที่สุด - โขนแดง) */}
        <button 
          onClick={() => navigate('/setup')}
          className='group relative w-full p-6 bg-gradient-to-br from-rose-500 to-rose-700 rounded-3xl shadow-lg shadow-rose-200 text-left overflow-hidden active:scale-[0.98] transition-all'
        >
          {/* ลายกราฟิกพื้นหลังการ์ด */}
          <div className='absolute -right-6 -top-6 w-32 h-32 bg-white opacity-10 rounded-full group-hover:scale-110 transition-transform'></div>
          
          <div className='relative flex items-center justify-between z-10'>
            <div>
              <h3 className='text-2xl font-black text-white mb-1'>โหมดจำลองการแข่งขัน</h3>
              <p className='text-rose-100 text-sm font-medium'>เข้าสู่โหมดการแข่งขัน 4 ยก</p>
            </div>
            <div className='bg-white/20 p-3 rounded-2xl backdrop-blur-sm text-white'>
              <PlayCircle size={36} />
            </div>
          </div>
        </button>

        {/* 2. ปุ่มโหมดทดสอบ (จุกดำ) */}
        <button 
          onClick={() => navigate('/sandbox')}
          className='w-full p-6 bg-stone-900 rounded-3xl shadow-lg shadow-stone-300 text-left active:scale-[0.98] transition-all flex items-center justify-between group'
        >
          <div>
            <h3 className='text-xl font-bold text-white mb-1'>โหมดทดสอบ</h3>
            <p className='text-stone-400 text-sm font-medium'>ทดสอบความแม่นยำและการให้คะแนน</p>
          </div>
          <div className='bg-stone-800 p-3 rounded-2xl text-amber-500 group-hover:text-amber-400 transition-colors'>
            <Beaker size={32} />
          </div>
        </button>

        {/* 3. ปุ่มดูประวัติ (สีขาวนวล) */}
        <button 
          onClick={() => navigate('/history')}
          className='w-full p-6 bg-white border-2 border-stone-200 rounded-3xl shadow-sm text-left hover:border-stone-300 active:scale-[0.98] transition-all flex items-center justify-between group'
        >
          <div>
            <h3 className='text-xl font-bold text-stone-800 mb-1'>ประวัติ</h3>
            <p className='text-stone-500 text-sm font-medium'>ดูประวัติการใช้งานย้อนหลัง</p>
          </div>
          <div className='bg-stone-100 p-3 rounded-2xl text-stone-600 group-hover:bg-stone-200 transition-colors'>
            <ClipboardList size={32} />
          </div>
        </button>

        {/* 4. ปุ่มสำหรับ Admin เท่านั้น */}
        {user?.role === 'admin' && (
          <button 
            onClick={() => navigate('/admin')}
            className='mt-4 w-full p-5 bg-amber-50 border-2 border-amber-200 rounded-2xl text-left active:scale-[0.98] transition-all flex items-center gap-4 group'
          >
            <div className='bg-amber-100 p-3 rounded-xl text-amber-600'>
              <ShieldAlert size={28} />
            </div>
            <div>
              <h3 className='text-lg font-bold text-amber-900 mb-0.5'>จัดการระบบ</h3>
              <p className='text-amber-700/80 text-xs font-medium'>จัดการสิทธิ์ผู้ใช้งานทั้งหมด</p>
            </div>
          </button>
        )}

      </div>
    </div>
  );
};

export default Home;