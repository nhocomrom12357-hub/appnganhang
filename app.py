import streamlit as st
import pandas as pd

# Cấu hình trang
st.set_page_config(
    page_title="Công cụ tính tiền tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Công Cụ Tính Tiền Tiết Kiệm")
st.write("Sử dụng ứng dụng này để so sánh lợi nhuận giữa **Lãi đơn** và **Lãi kép**.")

# Tạo khung nhập dữ liệu từ người dùng
st.sidebar.header("Tùy chỉnh thông số")

so_tien_gui = st.sidebar.number_input(
    "Số tiền gửi ban đầu (VNĐ):",
    min_value=100000,
    value=100000000,
    step=1000000,
    format="%d"
)

lai_suat_nam = st.sidebar.number_input(
    "Lãi suất (%/năm):",
    min_value=0.1,
    max_value=30.0,
    value=6.0,
    step=0.1,
    format="%.1f"
)

so_thang_gui = st.sidebar.number_input(
    "Số tháng gửi:",
    min_value=1,
    max_value=360,
    value=12,
    step=1
)

# Chuyển đổi lãi suất năm thành lãi suất tháng
lai_suat_thang = (lai_suat_nam / 100) / 12

# 1. Tính Lãi Đơn
# Công thức: Lãi = Gốc * Lãi suất tháng * Số tháng
tien_lai_don = so_tien_gui * lai_suat_thang * so_thang_gui
tong_tien_lai_don = so_tien_gui + tien_lai_don

# 2. Tính Lãi Kép (Lãi nhập gốc hàng tháng)
# Công thức: Tổng tiền = Gốc * (1 + Lãi suất tháng)^Số tháng
tong_tien_lai_kep = so_tien_gui * ((1 + lai_suat_thang) ** so_thang_gui)
tien_lai_kep = tong_tien_lai_kep - so_tien_gui

# Hiển thị kết quả tổng quan
st.subheader("📌 Kết Quả Dự Tính")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔹 Lãi Đơn")
    st.metric("Tiền lãi thu được", f"{tien_lai_don:,.0f} VNĐ")
    st.metric("Tổng số tiền nhận được", f"{tong_tien_lai_don:,.0f} VNĐ")

with col2:
    st.markdown("### 🔸 Lãi Kép")
    st.metric("Tiền lãi thu được", f"{tien_lai_kep:,.0f} VNĐ", delta=f"+{(tien_lai_kep - tien_lai_don):,.0f} VNĐ so với lãi đơn")
    st.metric("Tổng số tiền nhận được", f"{tong_tien_lai_kep:,.0f} VNĐ")

# Bảng và đồ thị tăng trưởng theo thời gian
st.subheader("📈 Biểu Đồ Tăng Trưởng Theo Thời Gian")

# Chuẩn bị dữ liệu theo từng tháng
thang_list = list(range(1, so_thang_gui + 1))
lai_don_list = [so_tien_gui + (so_tien_gui * lai_suat_thang * t) for t in thang_list]
lai_kep_list = [so_tien_gui * ((1 + lai_suat_thang) ** t) for t in thang_list]

df = pd.DataFrame({
    "Tháng": thang_list,
    "Lãi Đơn": lai_don_list,
    "Lãi Kép": lai_kep_list
})

df.set_index("Tháng", inplace=True)

# Hiển thị biểu đồ
st.line_chart(df)

# Cho phép xem chi tiết bảng dữ liệu
with st.expander("📄 Xem chi tiết bảng tổng kết qua từng tháng"):
    st.dataframe(df.style.format("{:,.0f} VNĐ"))
