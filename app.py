import streamlit as st

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="SmartDoc AI+", page_icon="⚖️", layout="wide")

st.title("⚖️ SmartDoc AI+ - Trợ lý Hành chính Công")
st.markdown("Hệ thống hỗ trợ giải đáp tự động các thủ tục về Hộ tịch và Cư trú.")

# Khởi tạo session_state để lưu lịch sử chat nếu chưa có
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị các tin nhắn đã có trong lịch sử
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Khung nhập liệu cho người dùng
if prompt := st.chat_input("Hãy đặt câu hỏi về thủ tục hành chính..."):
    # Hiển thị tin nhắn của người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Hiển thị phản hồi từ trợ lý
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Ở giai đoạn này, bot trả lời bằng câu cố định để kiểm tra giao diện
        mock_response = f"Đây là câu trả lời tạm thời cho câu hỏi: '{prompt}'. Tính năng tra cứu đang được xây dựng..."
        
        message_placeholder.markdown(mock_response)
    
    # Lưu phản hồi vào lịch sử
    st.session_state.messages.append({"role": "assistant", "content": mock_response})