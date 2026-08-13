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

| File | Vai trò |
|---|---|
| [`Resources/Resources.resx`](Resources/Resources.resx) | File nguồn (en) — nơi dev thêm string mới |
| [`.phrase.yml`](.phrase.yml) | Config cho Phrase CLI: khai báo file nào là source (push), file nào là target dịch (pull) |
| [`.github/workflows/phrase-push.yml`](.github/workflows/phrase-push.yml) | Khi `Resources.resx` thay đổi trên `main` → tự động push string mới lên Phrase |
| [`.github/workflows/phrase-pull.yml`](.github/workflows/phrase-pull.yml) | Chạy theo lịch (hoặc bấm tay) → kéo bản dịch đã hoàn thành từ Phrase về, mở PR vào `main` |

## Những gì demo này đã dựng sẵn (chạy local được)

- Cấu trúc `Resources/Resources.resx` + code đọc resource trong [`Program.cs`](Program.cs).
- Config `.phrase.yml` và 2 workflow GitHub Actions dùng action chính thức [`phrase/setup-cli`](https://github.com/phrase/setup-cli) để cài Phrase CLI, sau đó chạy `phrase push` / `phrase pull`.
- Git repo (đã push lên [Linhnth17/Phrase-Test](https://github.com/Linhnth17/Phrase-Test)) với các commit minh họa từng bước.

## Các bước để kết nối với project Phrase thật

1. Đăng nhập [phrase.com](https://phrase.com) (hoặc tạo account), tạo một **Strings project** mới (hoặc dùng project có sẵn).
2. Lấy 2 giá trị từ Phrase:
   - **Project ID**: trong project → Settings → xem "Project ID".
   - **Access Token**: Account Settings → API Access → tạo Personal Access Token (cần quyền đọc/ghi lên project đó).
3. Vào repo GitHub → **Settings → Secrets and variables → Actions → New repository secret**, thêm 2 secret:
   - `PHRASE_ACCESS_TOKEN`
   - `PHRASE_PROJECT_ID`
   (`.phrase.yml` trong repo đã tham chiếu 2 biến này sẵn, không cần sửa file này.)
4. Kiểm tra `Resources/Resources.resx` khớp với ngôn ngữ nguồn (`locale_id: en`) đã cấu hình trong `.phrase.yml` — nếu source locale trên Phrase khác `en`, sửa lại giá trị này.
5. Chạy thử thủ công để kiểm tra kết nối trước khi để workflow tự động chạy:
   ```bash
   export PHRASE_ACCESS_TOKEN=xxx
   export PHRASE_PROJECT_ID=xxx
   phrase push --wait   # đẩy Resources.resx lên Phrase, tạo/khớp key
   ```
6. Sau khi push thành công, string sẽ xuất hiện trong Phrase UI để dịch. Dịch xong (hoặc đánh dấu "reviewed"), chạy workflow `phrase-pull.yml` (Actions tab → Run workflow, hoặc chờ lịch chạy) → workflow tạo PR chứa `Resources.<locale>.resx` (ví dụ `Resources.fr.resx`) để bạn review & merge vào `main`.

## Chạy thử phần code

```bash
dotnet run
```
