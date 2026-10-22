# Project Advisor

[English](../../README.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [日本語](README.ja.md) · [Tiếng Việt](README.vi.md) · [한국어](README.ko.md) · [فارسی](README.fa.md) · [ภาษาไทย](README.th.md) · [العربية](README.ar.md) · [Français](README.fr.md) · **Bahasa Indonesia**

Skill lintas platform untuk memberi arahan proyek secara kritis, menyusun instruksi terarah bagi agen pelaksana, dan menilai hasil berdasarkan bukti.

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

Gunakan **percakapan dan ruang kerja penasihat yang terpisah, di luar pohon direktori proyek tujuan**. Agen pelaksana tetap berada di ruang kerja proyek dan mengikuti instruksi yang berlaku. Percakapan lain yang masih terkait dengan proyek yang sama tetap dapat memuat `AGENTS.md`, `CLAUDE.md`, atau aturan lokal lain.

Pengaturan ini mengurangi pemuatan otomatis instruksi khusus proyek ke konteks penasihat. Aturan global, instruksi direktori induk, integrasi, dan konteks warisan masih dapat berlaku; isolasi penuh tidak dijamin. Berikan konteks melalui tujuan, dokumen terpilih, dan laporan agen. Penasihat dapat memeriksa aturan proyek sebagai bukti sambil menghormati hierarki instruksi lingkungan.

Simpan status penasihat setiap proyek dalam folder eksternal tersendiri, di luar skill terpasang dan sebaiknya di luar repositori proyek. Jangan terbitkan status pribadi bersama skill.

## Instalasi

Klon atau unduh repositori ini, lalu salin seluruh folder `skills/project-advisor` ke lokasi yang sesuai. Pertahankan `references/` dan `agents/` di samping `SKILL.md`. Tinjau perubahan lokal sebelum menimpa instalasi yang ada.

| Lingkungan | Folder instalasi pribadi | Pemanggilan eksplisit |
|---|---|---|
| Codex | `~/.agents/skills/project-advisor/` | `$project-advisor` |
| Claude Code | `~/.claude/skills/project-advisor/` | `/project-advisor` |
| OpenCode | `~/.config/opencode/skills/project-advisor/` | Pilih atau muat skill secara eksplisit; lihat pengaturan perintah opsional di bawah. |

`~` berarti direktori pengguna Anda, termasuk di Windows. Lokasi ini untuk alat lokal; produk yang dihosting dapat menggunakan mekanisme berbeda. Jika skill belum muncul setelah instalasi, buka sesi penasihat baru.

### Kontrol pemanggilan

Inti skill selalu memerlukan permintaan aktivasi eksplisit. Kontrol lingkungan diatur terpisah:

- **Codex:** berkas `agents/openai.yaml` yang disertakan menetapkan `policy.allow_implicit_invocation: false`.
- **Claude Code:** tambahkan `disable-model-invocation: true` ke frontmatter YAML `SKILL.md` yang terpasang untuk mencegah pemanggilan oleh model. Ini penyesuaian Claude Code, bukan bagian dari berkas bersama.
- **OpenCode:** tambahkan metadata bernilai teks berikut ke frontmatter `SKILL.md` terpasang untuk menyediakan perintah dan mengeluarkan skill dari panduan pemilihan otomatis:

  ```yaml
  metadata:
    opencode/slash: "true"
    opencode/autoinvoke: "false"
  ```

  Kemudian panggil `/project-advisor` pada versi yang mendukung pengaturan ini. Jika klien Anda berbeda, gunakan mekanisme pemuatan skill eksplisitnya.

Ini penyesuaian instalasi lokal; tidak perlu membuat salinan metodologi terpisah dalam repositori. Pertahankan pengaturan frontmatter khusus lingkungan sebelum memperbarui instalasi.

Panduan instalasi dan pemanggilan diperiksa terhadap dokumentasi resmi [Codex](https://learn.chatgpt.com/docs/build-skills), [Claude Code](https://code.claude.com/docs/en/skills), dan [OpenCode](https://opencode.ai/docs/skills/) pada 21 Oktober 2026. **Versi ini belum diuji menyeluruh dari awal hingga akhir pada ketiga klien.** Pemeriksaan dokumentasi bukan sertifikasi kompatibilitas saat dijalankan. Penggunaan penasihat versi Portugis sebelumnya menjadi dasar versi ini; adaptasi Inggris masih memerlukan masukan dari penggunaan nyata yang lebih beragam.

## Aktivasi dan penggunaan

Panggil skill melalui mekanisme lingkungan Anda, lalu jelaskan tujuan dan folder status. Contoh:

```text
Aktifkan Project Advisor.
Gunakan folder status eksternal ini: /jalur/ke/ruang-penasihat-saya.
Agen pelaksana berada di percakapan terpisah.
Saya ingin menambahkan impor pelanggan melalui CSV ke aplikasi yang sudah ada.
```

Penasihat membaca instruksi inti dan status eksternal, atau membuat status jika diperlukan. Penasihat tetap aktif dalam percakapan yang sama sampai Anda menonaktifkannya secara eksplisit:

```text
Nonaktifkan penasihat.
```

Dalam percakapan baru, aktifkan skill lagi dan berikan folder status yang sama untuk melanjutkan proyek. Instalasi saja tidak pernah mengaktifkan peran. Instruksi dan contoh dalam skill berbahasa Inggris; **penasihat berkomunikasi dalam bahasa pilihan Anda**.

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

Penasihat menggunakan `ADVISOR_STATE.md` di ruang eksternal Anda. Saat membuat status baru, `ADVISOR_STATE_TEMPLATE.md` yang sudah ada didahulukan daripada skema cadangan. `STATE_SCHEMA.md` hanya memuat isian generik.

Status dapat berisi keputusan sensitif, jalur, atau fakta proyek. Tentukan penyimpanan dan pembagiannya dengan sengaja. `.gitignore` mengecualikan nama berkas status, tetapi hanya dalam salinan repositori ini dan tidak menghapus berkas yang sudah dilacak. Sebaiknya simpan status pribadi di luar repositori yang dipublikasikan.

Status diringkas dan diperbarui selama giliran aktif ketika informasi berubah secara berarti, saat menutup pekerjaan, atau saat melanjutkan setelah pemadatan konteks bila perlu. Tidak ada proses latar belakang, hook sesi, atau jaminan pemulihan jika konteks aktivasi hilang. Aktifkan kembali dengan folder yang sama jika perlu. Tanpa akses berkas, penasihat dapat memberikan ringkasan untuk Anda simpan, alih-alih mengklaim status sudah disimpan.

Skill menyediakan instruksi, bukan kontrol akses atau jaminan keputusan benar. Perilakunya bergantung pada model, bukti, instruksi lingkungan, dan alat. Skill tidak menerapkan proyek yang dikoordinasikan atau menghubungi agen secara mandiri.

## Struktur repositori

```text
skills/project-advisor/
├── SKILL.md                   Aktivasi, status, dan kelanjutan
├── agents/openai.yaml         Kebijakan pemanggilan khusus Codex
└── references/
    ├── ADVISOR_CORE.md        Metode lintas platform
    └── STATE_SCHEMA.md        Struktur pemulihan status
```

## Kontribusi

Jelaskan masalah nyata, perilaku yang diharapkan, dan mengapa perubahan membantu tanpa menambah proses yang tidak perlu. Gunakan contoh sintetis, hapus informasi pribadi, dan laporkan lingkungan serta batas pemeriksaan perilaku. Pisahkan panduan yang dapat dipakai ulang dari preferensi pribadi atau khusus proyek.

Terjemahan README berada di `.github/readme/`. Saat memperbarui dokumentasi, selaraskan contoh, perintah, tautan, dan batasan dengan README Inggris. Tambahkan navigasi bahasa hanya untuk terjemahan yang ada dalam repositori.

## Lisensi

[MIT](../../LICENSE) — Copyright (c) 2026 Guilherme Rocha.
