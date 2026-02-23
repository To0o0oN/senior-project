import { useLocation } from 'react-router-dom';

const Competition = () => {
    const location = useLocation();
    const data = location.state;

    return (
        <div>
            <h1>ตรวจสอบข้อมูลที่ได้รับ</h1>
            <pre>
                {JSON.stringify(data, null, 2)}
            </pre>
            <ul>
                <li><strong>Match:</strong> {data?.match_name}</li>
                <li><strong>Cage:</strong> {data?.cage_number}</li>
                <li><strong>Session ID:</strong> {data?.session_id}</li>
                <li><strong>Round:</strong> {data?.round_no}</li>
            </ul>
        </div>
    );
};

export default Competition;