# Project Advisor

[English](../../README.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [日本語](README.ja.md) · **Tiếng Việt** · [한국어](README.ko.md) · [فارسی](README.fa.md) · [ภาษาไทย](README.th.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Bahasa Indonesia](README.id.md)

Phương pháp tư vấn dự án không phụ thuộc mô hình, với bộ chuyển đổi không gian làm việc cho Codex, Claude Code và OpenCode.

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

Dùng một thư mục và cuộc trò chuyện tư vấn riêng cho mỗi dự án, nằm ngoài kho mã đích. Dự án khác cần thư mục khác và trạng thái mới. Tác nhân thực thi làm việc trong kho mã. Chỉ dẫn toàn cục và từ thư mục cha vẫn có thể áp dụng.

## Cài đặt

Sao chép toàn bộ `skills/project-advisor` cùng các thư mục con vào thư mục skill cá nhân của môi trường. Dùng Python 3.10+ để xem trước, sau đó thêm `--apply` khi đã kiểm tra thay đổi. Thay đường dẫn ví dụ và chọn `codex`, `claude` hoặc `opencode`.

```sh
python <skill-dir>/scripts/workspace.py --workspace <advisor-dir> --project <target-dir> --harness codex
python <skill-dir>/scripts/workspace.py --workspace <advisor-dir> --project <target-dir> --harness codex --apply
```

Codex: `$project-advisor` · Claude Code: `/project-advisor` · OpenCode: `project-advisor`

[Codex / Claude Code / OpenCode — setup, updates, migration](../../skills/project-advisor/references/HARNESSES.md)

## Kích hoạt và sử dụng

Mở cuộc trò chuyện mới trong thư mục đã chuẩn bị. Việc nạp chỉ dẫn cục bộ kích hoạt tư vấn cho dự án đã gắn; chỉ cài skill không kích hoạt các cuộc trò chuyện khác. Kiểm tra vai trò, dự án, trạng thái và bước tiếp theo. Tắt rõ ràng chỉ có hiệu lực trong cuộc trò chuyện hiện tại; cuộc trò chuyện mới lại bắt đầu ở vai trò tư vấn. Câu trả lời dùng ngôn ngữ bạn chọn.

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

`AGENTS.md` chứa phương pháp; `CLAUDE.md` nhập tệp đó khi cần. `.advisor-workspace.json` ghi dự án, môi trường, phiên bản và mã băm. Trạng thái riêng nằm trong `ADVISOR_STATE.md`; có thể giữ `CONSULTOR_STATE.md` cũ. Đọc trạng thái trước khi dùng `--adopt-existing-state`. Lưu tùy chọn trong `ADVISOR_LOCAL.md`. Cập nhật hiển thị khác biệt và từ chối ghi đè chỉ dẫn đã sửa; cần xem xét và hợp nhất. Trạng thái có sẵn được giữ nguyên. Không có hook hay dịch vụ nền. Kiểm thử trình cài không chứng minh hành vi của mọi ứng dụng.

## Cấu trúc kho

Mẫu là nguồn phương pháp duy nhất được phân phối; mỗi workspace nhận bản sao có phiên bản. Không còn CORE riêng. Cập nhật skill không tự cập nhật workspace. Không công bố trạng thái hay cấu hình riêng.

```text
skills/project-advisor/
├── SKILL.md
├── templates/AGENTS.md
├── scripts/workspace.py
├── agents/openai.yaml
└── references/
    ├── HARNESSES.md
    └── STATE_SCHEMA.md
```

## Đóng góp

Mô tả vấn đề thực tế, hành vi mong đợi và lý do thay đổi giúp ích mà không thêm quy trình thừa. Dùng ví dụ giả lập, bỏ thông tin riêng tư và nêu môi trường cùng giới hạn kiểm tra hành vi. Giữ ranh giới giữa hướng dẫn tái sử dụng được và sở thích cá nhân hoặc riêng dự án.

Bản dịch README nằm trong `.github/readme/`. Khi cập nhật, giữ ví dụ, lệnh, liên kết và giới hạn đồng bộ với README tiếng Anh. Chỉ thêm liên kết ngôn ngữ cho bản dịch có trong kho.

## Giấy phép

[MIT](../../LICENSE) — Copyright (c) 2026 Guilherme Rocha.

## 2.1.0

Bản sửa đổi 2.1.0: trạng thái phân biệt nguồn bằng chứng, đối chiếu các quyết định đã thay thế và giữ lại ràng buộc cùng kiểm chứng chưa hoàn tất. Trình cài đặt dùng một mẫu trạng thái, giữ tên tệp cũ và cải thiện hướng dẫn khôi phục manifest và khóa. Chưa có so sánh có kiểm soát chứng minh lợi ích về chất lượng, thời gian hoặc chi phí. Kiểm thử bộ chuyển đổi không chứng minh hoạt động thực tế trong từng môi trường; khi chat không truy cập tệp, cần cung cấp và lưu phương pháp cùng trạng thái thủ công.

[English technical reference](../../docs/AUDIT_2_1.md) · [Examples](../../skills/project-advisor/references/EXAMPLES.md)
