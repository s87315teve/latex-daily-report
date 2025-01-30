# LaTeX 報告合併系統

本系統可根據指定日期或使用者，自動合併 .tex 文件中的對應內容，並輸出 LaTeX PDF 報告。若未指定日期，則預設輸出當天 (YYYY-MM-DD) 的內容。

## 系統特色

* 合併不同使用者的 .tex 報告，自動整合成單一文件
* 使用 `\section{使用者名稱}` 作為標題，確保報告架構清晰
* 支援日期區段 `\section{YYYY-MM-DD}`，方便歷史追蹤
* 提供 make 指令支援，實現一鍵編譯 PDF 功能
* 自動檢查內容，若查無資料則輸出提示訊息

## 目錄結構

```
/報告系統/
│── reports/            # 存放各使用者的 .tex 報告
│     ├── aaa.tex       # 例如 AAA 使用者的報告
│     ├── bbb.tex       # 例如 BBB 使用者的報告
│── templates/          # LaTeX 樣板
│     ├── main.tex      # 合併 LaTeX 模板
│── output/             # 生成的 PDF 檔案
│── scripts/            # Python 腳本
│     ├── merge_tex.py  # 負責合併 .tex 檔案
│── Makefile           # 控制 LaTeX 編譯
│── README.md          # 使用說明
```

## 使用方法

### 1. 生成當天的報告

使用 make 指令：
```bash
make
```

輸出檔案：`output/main_YYYY-MM-DD.pdf`

### 2. 生成指定日期的報告

```bash
make YEAR=2025 MM=01 DD=30
```

輸出檔案：`output/main_2025-01-30.pdf`

### 3. 生成特定使用者的報告

生成所有歷史報告：
```bash
make user USER=aaa
```
輸出檔案：`output/main_aaa.pdf`

生成特定日期的報告：
```bash
make user USER=aaa DATE=2024-01-30
```
輸出檔案：`output/main_aaa_2024-01-30.pdf`

### 4. 清除輔助檔案

```bash
make clean
```
將清除所有暫存檔，包括 .aux、.log、.out、.pdf、.tex 等檔案。