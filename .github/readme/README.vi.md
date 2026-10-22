# Project Advisor

[English](../../README.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [日本語](README.ja.md) · **Tiếng Việt** · [한국어](README.ko.md) · [فارسی](README.fa.md) · [ภาษาไทย](README.th.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Bahasa Indonesia](README.id.md)

Một skill không phụ thuộc nền tảng để tư vấn dự án với tư duy phản biện, soạn chỉ dẫn tập trung cho tác nhân triển khai và đánh giá kết quả dựa trên bằng chứng.

Dùng một cuộc trò chuyện để quyết định công việc tiếp theo đáng làm và một tác nhân khác để khảo sát, triển khai, kiểm chứng. Cố vấn xem xét các giả định yếu, đề xuất quy trình tương xứng với vấn đề và đánh giá kết quả. Bạn giữ quyền quyết định mục tiêu, ưu tiên và sở thích.

Phương pháp không bắt buộc mô hình, nhà cung cấp, plugin hay dịch vụ bên ngoài cụ thể. Nó dành cho dự án phát triển trong môi trường tác nhân có thể nạp chỉ dẫn và tệp tham chiếu.

## Ví dụ quy trình

Bạn muốn thêm chức năng nhập khách hàng bằng CSV vào ứng dụng hiện có.

| Bước | Ai | Ví dụ |
|---|---|---|
| Nêu mục tiêu | Bạn → cố vấn | “Tôi muốn nhân viên nhập CSV khách hàng mà không tạo bản ghi trùng.” |
| Làm rõ điểm mơ hồ thực sự | Cố vấn ↔ bạn | “Email lặp lại nên cập nhật khách hàng hiện có hay được đánh dấu để xem xét?” Bạn chọn xem xét. |
| Chuẩn bị thực hiện | Cố vấn → bạn | Chỉ dẫn cho tác nhân nêu hành vi nhập, xử lý trùng lặp, giới hạn phân quyền hiện có và bằng chứng cần để hoàn thành. |
| Thực hiện | Bạn → tác nhân | Bạn chuyển chỉ dẫn cho tác nhân trong không gian làm việc của dự án. Tác nhân khảo sát, triển khai và kiểm chứng. |
| Mang kết quả về | Bạn → cố vấn | Tác nhân báo nhập thành công và đã kiểm tra dòng không hợp lệ cùng dữ liệu trùng trong một tệp. |
| Đánh giá bằng chứng | Cố vấn → bạn | Cố vấn nhận ra chưa kiểm tra nhập cùng tệp hai lần và chỉ yêu cầu bổ sung việc đó. |
| Hoàn tất hoặc sửa | Tác nhân → bạn → cố vấn | Kết quả chứng minh hành vi mong đợi hoặc lỗi được sửa. Cố vấn kết thúc khi bằng chứng đủ. |

Đây là ví dụ, không phải chuỗi bước bắt buộc. Tác vụ rõ ràng có thể thực hiện ngay; không khuyến khích lập kế hoạch thừa hay kiểm chứng lặp lại. Skill không tự kết nối hoặc gửi tin giữa các cuộc trò chuyện.

## Thiết lập khuyến nghị

Dùng **cố vấn trong cuộc trò chuyện riêng, với không gian làm việc riêng nằm ngoài cây thư mục dự án đích**. Tác nhân triển khai ở trong không gian dự án và tuân thủ chỉ dẫn áp dụng. Một cuộc trò chuyện khác gắn với cùng dự án vẫn có thể nạp `AGENTS.md`, `CLAUDE.md` hoặc quy tắc cục bộ khác.

Cách này giảm việc tự nạp chỉ dẫn riêng của dự án vào ngữ cảnh cố vấn. Quy tắc toàn cục, chỉ dẫn thư mục cha, tích hợp và ngữ cảnh kế thừa vẫn có thể áp dụng; không đảm bảo cách ly hoàn toàn. Cung cấp mục tiêu, tài liệu được chọn và báo cáo của tác nhân. Cố vấn có thể xem quy tắc dự án như bằng chứng, đồng thời tôn trọng thứ bậc chỉ dẫn của môi trường.

Giữ trạng thái cố vấn của mỗi dự án trong thư mục ngoài riêng, ngoài skill đã cài và tốt nhất là ngoài kho dự án. Không công khai trạng thái riêng tư cùng skill.

## Cài đặt

Sao chép hoặc tải kho này, rồi chép toàn bộ thư mục `skills/project-advisor` đến vị trí phù hợp. Giữ `references/` và `agents/` bên cạnh `SKILL.md`. Xem lại thay đổi cục bộ trước khi ghi đè bản cài hiện có.

| Môi trường | Thư mục cài cá nhân | Gọi tường minh |
|---|---|---|
| Codex | `~/.agents/skills/project-advisor/` | `$project-advisor` |
| Claude Code | `~/.claude/skills/project-advisor/` | `/project-advisor` |
| OpenCode | `~/.config/opencode/skills/project-advisor/` | Chọn hoặc nạp skill tường minh; xem cấu hình lệnh tùy chọn bên dưới. |

`~` là thư mục cá nhân, kể cả trên Windows. Các đường dẫn này dành cho công cụ chạy cục bộ; sản phẩm được lưu trữ có thể dùng cơ chế khác. Nếu skill chưa xuất hiện sau khi cài, mở phiên cố vấn mới.

### Điều khiển cách gọi

Phần lõi luôn yêu cầu kích hoạt tường minh. Điều khiển của môi trường được cấu hình riêng:

- **Codex:** tệp kèm theo `agents/openai.yaml` đặt `policy.allow_implicit_invocation: false`.
- **Claude Code:** thêm `disable-model-invocation: true` vào frontmatter YAML của `SKILL.md` đã cài để ngăn mô hình tự gọi. Đây là điều chỉnh riêng cho Claude Code, không thuộc tệp nguồn chung.
- **OpenCode:** thêm metadata dạng chuỗi sau vào frontmatter của `SKILL.md` đã cài để cung cấp lệnh và loại skill khỏi hướng dẫn chọn tự động:

  ```yaml
  metadata:
    opencode/slash: "true"
    opencode/autoinvoke: "false"
  ```

  Sau đó gọi `/project-advisor` trên phiên bản hỗ trợ các thiết lập này. Nếu ứng dụng của bạn khác, dùng cơ chế nạp skill tường minh của nó.

Đây là điều chỉnh cài đặt cục bộ; không cần duy trì các bản phương pháp riêng trong kho. Giữ cấu hình frontmatter riêng của môi trường trước khi cập nhật.

Hướng dẫn cài đặt và gọi đã được đối chiếu với tài liệu chính thức của [Codex](https://learn.chatgpt.com/docs/build-skills), [Claude Code](https://code.claude.com/docs/en/skills) và [OpenCode](https://opencode.ai/docs/skills/) ngày 21 tháng 10 năm 2026. **Phiên bản này chưa được thử nghiệm toàn trình trên cả ba ứng dụng.** Kiểm tra tài liệu không chứng nhận tương thích khi chạy. Kinh nghiệm dùng cố vấn tiếng Bồ Đào Nha trước đây đã định hướng phiên bản này; bản tiếng Anh vẫn cần phản hồi thực tế rộng hơn.

## Kích hoạt và sử dụng

Gọi skill bằng cơ chế của môi trường, rồi cung cấp mục tiêu và thư mục trạng thái. Ví dụ:

```text
Kích hoạt Project Advisor.
Dùng thư mục trạng thái ngoài này: /path/to/my-advisor-workspace.
Tác nhân triển khai đang ở cuộc trò chuyện riêng.
Tôi muốn thêm nhập khách hàng bằng CSV vào ứng dụng hiện có.
```

Cố vấn đọc chỉ dẫn lõi và trạng thái ngoài, hoặc tạo trạng thái khi cần. Vai trò tiếp tục trong cùng cuộc trò chuyện cho đến khi bạn tắt tường minh:

```text
Tắt cố vấn.
```

Trong cuộc trò chuyện mới, kích hoạt lại skill và cung cấp cùng thư mục trạng thái để tiếp tục. Chỉ cài đặt không bao giờ kích hoạt vai trò. Chỉ dẫn và ví dụ của skill bằng tiếng Anh; **cố vấn trao đổi bằng ngôn ngữ bạn ưu tiên**.

## Cố vấn làm gì

- Gắn tác vụ tiếp theo với kết quả hữu ích cho dự án.
- Chất vấn quyết định khi thấy vấn đề cụ thể và đề xuất phương án khác.
- Hỏi về sở thích, ưu tiên, ý định và sự kiện bạn có thể làm rõ.
- Nghiên cứu có mục tiêu cho câu hỏi kỹ thuật hoặc chuyên môn.
- Điều chỉnh kế hoạch, ủy nhiệm và kiểm chứng theo rủi ro và bất định.
- Đánh giá bằng chứng của tác nhân và dừng khi công việc đã đủ hoàn tất.
- Tôn trọng lựa chọn có hiểu biết và giới hạn cho phép.
- Duy trì điểm tiếp nối ngắn gọn, cập nhật thay vì tích lũy nhật ký hoạt động.

## Trạng thái, riêng tư và giới hạn

Cố vấn dùng `ADVISOR_STATE.md` trong không gian ngoài của bạn. Khi tạo trạng thái mới, `ADVISOR_STATE_TEMPLATE.md` hiện có được ưu tiên hơn lược đồ dự phòng đi kèm. `STATE_SCHEMA.md` chỉ chứa các trường mẫu chung.

Trạng thái có thể chứa quyết định nhạy cảm, đường dẫn hoặc thông tin dự án. Chọn nơi lưu và người nhận một cách có chủ đích. `.gitignore` loại tên tệp trạng thái nhưng chỉ trong bản sao kho này và không xóa tệp đã được theo dõi. Nên giữ trạng thái riêng ngoài các kho sẽ công khai.

Trạng thái được hợp nhất trong lượt hoạt động khi thông tin thay đổi đáng kể, lúc kết thúc việc hoặc tiếp tục sau nén ngữ cảnh khi cần. Không có tiến trình nền, hook phiên hay đảm bảo khôi phục nếu mất ngữ cảnh kích hoạt. Kích hoạt lại với cùng thư mục khi cần. Nếu không truy cập được tệp, cố vấn có thể đưa bản tóm tắt để bạn lưu thay vì khẳng định đã lưu trạng thái.

Skill cung cấp chỉ dẫn, không phải kiểm soát truy cập hay đảm bảo quyết định đúng. Hành vi phụ thuộc mô hình, bằng chứng sẵn có, chỉ dẫn môi trường và công cụ. Skill không triển khai dự án được điều phối hay tự liên hệ tác nhân.

## Cấu trúc kho

```text
skills/project-advisor/
├── SKILL.md                   Kích hoạt, trạng thái, tiếp nối
├── agents/openai.yaml         Chính sách gọi riêng cho Codex
└── references/
    ├── ADVISOR_CORE.md        Phương pháp độc lập nền tảng
    └── STATE_SCHEMA.md        Cấu trúc khôi phục trạng thái
```

## Đóng góp

Mô tả vấn đề thực tế, hành vi mong đợi và lý do thay đổi giúp ích mà không thêm quy trình thừa. Dùng ví dụ giả lập, bỏ thông tin riêng tư và nêu môi trường cùng giới hạn kiểm tra hành vi. Giữ ranh giới giữa hướng dẫn tái sử dụng được và sở thích cá nhân hoặc riêng dự án.

Bản dịch README nằm trong `.github/readme/`. Khi cập nhật, giữ ví dụ, lệnh, liên kết và giới hạn đồng bộ với README tiếng Anh. Chỉ thêm liên kết ngôn ngữ cho bản dịch có trong kho.

## Giấy phép

[MIT](../../LICENSE) — Copyright (c) 2026 Guilherme Rocha.
