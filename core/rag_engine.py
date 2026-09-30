import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document

class RAGProcessor:
    def __init__(self):
        # Khởi tạo mô hình nhúng
        self.embeddings = HuggingFaceEmbeddings(model_name="keepitreal/vietnamese-sbert")
        # Trỏ đích danh tới Server Ollama ổ D
        self.llm = Ollama(model="qwen2.5:7b", base_url="http://127.0.0.1:11434")
    
    def process_pdf(self, pdf_path):
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        # Chia nhỏ văn bản để AI dễ nuốt
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        chunks = splitter.split_text(text)
        return [Document(page_content=chunk) for chunk in chunks]

    def build_hybrid_retriever(self, documents):
        # Dùng Vector Search (FAISS) cực mạnh để lấy 3 đoạn luật liên quan nhất
        faiss_vectorstore = FAISS.from_documents(documents, self.embeddings)
        return faiss_vectorstore.as_retriever(search_kwargs={"k": 6})

    def get_answer(self, query, retriever):
        # 1. BẬT CHẾ ĐỘ DEBUG: Lấy thử dữ liệu và in ra màn hình
        retrieved_docs = retriever.invoke(query)
        print("\n" + "="*50)
        print("🔍 [DEBUG] CÁC ĐOẠN LUẬT MÀ FAISS TÌM THẤY:")
        for i, doc in enumerate(retrieved_docs):
            print(f"\n--- Đoạn {i+1} ---")
            print(doc.page_content) # In thẳng nội dung PDF đã trích xuất
        print("="*50 + "\n")

        # 2. Xử lý Prompt như cũ
        template = """Bạn là SmartDoc AI+, trợ lý ảo hỗ trợ chính quyền địa phương cấp cơ sở.
        NHIỆM VỤ TỐI THƯỢNG: BẠN CHỈ ĐƯỢC PHÉP SỬ DỤNG phần [THÔNG TIN NGỮ CẢNH] bên dưới để trả lời.
        - TUYỆT ĐỐI KHÔNG tự suy diễn, KHÔNG dùng kiến thức bên ngoài, KHÔNG lấy ví dụ cụ thể trong ngữ cảnh để làm định nghĩa chung.
        - Nếu [THÔNG TIN NGỮ CẢNH] không chứa trực tiếp câu trả lời, bạn PHẢI trả lời đúng nguyên văn câu sau: "Xin lỗi, tôi chưa tìm thấy quy định pháp luật về vấn đề này trong tài liệu hiện tại."
        
        [THÔNG TIN NGỮ CẢNH]:
        {context}
        
        [CÂU HỎI CỦA NGƯỜI DÂN]: {question}
        
        Trả lời:"""
        
        prompt = PromptTemplate.from_template(template)
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return rag_chain.invoke(query)