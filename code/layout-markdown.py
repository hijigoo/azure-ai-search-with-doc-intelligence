# import libraries
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
# ✨ 변경: DocumentContentFormat 임포트 추가 (마크다운 출력 형식 지정용)
from azure.ai.documentintelligence.models import DocumentContentFormat

# load environment variables from .env file
load_dotenv()

# set endpoint from environment variable
endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
credential = DefaultAzureCredential()

print("Endpoint:", endpoint)


def analyze_layout_to_markdown():
    # sample document
    formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-layout.pdf"

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=credential
    )

    # ✨ 변경: output_content_format 파라미터 추가하여 마크다운 형식으로 출력 요청
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout", 
        AnalyzeDocumentRequest(url_source=formUrl),
        output_content_format=DocumentContentFormat.MARKDOWN  # 마크다운 형식 지정
    )

    result: AnalyzeResult = poller.result()

    # ✨ 변경: 마크다운 콘텐츠 추출 및 출력
    print("=" * 80)
    print("📄 Extracted Markdown Content:")
    print("=" * 80)
    
    if result.content:
        print(result.content)
    else:
        print("No markdown content found.")
    
    print("\n" + "=" * 80)
    
    # ✨ 추가: 마크다운 파일로 저장
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)  # output 폴더 생성
    output_file = os.path.join(output_dir, "output_markdown.md")
    
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
    
    print("-" * 80)


if __name__ == "__main__":
    analyze_layout_to_markdown()
