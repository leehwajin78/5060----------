import os
import glob
import re
from datetime import datetime

base_dir = r"e:\꿈몰다\외부사업\2026\모두의연구소\5060 브랜드 매니지먼트\5060-brand-management-workbase\my-healthcare-workbase"
raw_dir = os.path.join(base_dir, "raw", "assets")
wiki_dir = os.path.join(base_dir, "wiki")
sources_dir = os.path.join(wiki_dir, "sources")

categories = {
    "market_analysis": ["1_", "2_", "3_", "4_", "5_", "6_", "7_", "8_", "9_", "10_"],
    "product_specs": ["PRD", "SRS"],
    "strategy": ["Value", "사업기획서"],
    "coaching": ["코칭", "42Q"]
}

for cat in categories.keys():
    os.makedirs(os.path.join(sources_dir, cat), exist_ok=True)
os.makedirs(os.path.join(wiki_dir, "frameworks"), exist_ok=True)
os.makedirs(os.path.join(wiki_dir, "entities", "personas"), exist_ok=True)
os.makedirs(os.path.join(wiki_dir, "entities", "competitors"), exist_ok=True)
os.makedirs(os.path.join(wiki_dir, "concepts", "business_strategy"), exist_ok=True)
os.makedirs(os.path.join(wiki_dir, "concepts", "product_design"), exist_ok=True)

files = glob.glob(os.path.join(raw_dir, "*.md"))

source_entries = {cat: [] for cat in categories.keys()}
source_entries["uncategorized"] = []

log_entries = []

for file_path in files:
    filename = os.path.basename(file_path)
    if filename == "나다운 브랜딩 5060 코칭 가이드 42문항.md" and os.path.exists(os.path.join(sources_dir, "나다운_브랜딩_5060_코칭_가이드_42문항.md")):
        # We already processed this, but let's move it to category
        pass
    
    # Read first few lines for title and summary
    title = filename.replace(".md", "")
    summary = ""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(2000)
            headers = re.findall(r"^#\s+(.+)$", content, re.MULTILINE)
            if headers:
                title = headers[0].strip()
            
            # Find a short paragraph for summary
            paragraphs = re.findall(r"^(?![#\-\*]).+$", content, re.MULTILINE)
            for p in paragraphs:
                p = p.strip()
                if len(p) > 20:
                    summary = p[:150] + ("..." if len(p) > 150 else "")
                    break
    except Exception as e:
        summary = "요약 정보를 추출할 수 없습니다."

    # Determine category
    assigned_cat = "uncategorized"
    for cat, prefixes in categories.items():
        if any(filename.startswith(p) or p in filename for p in prefixes):
            assigned_cat = cat
            break
            
    source_filename = filename.replace(" ", "_")
    source_file_path = os.path.join(sources_dir, assigned_cat, source_filename)
    
    with open(source_file_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"- **원본 파일**: `raw/assets/{filename}`\n")
        f.write(f"- **카테고리**: {assigned_cat}\n\n")
        f.write("## 자동 추출 요약\n")
        f.write(f"{summary}\n\n")
        f.write("## 메타데이터 및 태그\n")
        f.write("- [작성 필요]\n")
        
    source_entries[assigned_cat].append(f"- [{title}](sources/{assigned_cat}/{source_filename})")
    log_entries.append(f"- `{filename}` -> `sources/{assigned_cat}/` 수집 완료")

# Build new index
index_path = os.path.join(wiki_dir, "index.md")
with open(index_path, "w", encoding="utf-8") as f:
    f.write("# 위키 인덱스 (Index)\n\n")
    f.write("위키 내의 모든 정보에 대한 체계적 카탈로그입니다. (자동 생성됨)\n\n")
    
    f.write("## 📁 Sources (출처 문서)\n\n")
    f.write("### 시장 및 경쟁 분석 (Market Analysis)\n")
    for entry in source_entries.get("market_analysis", []): f.write(entry + "\n")
    
    f.write("\n### 제품 및 요구사항 (Product Specs)\n")
    for entry in source_entries.get("product_specs", []): f.write(entry + "\n")
    
    f.write("\n### 전략 및 비즈니스 (Strategy)\n")
    for entry in source_entries.get("strategy", []): f.write(entry + "\n")
    
    f.write("\n### 코칭 프레임워크 (Coaching)\n")
    for entry in source_entries.get("coaching", []): f.write(entry + "\n")
    
    f.write("\n### 기타 (Uncategorized)\n")
    for entry in source_entries.get("uncategorized", []): f.write(entry + "\n")
    
    f.write("\n## 💡 Concepts (핵심 개념)\n")
    f.write("### 비즈니스 전략 (Business Strategy)\n")
    f.write("- *(문서 생성 필요)*\n")
    f.write("### 기획 및 설계 (Product Design)\n")
    f.write("- [브랜드 프로필 매핑](concepts/브랜드_프로필_매핑.md)\n")
    f.write("- [5060 특화 인사이트](concepts/5060_특화_인사이트.md)\n")
    
    f.write("\n## 📐 Frameworks (분석 프레임워크)\n")
    f.write("- *(문서 생성 필요)*\n")
    
    f.write("\n## 👤 Entities (엔티티)\n")
    f.write("### 페르소나 (Personas)\n")
    f.write("- *(문서 생성 필요)*\n")
    f.write("### 경쟁자 (Competitors)\n")
    f.write("- *(문서 생성 필요)*\n")

# Append to log
log_path = os.path.join(wiki_dir, "log.md")
today = datetime.now().strftime("%Y-%m-%d")
with open(log_path, "a", encoding="utf-8") as f:
    f.write(f"\n## [{today}] bulk_ingest | 일괄 지식베이스 마이그레이션\n")
    f.write("`raw/assets/` 내의 16개 파일을 카테고리별로 분류하고 Source 페이지를 자동 생성함.\n")
    for log in log_entries:
        f.write(log + "\n")
    f.write("- 위키 디렉토리 구조 확장 (`frameworks`, `entities/personas`, `entities/competitors` 등)\n")
    f.write("- `index.md` 구조 전면 개편 및 자동 갱신.\n")

print("Ingestion script completed successfully.")
