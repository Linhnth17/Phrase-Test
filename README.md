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
- Config `.phrase.yml` và 2 workflow GitHub Actions theo đúng pattern chính thức của Phrase (dùng action `phrase/phrase-cli-action`).
- Git repo local với các commit minh họa từng bước.

## Những gì cần bạn tự làm để chạy "live" (cần tài khoản/quyền thật)

1. Tạo project trên [phrase.com](https://phrase.com), lấy `PHRASE_ACCESS_TOKEN` và `PHRASE_PROJECT_ID`.
2. Tạo repo GitHub thật, push repo này lên.
3. Vào repo Settings → Secrets → thêm `PHRASE_ACCESS_TOKEN`, `PHRASE_PROJECT_ID`.
4. Trong Phrase, bật GitHub integration hoặc để 2 workflow trên tự chạy — khi đó:
   - Push string mới → tự lên Phrase UI để dịch.
   - Sau khi dịch xong trên Phrase → workflow `phrase-pull.yml` tạo PR chứa file `Resources.<locale>.resx` (ví dụ `Resources.fr.resx`, `Resources.vi.resx`) để merge vào `main`.

## Chạy thử phần code

```bash
dotnet run
```
