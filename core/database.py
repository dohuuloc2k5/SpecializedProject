import pyodbc
from .config import Config

class DatabaseManager:
    _instance = None

    # Áp dụng Singleton Pattern để đảm bảo chỉ có 1 instance quản lý DB
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.connection_string = cls._build_connection_string()
        return cls._instance

    @staticmethod
    def _build_connection_string():
        # Nếu file .env không có USER/PASS, tự động dùng Windows Authentication
        if not Config.DB_USER or not Config.DB_PASSWORD:
            return (f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={Config.DB_SERVER};"
                    f"DATABASE={Config.DB_NAME};"
                    f"Trusted_Connection=yes;"
                    f"TrustServerCertificate=yes;")
        else:
            return (f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={Config.DB_SERVER};"
                    f"DATABASE={Config.DB_NAME};"
                    f"UID={Config.DB_USER};"
                    f"PWD={Config.DB_PASSWORD};"
                    f"TrustServerCertificate=yes;")

    def get_connection(self):
        return pyodbc.connect(self.connection_string)

    def init_db(self):
        """Khởi tạo các bảng cần thiết nếu chưa tồn tại"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 1. Tạo bảng Chat_Sessions
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Chat_Sessions' and xtype='U')
                CREATE TABLE Chat_Sessions (
                    SessionID VARCHAR(36) PRIMARY KEY,
                    StartTime DATETIME DEFAULT GETDATE()
                )
            """)
            
            # 2. Tạo bảng Messages
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Messages' and xtype='U')
                CREATE TABLE Messages (
                    MessageID INT IDENTITY(1,1) PRIMARY KEY,
                    SessionID VARCHAR(36) FOREIGN KEY REFERENCES Chat_Sessions(SessionID),
                    Role VARCHAR(20),
                    Content NVARCHAR(MAX),
                    Timestamp DATETIME DEFAULT GETDATE()
                )
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ Lỗi khởi tạo database: {e}")
            raise e

    def save_message(self, session_id, role, content):
        """Lưu tin nhắn vào DB. Tự động tạo Session nếu chưa có."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Kiểm tra xem Session đã tồn tại chưa, nếu chưa thì tạo mới
            cursor.execute("SELECT 1 FROM Chat_Sessions WHERE SessionID = ?", (session_id,))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO Chat_Sessions (SessionID) VALUES (?)", (session_id,))
            
            # Chèn tin nhắn
            cursor.execute("""
                INSERT INTO Messages (SessionID, Role, Content)
                VALUES (?, ?, ?)
            """, (session_id, role, content))
            
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ Lỗi lưu tin nhắn: {e}")
            raise e