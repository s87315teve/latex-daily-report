# 定義目錄
REPORTS_DIR = reports
OUTPUT_DIR = output
TEMPLATE_DIR = templates
SCRIPT_DIR = scripts

# 取得當前日期（僅用於預設的 all target）
YEAR := $(shell date +%Y)
MONTH := $(shell date +%m)
DAY := $(shell date +%d)
TODAY := $(YEAR)-$(MONTH)-$(DAY)

# 預設使用 XeLaTeX
LATEXMK = latexmk -pdf -xelatex -interaction=nonstopmode -output-directory=$(OUTPUT_DIR)

# 預設生成當日報告
all:
	python3 $(SCRIPT_DIR)/merge_tex.py --date "$(TODAY)" --output "$(OUTPUT_DIR)/main_$(TODAY).tex"
	$(LATEXMK) "$(OUTPUT_DIR)/main_$(TODAY).tex"

# 生成特定日期的報告
report:
	python3 $(SCRIPT_DIR)/merge_tex.py --date "$(YEAR)-$(MM)-$(DD)" --output "$(OUTPUT_DIR)/main_$(YEAR)-$(MM)-$(DD).tex"
	$(LATEXMK) "$(OUTPUT_DIR)/main_$(YEAR)-$(MM)-$(DD).tex"

# 生成特定用戶的報告
user:
	@if [ -z "$(USER)" ]; then \
		echo "錯誤：請指定 USER 變數，例如 make user USER=aaa"; \
		exit 1; \
	fi
	@if [ -z "$(DATE)" ]; then \
		echo "生成 $(USER) 的所有歷史報告"; \
		python3 $(SCRIPT_DIR)/merge_tex.py --user "$(USER)" --output "$(OUTPUT_DIR)/main_$(USER).tex"; \
		$(LATEXMK) "$(OUTPUT_DIR)/main_$(USER).tex"; \
	else \
		echo "生成 $(USER) 在 $(DATE) 的報告"; \
		python3 $(SCRIPT_DIR)/merge_tex.py --user "$(USER)" --date "$(DATE)" --output "$(OUTPUT_DIR)/main_$(USER)_$(DATE).tex"; \
		$(LATEXMK) "$(OUTPUT_DIR)/main_$(USER)_$(DATE).tex"; \
	fi

# 清理輸出檔案
clean:
	rm -rf $(OUTPUT_DIR)/*.aux $(OUTPUT_DIR)/*.log $(OUTPUT_DIR)/*.out $(OUTPUT_DIR)/*.pdf $(OUTPUT_DIR)/*.tex