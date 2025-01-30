import os
import argparse
from datetime import datetime
import re

# 設定報告目錄 & LaTeX 樣板
REPORTS_DIR = "reports"
TEMPLATE_FILE = "templates/main.tex"

def extract_sections(file_path, target_date=None):
    """
    從 .tex 檔案中擷取符合指定日期的內容（如果有指定日期）。
    如果未指定日期，則輸出所有內容。
    """
    content = ""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    temp_content = ""
    
    for line in lines:
        # 檢查是否是日期標題區段
        match = re.match(r"\\section\{(\d{4}-\d{2}-\d{2})\}", line)
        if match:
            # 如果已經有暫存的內容，加入到最終內容中
            if temp_content.strip():
                content += temp_content + "\n"
            
            # 如果有指定日期，則檢查是否符合
            if target_date:
                section_date = match.group(1)
                if section_date == target_date:
                    temp_content = line  # 如果有指定日期，保留日期標題
            else:
                temp_content = line  # 如果沒有指定日期，保留所有日期標題
        else:
            # 如果沒有指定日期，或者目前的區段符合目標日期，則加入內容
            if not target_date or temp_content:
                temp_content += line
    
    # 加入最後一個區段的內容
    if temp_content.strip():
        content += temp_content

    return content.strip()

def merge_tex_files(date=None, user=None, output_file="output/main.tex"):
    """
    合併所有符合條件的報告，並輸出成新的 .tex 檔案
    """
    tex_content = ""

    if user:
        user_file = os.path.join(REPORTS_DIR, f"{user}.tex")
        if os.path.exists(user_file):
            extracted_content = extract_sections(user_file, date)
            if extracted_content:
                if not date:  # 如果沒有指定日期，只加入使用者標題
                    tex_content += f"\\section{{{user}}}\n" + extracted_content + "\n\n"
                else:  # 如果有指定日期，保持原有格式
                    tex_content += extracted_content + "\n\n"
        else:
            print(f"❌ 找不到 {user} 的報告！")
            return
    else:
        for file_name in os.listdir(REPORTS_DIR):
            if file_name.endswith(".tex"):
                file_path = os.path.join(REPORTS_DIR, file_name)
                user_name = os.path.splitext(file_name)[0]

                extracted_content = extract_sections(file_path, date)
                if extracted_content:
                    tex_content += f"\\section{{{user_name}}}\n" + extracted_content + "\n\n"

    if not tex_content.strip():
        tex_content = f"\\section{{{user if user else date}}}\n沒有找到符合條件的報告。\n"

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    final_tex = template.replace("{{CONTENT}}", tex_content)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_tex)

    print(f"✅ 生成 {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, help="指定日期 (YYYY-MM-DD)")
    parser.add_argument("--user", type=str, help="指定使用者")
    parser.add_argument("--output", type=str, required=True, help="輸出 .tex 檔案")

    args = parser.parse_args()
    merge_tex_files(date=args.date, user=args.user, output_file=args.output)