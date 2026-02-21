import { useNavigate, useLocation } from 'react-router-dom';
import { ChevronLeft, UserCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext.jsx';

const Layout = ({ children }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();

  // ไม่แสดงปุ่มย้อนกลับในหน้าหลัก หรือหน้า Login
  const isRoot = location.pathname === '/' || location.pathname === '/login';

  return (
    <div className="flex justify-center bg-stone-200 min-h-screen font-sans">
      
      {/* 📱 Mobile Frame Container */}
      <div className="w-full max-w-[480px] bg-stone-50 shadow-2xl flex flex-col min-h-screen relative overflow-x-hidden border-x border-stone-300">
        
        {/* --- Header (สไตล์จุกดำ ตัดเส้นโขนแดง) --- */}
        <header className="h-16 flex items-center justify-between px-4 sticky top-0 bg-stone-900 text-stone-50 z-30 border-b-4 border-rose-600 shadow-md">
          <div className="w-10">
            {!isRoot && (
              <button 
                onClick={() => navigate(-1)} 
                className="p-2 hover:bg-stone-800 rounded-full transition-colors"
                aria-label="ย้อนกลับ"
              >
                <ChevronLeft size={24} className="text-stone-100" />
              </button>
            )}
          </div>
          
          <div className="flex flex-col items-center">
            <h1 className="font-bold text-lg tracking-wide uppercase flex items-center gap-2">
              <span className="text-rose-500">🐦</span> Bird Score
            </h1>
          </div>
          
          <div className="w-10 flex justify-end">
            {user && (
              <button onClick={logout} title="ออกจากระบบ" className="relative group">
                <UserCircle size={24} className="text-amber-500 group-hover:text-rose-400 transition-colors" />
                {/* จุดไฟสถานะออนไลน์ */}
                <span className="absolute -bottom-1 -right-1 flex h-2.5 w-2.5 rounded-full bg-emerald-500 border-2 border-stone-900"></span>
              </button>
            )}
          </div>
        </header>

        {/* --- Main Content (พื้นหลังอกขาว) --- */}
        <main className="flex-1 p-5 bg-stone-50 flex flex-col">
          {children}
        </main>

        {/* --- Footer Decoration (แถบตกแต่งด้านล่าง) --- */}
        <div className="h-1.5 w-full bg-gradient-to-r from-stone-900 via-rose-600 to-amber-600"></div>
      </div>
    </div>
  );
};

export default Layout;