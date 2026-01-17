# import libraries
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.ai.documentintelligence.models import DocumentContentFormat
import fitz  # PyMuPDF for image extraction

# load environment variables from .env file
load_dotenv()

# set endpoint from environment variable
endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
credential = DefaultAzureCredential()

print("Endpoint:", endpoint)


def analyze_layout_to_markdown():
    # ✨ 변경: PDF 파일 경로로 변경
    file_path = "sample/sample-pptx.pptx"
    
    # 파일 존재 여부 확인
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at {file_path}")
        return
    
    print(f"📂 Processing file: {file_path}")

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=credential
    )

    # 로컬 파일을 바이너리로 읽어서 전송
    with open(file_path, "rb") as f:
        file_content = f.read()
        
    # PDF 파일 분석 시작
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout",
        body=file_content,
        content_type="application/pdf",  # PDF content type
        output_content_format=DocumentContentFormat.MARKDOWN
    )

    result: AnalyzeResult = poller.result()

    # 마크다운 콘텐츠 추출 및 출력
    print("=" * 80)
    print("📄 Extracted Markdown Content:")
    print("=" * 80)
    
    if result.content:
        print(result.content)
    else:
        print("No markdown content found.")
    
    print("\n" + "=" * 80)
    
    # 마크다운 파일로 저장
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)  # output 폴더 생성

    # ✨ 변경: 출력 파일명을 pdf에 맞게 변경
    output_file = os.path.join(output_dir, "output_pdf_markdown.md")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result.content if result.content else "")
    
    print(f"✅ Markdown saved to: {output_file}")
    print("=" * 80)

    # 기본 문서 정보 출력
    print("\n📊 Document Analysis Summary:")
    print("-" * 80)
    
    if result.pages:
        print(f"Total pages: {len(result.pages)}")
        for page in result.pages:
            print(f"  Page {page.page_number}: {page.width} x {page.height} {page.unit}")
    
    if result.tables:
        print(f"\nTables found: {len(result.tables)}")
        for idx, table in enumerate(result.tables):
            print(f"  Table {idx + 1}: {table.row_count} rows x {table.column_count} columns")
    
    if result.paragraphs:
        print(f"\nParagraphs found: {len(result.paragraphs)}")
    
    # ✨ 추가: 이미지/그림 정보 및 캡션 출력
    if result.figures:
        print(f"\nFigures/Images found: {len(result.figures)}")
        for idx, figure in enumerate(result.figures):
            caption = ""
            if hasattr(figure, 'caption') and figure.caption:
                caption = f" - Caption: {figure.caption.content}"
            elif hasattr(figure, 'elements') and figure.elements:
                caption = f" - Elements: {len(figure.elements)}"
            print(f"  Figure {idx + 1}: Page {figure.bounding_regions[0].page_number if figure.bounding_regions else 'N/A'}{caption}")
    
    print("-" * 80)


if __name__ == "__main__":
    analyze_layout_to_markdown()
