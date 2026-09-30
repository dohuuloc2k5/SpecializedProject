import os
from core.rag_engine import RAGProcessor

def test_rag():
    print("Đang khởi động SmartDoc AI+...")
    rag = RAGProcessor()
    
    # Thay đổi tên file này cho khớp với file PDF bạn đã tải
    pdf_path = "data/luat_ho_tich.pdf" 
    
    if not os.path.exists(pdf_path):
        print(f"❌ Không tìm thấy file: {pdf_path}")
        return

    print(f"📄 Đang đọc và xử lý file: {pdf_path}...")
    documents = rag.process_pdf(pdf_path)
    print(f"✅ Đã trích xuất và chia thành {len(documents)} đoạn văn bản (chunks).")
    
    print("🧠 Đang xây dựng không gian tìm kiếm kết hợp (FAISS + BM25)...")
    retriever = rag.build_hybrid_retriever(documents)
    
    # Bạn có thể đổi câu hỏi này bám sát nội dung file PDF của bạn
    query = query = "Tôi muốn đăng ký thường trú tại nhà đi thuê thì cần phải đáp ứng những điều kiện gì?"
    print(f"\n❓ Câu hỏi của người dân: {query}")
    print("🤖 AI đang suy nghĩ và tra cứu...\n")
    
    answer = rag.get_answer(query, retriever)
    print(f"💡 Trả lời từ SmartDoc AI+:\n{answer}")

if __name__ == "__main__":
    test_rag()