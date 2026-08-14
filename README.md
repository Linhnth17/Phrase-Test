# Test phrase — demo tích hợp Phrase (Localization)

Demo minh họa quy trình đồng bộ chuỗi (string) giữa project .NET và [Phrase Strings](https://phrase.com):

```
dev thêm string vào Resources.resx (en)
        │  git push
        ▼
GitHub Actions: phrase-push.yml  ──►  phrase push  ──►  Phrase project
        │
        │  string mới xuất hiện trong Phrase UI, translator dịch tại đó
        ▼
GitHub Actions: phrase-pull.yml  ──►  phrase pull  ──►  tạo PR mới vào main
        │                                              (Resources.<locale>.resx)
        ▼
  review & merge PR
```

## Các file trong demo

Demo có **3 project, mỗi project 1 file resx nguồn riêng** — minh họa trường hợp thật là 1 repo có nhiều project, mỗi project quản lý string của mình:

| Project | File resx | Tag trên Phrase |
|---|---|---|
| `Test phrase` (console app gốc) | [`Properties/Resources.resx`](Properties/Resources.resx) | `mainapp` |
| `OrderService` | [`OrderService/Properties/Resources.resx`](OrderService/Properties/Resources.resx) | `orderservice` |
| `PaymentService` | [`PaymentService/Properties/Resources.resx`](PaymentService/Properties/Resources.resx) | `paymentservice` |

| File | Vai trò |
|---|---|
| [`.phrase.yml`](.phrase.yml) | Config Phrase CLI: 3 push source (mỗi source gắn `tag` riêng) + 3 pull target (lọc lại theo đúng `tags` để không bị trộn key giữa các project) |
| [`.github/workflows/phrase-push.yml`](.github/workflows/phrase-push.yml) | Khi bất kỳ file resx nào trong 3 file đổi trên `main` → chạy `phrase push`, đẩy toàn bộ 3 source (source nào không đổi thì coi như no-op) |
| [`.github/workflows/phrase-pull.yml`](.github/workflows/phrase-pull.yml) | Chạy theo lịch (hoặc bấm tay) → `phrase pull`, mỗi target lọc đúng tag của nó → mở 1 PR chứa cả 3 file dịch tương ứng vào `main` |

**Vì sao cần `tag`/`tags`:** Phrase lưu key ở cấp *project*, không phải cấp file. Nếu không gắn tag, key của cả 3 project sẽ trộn chung 1 chỗ (2 project trùng tên key sẽ bị coi là cùng 1 key), và khi pull thì cả 3 file export ra sẽ chứa key của cả 3 project luôn, sai với ý đồ ban đầu.

## Những gì demo này đã dựng sẵn (chạy local được)

- Cấu trúc `Properties/Resources.resx` + code đọc resource trong [`Program.cs`](Program.cs).
- Config `.phrase.yml` và 2 workflow GitHub Actions dùng action chính thức [`phrase/setup-cli`](https://github.com/phrase/setup-cli) để cài Phrase CLI, sau đó chạy `phrase push` / `phrase pull`.
- Git repo (đã push lên [Linhnth17/Phrase-Test](https://github.com/Linhnth17/Phrase-Test)) với các commit minh họa từng bước.

## Các bước để kết nối với project Phrase thật

1. Đăng nhập [phrase.com](https://phrase.com), tạo (hoặc dùng) một **Strings project**.
2. Lấy 2 giá trị từ Phrase:
   - **Project ID**: project → **More/Project settings → API** tab.
   - **Access Token**: avatar → **Account Settings → API Access** → tạo Personal Access Token (quyền đọc/ghi project đó).
3. Đặt **Project ID** thật vào `.phrase.yml` (dòng `project_id:`) — giá trị này **không nhạy cảm**, có thể commit thẳng vào repo. CLI không có flag `--project_id`, nên bắt buộc phải khai báo ở đây.
4. Vào repo GitHub → **Settings → Secrets and variables → Actions → New repository secret**, thêm secret `PHRASE_ACCESS_TOKEN` (giá trị là access token vừa tạo). **Lưu ý:** `.phrase.yml` **không** hỗ trợ cú pháp `$VAR` để nội suy biến môi trường — nếu viết `access_token: $PHRASE_ACCESS_TOKEN` trong file, CLI sẽ gửi đúng chuỗi literal đó làm token và bị `401 Unauthorized`. Vì vậy token được truyền qua flag `--access_token="$PHRASE_ACCESS_TOKEN"` ngay trong lệnh ở workflow, không đặt trong `.phrase.yml`.
5. Chạy thử thủ công để kiểm tra kết nối trước khi để workflow tự động chạy:
   ```bash
   export PHRASE_ACCESS_TOKEN=xxx
   phrase push --wait --access_token="$PHRASE_ACCESS_TOKEN"
   ```
6. Sau khi push thành công, string của cả 3 project sẽ xuất hiện trong Phrase UI (lọc theo tag `mainapp`/`orderservice`/`paymentservice` nếu cần xem riêng). Dịch xong, chạy workflow `phrase-pull.yml` (Actions tab → Run workflow, hoặc chờ lịch chạy) → workflow mở 1 PR chứa cả 3 file `Resources.<locale>.resx` tương ứng để bạn review & merge vào `main`.

## Chạy thử phần code

```bash
dotnet run
```
