import os
import uuid
from dotenv import load_dotenv
from core.database import DatabaseManager

# Tải các biến từ file .env
load_dotenv()

def run_test():
    print("Đang khởi tạo kết nối SQL Server...")
    try:
        # Khởi tạo đối tượng Database 
        db = DatabaseManager()
        
        # Kích hoạt hàm tạo bảng
        db.init_db()
        print("✅ Kết nối thành công! Đã kiểm tra/tạo bảng 'Chat_Sessions' và 'Messages'.")
        
        # Ghi thử một dòng dữ liệu để test Insert
        test_session_id = str(uuid.uuid4())
        db.save_message(test_session_id, "user", "Kịch bản kiểm thử kết nối DB thành công!")
        print("✅ Đã ghi thành công 1 dòng dữ liệu test vào bảng Messages!")
        
    except Exception as e:
        print(f"❌ Kết nối thất bại. Lỗi chi tiết:\n{e}")

if __name__ == "__main__":
    run_test()