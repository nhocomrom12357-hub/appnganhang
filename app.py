import streamlit as st

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính tiền gửi tiết kiệm",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 TÍNH TIỀN GỬI TIẾT KIỆM")
st.write("Tính toán tiền nhận được theo **lãi đơn** và **lãi kép**.")

st.divider()

# ==============================
# NHẬP DỮ LIỆU
# ==============================

# Số tiền gửi
so_tien = st.number_input(
    "💰 Số tiền gửi (VNĐ)",
    min_value=0,
    value=100_000_000,
    step=1_000_000,
    format="%d"
)

# Số tháng gửi
so_thang = st.number_input(
    "📅 Số tháng gửi",
    min_value=1,
    value=12,
    step=1
)

# Lãi suất
lai_suat = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

st.divider()

# ==============================
# NÚT TÍNH TOÁN
# ==============================

if st.button("🧮 TÍNH TOÁN", use_container_width=True):

    # Kiểm tra dữ liệu
    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if so_thang <= 0:
        st.error("Số tháng gửi phải lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # ==========================================
    # CHUYỂN ĐỔI LÃI SUẤT
    # ==========================================

    # Lãi suất năm dạng thập phân
    r_nam = lai_suat / 100

    # Thời gian gửi theo năm
    so_nam = so_thang / 12

    # ==========================================
    # 1. TÍNH LÃI ĐƠN
    # ==========================================

    # Công thức:
    # Tiền lãi = P * r * t
    lai_don = so_tien * r_nam * so_nam

    # Tổng tiền nhận được
    tong_lai_don = so_tien + lai_don

    # ==========================================
    # 2. TÍNH LÃI KÉP
    # ==========================================

    # Quy đổi lãi suất năm thành lãi suất tháng
    r_thang = r_nam / 12

    # Công thức:
    # A = P * (1 + r)^n
    tong_lai_kep = so_tien * (1 + r_thang) ** so_thang

    # Tiền lãi
    lai_kep = tong_lai_kep - so_tien

    # ==========================================
    # HIỂN THỊ KẾT QUẢ
    # ==========================================

    st.success("✅ Đã tính toán thành công!")

    st.subheader("📊 KẾT QUẢ")

    # ------------------------------------------
    # LÃI ĐƠN
    # ------------------------------------------

    st.markdown("### 🔵 1. Lãi đơn")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Tiền lãi",
            f"{lai_don:,.0f} VNĐ"
        )

    with col2:
        st.metric(
            "Tổng tiền nhận",
            f"{tong_lai_don:,.0f} VNĐ"
        )

    # ------------------------------------------
    # LÃI KÉP
    # ------------------------------------------

    st.markdown("### 🟢 2. Lãi kép")

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "Tiền lãi",
            f"{lai_kep:,.0f} VNĐ"
        )

    with col4:
        st.metric(
            "Tổng tiền nhận",
            f"{tong_lai_kep:,.0f} VNĐ"
        )

    # ------------------------------------------
    # SO SÁNH
    # ------------------------------------------

    st.divider()

    st.subheader("📈 SO SÁNH")

    chenh_lech = tong_lai_kep - tong_lai_don

    st.write(
        f"**Lãi kép cao hơn lãi đơn:** "
        f"**{chenh_lech:,.0f} VNĐ**"
    )

    # ==========================================
    # THÔNG TIN TÍNH TOÁN
    # ==========================================

    with st.expander("🔎 Xem chi tiết cách tính"):

        st.write(f"**Số tiền gửi:** {so_tien:,.0f} VNĐ")
        st.write(f"**Thời gian gửi:** {so_thang} tháng")
        st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")

        st.write(
            f"**Thời gian quy đổi:** {so_nam:.2f} năm"
        )

        st.markdown("#### Công thức lãi đơn")

        st.latex(
            r"A = P(1 + rt)"
        )

        st.write(
            f"A = {so_tien:,.0f} × "
            f"(1 + {r_nam:.4f} × {so_nam:.2f})"
        )

        st.write(
            f"= **{tong_lai_don:,.0f} VNĐ**"
        )

        st.markdown("#### Công thức lãi kép")

        st.latex(
            r"A = P(1+r)^n"
        )

        st.write(
            f"Lãi suất tháng = {r_thang * 100:.4f}%"
        )

        st.write(
            f"A = {so_tien:,.0f} × "
            f"(1 + {r_thang:.6f})^{so_thang}"
        )

        st.write(
            f"= **{tong_lai_kep:,.0f} VNĐ**"
        )
