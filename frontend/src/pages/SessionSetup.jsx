import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Play, Bird, Trophy, MapPin, Info } from 'lucide-react';

const SessionSetup = () => {
  const navigate = useNavigate();
  // ใช้ชื่อตัวแปรให้ตรงกับ Schema: match_name และ cage_number
  const [matchName, setMatchName] = useState('');
  const [cageNumber, setCageNumber] = useState('');
  const [loading, setLoading] = useState(false);

  // ฟังก์ชันสร้าง Unique Session ID (BIRD-เบอร์กรง-Timestamp)
  const generateUniqueSessionId = (cage) => {
    const timestamp = Date.now();
    const randomStr = Math.random().toString(36).substring(2, 7).toUpperCase();
    return `BIRD-${cage}-${timestamp}-${randomStr}`;
  };

  const handleStartSession = async (e) => {
    e.preventDefault();
    
    if (!matchName.trim()) {
      alert('กรุณาระบุชื่อรายการแข่งขันครับ');
      return;
    }

    if (!cageNumber.trim()) {
      alert('กรุณาระบุหมายเลขกรงครับ');
      return;
    }

    setLoading(true);

    try {
      // 🌟 สร้าง sessionId อัตโนมัติให้เป็น Unique ตามที่ MongoDB คาดหวัง
      const sessionId = generateUniqueSessionId(cageNumber);

      // จำลองการเตรียมระบบ 800ms
      setTimeout(() => {
        // ส่งข้อมูลทั้งหมดไปยังหน้า /competition ผ่าน state
        navigate('/competition', { 
          state: { 
            match_name: matchName, 
            cage_number: cageNumber,
            session_id: sessionId,
            mode: 'competition', // ล็อกโหมดเป็นแข่งขัน
            round_no: 1 // เริ่มที่ยก 1
          } 
        });
        setLoading(false);
      }, 800);

    } catch (error) {
      console.error('Setup Error:', error);
      alert('เกิดข้อผิดพลาดในการสร้างเซสชัน');
      setLoading(false);
    }
  };

  return (
    <div className='flex flex-col h-full animate-in fade-in duration-300 pb-6'>
      
      {/* --- Header Section --- */}
      <div className='mb-8 mt-2 flex items-center gap-3'>
        <div className='bg-rose-100 p-3 rounded-2xl text-rose-600 shadow-inner'>
          <Trophy size={28} />
        </div>
        <div>
          <h2 className='text-2xl font-black text-stone-900 tracking-tight'>โหมดการแข่งขัน</h2>
          <p className='text-stone-500 font-medium text-sm mt-0.5'>เตรียมข้อมูลสำหรับการบันทึกคะแนน</p>
        </div>
      </div>

      <form onSubmit={handleStartSession} className='flex-1 flex flex-col gap-6'>
        
        {/* --- 1. ชื่อรายการแข่งขัน (match_name) --- */}
        <div className='space-y-2'>
          <label className='text-sm font-bold text-stone-700 ml-1 flex items-center gap-1.5'>
            <MapPin size={16} className='text-rose-600' /> ชื่อรายการแข่งขัน
          </label>
          <input 
            type='text' 
            placeholder='เช่น พัทลุงคัพ 2026'
            className='w-full p-4 bg-white border-2 border-stone-200 rounded-2xl focus:ring-0 focus:border-rose-500 outline-none transition-all shadow-sm text-stone-900 font-medium'
            value={matchName}
            onChange={(e) => setMatchName(e.target.value)}
            required
          />
        </div>

        {/* --- 2. หมายเลขกรง (cage_number) --- */}
        <div className='space-y-3 bg-white p-6 rounded-3xl border-2 border-stone-200 shadow-sm mt-2 flex flex-col items-center text-center'>
          <Bird size={48} className='text-rose-600 mb-2 opacity-80' />
          <label className='text-lg font-black text-stone-800'>
            หมายเลขกรงนก
          </label>
          <p className='text-sm text-stone-500 font-medium mb-4'>
            ระบุเบอร์กรงที่ต้องการตัดสิน
          </p>
          
          <input
            type='text'
            placeholder='A01'
            className='w-full max-w-[220px] p-4 bg-stone-50 border-2 border-stone-200 rounded-2xl focus:ring-4 focus:ring-rose-100 focus:border-rose-500 outline-none transition-all text-4xl font-black text-stone-900 text-center tracking-widest placeholder:text-stone-300 shadow-inner uppercase'
            value={cageNumber}
            onChange={(e) => setCageNumber(e.target.value)}
            required
          />
        </div>

        {/* --- Info Box --- */}
        <div className='bg-amber-50 border border-amber-200 rounded-2xl p-4 flex gap-3 text-amber-800'>
          <Info size={20} className='shrink-0 mt-0.5 text-amber-600' />
          <p className='text-sm font-medium'>
            เมื่อกดเริ่ม ระบบจะสร้าง <strong className='font-black'>Session ID</strong> เพื่อรวบรวมคะแนนทั้ง 4 ยกเข้าด้วยกันโดยอัตโนมัติ
          </p>
        </div>

        {/* --- Submit Button --- */}
        <div className='mt-auto pt-4'>
          <button 
            type='submit' 
            disabled={loading}
            className='w-full p-5 flex justify-center items-center gap-2 bg-gradient-to-r from-rose-600 to-rose-700 text-white font-black text-xl rounded-2xl shadow-lg shadow-rose-200 hover:from-rose-700 hover:to-rose-800 active:scale-[0.98] transition-all disabled:opacity-50'
          >
            {loading ? 'กำลังเตรียมระบบ...' : (
              <>
                <Play fill='currentColor' size={24} /> 
                เริ่มการแข่งขัน
              </>
            )}
          </button>
        </div>

      </form>
    </div>
  );
};

export default SessionSetup;