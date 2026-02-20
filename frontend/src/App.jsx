const App = () => {
  return (
    <div className='min-h-screen bg-gray-100 flex items-center justify-center p-4'>
      <div className='bg-white p-8 rounded-3xl shadow-xl max-w-sm w-full text-center'>
        <h1 className='text-2xl font-bold text-emerald-600 mb-2'>
          Bird Score AI 🐦
        </h1>
        <p className='text-gray-500 mb-6'>
          โครงสร้างโฟลเดอร์พร้อมแล้ว! ระบบ React 19 กำลังทำงาน
        </p>
        <div className='space-y-2'>
          <div className='p-3 bg-emerald-50 rounded-xl border border-emerald-100 text-emerald-700 font-medium'>
            ✅ Tailwind CSS Connected
          </div>
          <div className='p-3 bg-blue-50 rounded-xl border border-blue-100 text-blue-700 font-medium'>
            📂 Folder Structure Created
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
