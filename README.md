# SmartTAB - Sắp xếp công việc, đơn giản hóa cuộc sống

SmartTAB là giải pháp quản lý công việc thông minh, giúp bạn tối ưu hóa thời gian và tăng cường năng suất lao động hàng ngày thông qua giao diện trực quan và trợ lý ảo tích hợp.

## 🌟 Giới thiệu
Ứng dụng được thiết kế để giải quyết vấn đề quản lý thời gian của cá nhân và đội nhóm. Với SmartTAB, bạn không chỉ liệt kê các đầu việc mà còn có cái nhìn tổng quan thông qua lịch trình và nhận được sự hỗ trợ đắc lực từ trí tuệ nhân tạo.

## 🚀 Các tính năng chính
- **Quản lý Task linh hoạt:** Thêm, xóa, và đánh dấu hoàn thành công việc nhanh chóng.
- **Phân loại ưu tiên:** Gán mức độ ưu tiên (Cao, Trung bình, Thấp) để tập trung vào những việc quan trọng nhất.
- **Bộ lọc & Sắp xếp:** Tìm kiếm và sắp xếp công việc theo thời gian hoặc độ ưu tiên.
- **Chế độ xem Lịch (Calendar View):** Theo dõi deadline một cách trực quan theo từng tháng.
- **Thông báo nhắc nhở:** Tích hợp Web Notifications để cảnh báo các công việc sắp đến hạn.
- **Trợ lý AI Gemini:** Tích hợp AI giúp phân tích danh sách công việc, gợi ý cách thực hiện và tối ưu hóa lịch trình.

## 🛠️ Yêu cầu hệ thống
- **Frontend:** Node.js 18+ (Dành cho việc phát triển giao diện React).
- **Backend/Scripts:** Python 3.9+ (Dành cho các công cụ bổ trợ nếu có).

## 📦 Hướng dẫn cài đặt nhanh

### 1. Cài đặt các thư viện Python (nếu có công cụ bổ trợ)
```bash
pip install -r requirements.txt
```

### 2. Cài đặt môi trường Node.js cho Frontend
```bash
npm install
npm run dev
```

## 🔑 Thiết lập API Key
Để sử dụng tính năng Trợ lý AI, bạn cần thiết lập API Key từ Google AI Studio:

1. Truy cập [Google AI Studio](https://aistudio.google.com/).
2. Tạo API Key mới.
3. Thiết lập biến môi trường:
   - Trên Linux/macOS: `export API_KEY=your_api_key_here`
   - Trên Windows: `set API_KEY=your_api_key_here`
   *(Lưu ý: Ứng dụng này tự động đọc khóa từ biến môi trường `process.env.API_KEY`)*

## 👤 Thông tin tác giả
- **Create by:** Hailyngvn
- **Project:** SmartTAB Management System

---
*Sắp xếp công việc, đơn giản hóa cuộc sống.*
