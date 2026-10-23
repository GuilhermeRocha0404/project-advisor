# Project Advisor

[English](../../README.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [日本語](README.ja.md) · [Tiếng Việt](README.vi.md) · [한국어](README.ko.md) · [فارسی](README.fa.md) · [ภาษาไทย](README.th.md) · [العربية](README.ar.md) · [Français](README.fr.md) · **Bahasa Indonesia**

Metode konsultasi proyek yang independen dari model, dengan adaptor ruang kerja untuk Codex, Claude Code, dan OpenCode.

Gunakan satu percakapan untuk menentukan pekerjaan berikutnya yang bernilai dan agen lain untuk menyelidiki, menerapkan, serta memverifikasi. Penasihat menguji asumsi yang lemah, menyarankan proses yang sebanding dengan masalah, dan menilai hasilnya. Keputusan tentang tujuan, prioritas, dan preferensi tetap berada di tangan Anda.

Metode ini tidak mewajibkan model, penyedia, plugin, atau layanan eksternal tertentu. Skill ditujukan untuk proyek pengembangan dalam lingkungan agen yang dapat memuat instruksi dan berkas pendukungnya.

## Contoh alur kerja

Anda ingin menambahkan impor pelanggan melalui CSV ke aplikasi yang sudah ada.

| Langkah | Siapa | Contoh |
|---|---|---|
| Jelaskan tujuan | Anda → penasihat | “Saya ingin staf mengimpor CSV pelanggan tanpa membuat data ganda.” |
| Perjelas ambiguitas nyata | Penasihat ↔ Anda | “Apakah email yang berulang memperbarui pelanggan lama atau ditandai untuk ditinjau?” Anda memilih peninjauan. |
| Siapkan pelaksanaan | Penasihat → Anda | Instruksi untuk agen yang menjelaskan perilaku impor, penanganan duplikat, batas otorisasi yang berlaku, dan bukti penyelesaian. |
| Laksanakan | Anda → agen | Anda menyampaikan instruksi kepada agen di ruang kerja proyek. Agen menyelidiki, menerapkan, dan memverifikasi. |
| Bawa hasil kembali | Anda → penasihat | Agen melaporkan impor berhasil serta pemeriksaan baris tidak valid dan duplikat dalam satu berkas. |
| Nilai bukti | Penasihat → Anda | Penasihat melihat bahwa impor berkas yang sama dua kali belum diperiksa, lalu meminta verifikasi itu saja. |
| Selesaikan atau perbaiki | Agen → Anda → penasihat | Hasil menunjukkan perilaku yang diharapkan, atau cacat diperbaiki. Penasihat menutup tugas ketika buktinya cukup. |

Ini contoh, bukan urutan wajib. Tugas yang jelas dapat langsung dilaksanakan; perencanaan berlebihan dan verifikasi berulang tidak dianjurkan. Skill tidak menghubungkan atau mengirim pesan antarpercakapan secara otomatis.

## Pengaturan yang disarankan

Gunakan satu folder dan chat penasihat khusus untuk setiap proyek, di luar repositori sasaran. Proyek lain mendapat folder dan status baru. Agen pelaksana tetap berada di repositori. Instruksi global dan folder induk masih dapat berlaku.

## Instalasi

Salin seluruh folder `skills/project-advisor` beserta subfoldernya ke direktori skill pribadi lingkungan Anda. Gunakan Python 3.10+ untuk melihat pratinjau, lalu ulangi dengan `--apply` setelah meninjau perbedaannya. Ganti jalur contoh dan pilih `codex`, `claude`, atau `opencode`.

```sh
python <skill-dir>/scripts/workspace.py --workspace <advisor-dir> --project <target-dir> --harness codex
python <skill-dir>/scripts/workspace.py --workspace <advisor-dir> --project <target-dir> --harness codex --apply
```

Codex: `$project-advisor` · Claude Code: `/project-advisor` · OpenCode: `project-advisor`

[Codex / Claude Code / OpenCode — setup, updates, migration](../../skills/project-advisor/references/HARNESSES.md)

## Aktivasi dan penggunaan

Buka chat baru di folder yang disiapkan. Pemuatan instruksi lokal mengaktifkan penasihat untuk proyek terkait; pemasangan skill saja tidak mengaktifkan chat lain. Periksa peran, proyek, status, dan langkah berikutnya. Penonaktifan eksplisit berlaku untuk chat saat ini; chat baru kembali menjadi penasihat. Jawaban mengikuti bahasa pilihan Anda.

## Peran penasihat

- Menghubungkan tugas berikutnya dengan hasil proyek yang berguna.
- Mempertanyakan keputusan ketika ada masalah konkret dan menawarkan alternatif.
- Menanyakan preferensi, prioritas, maksud, dan fakta yang dapat Anda jelaskan.
- Melakukan penelitian terarah untuk pertanyaan teknis atau khusus.
- Menyesuaikan perencanaan, delegasi, dan verifikasi dengan risiko serta ketidakpastian.
- Menilai bukti agen dan berhenti ketika tugas cukup tuntas.
- Menghormati keputusan yang dibuat dengan pemahaman dan batas otorisasi.
- Menjaga catatan kelanjutan yang ringkas dan terkini, bukan tumpukan log aktivitas.

## Status, privasi, dan batasan

`AGENTS.md` memuat metode; `CLAUDE.md` mengimpornya bila diperlukan. `.advisor-workspace.json` mencatat proyek, lingkungan, versi, dan hash. Status pribadi disimpan di `ADVISOR_STATE.md`; `CONSULTOR_STATE.md` lama dapat dipertahankan. Baca status sebelum memakai `--adopt-existing-state`. Simpan preferensi di `ADVISOR_LOCAL.md`. Pembaruan menampilkan perbedaan dan menolak instruksi yang telah diubah; tinjau dan gabungkan secara eksplisit. Status lama tidak ditimpa. Tidak ada hook atau layanan latar belakang. Pengujian pemasang tidak membuktikan perilaku semua klien.

## Struktur repositori

Template adalah satu-satunya sumber metode yang didistribusikan; setiap workspace mendapat salinan berversi. Tidak ada CORE terpisah. Memperbarui skill tidak otomatis memperbarui workspace. Jangan publikasikan status atau pengaturan pribadi.

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

## Kontribusi

Jelaskan masalah nyata, perilaku yang diharapkan, dan mengapa perubahan membantu tanpa menambah proses yang tidak perlu. Gunakan contoh sintetis, hapus informasi pribadi, dan laporkan lingkungan serta batas pemeriksaan perilaku. Pisahkan panduan yang dapat dipakai ulang dari preferensi pribadi atau khusus proyek.

Terjemahan README berada di `.github/readme/`. Saat memperbarui dokumentasi, selaraskan contoh, perintah, tautan, dan batasan dengan README Inggris. Tambahkan navigasi bahasa hanya untuk terjemahan yang ada dalam repositori.

## Lisensi

[MIT](../../LICENSE) — Copyright (c) 2026 Guilherme Rocha.

## 2.1

Revisi 2.1.0: status membedakan asal bukti dan menyelaraskan keputusan yang diganti, sambil mempertahankan batasan aktif dan verifikasi terbuka. Pemasang memakai satu skema status, mempertahankan nama lama, serta memperjelas pemulihan manifes dan kunci. Belum ada perbandingan terkontrol yang membuktikan manfaat kualitas, waktu, atau biaya. Pengujian adaptor tidak membuktikan eksekusi nyata di setiap lingkungan; dalam chat tanpa akses berkas, metode dan status harus diberikan dan disimpan secara manual.

[English technical reference](../../docs/AUDIT_2_1.md) · [Examples](../../skills/project-advisor/references/EXAMPLES.md)
