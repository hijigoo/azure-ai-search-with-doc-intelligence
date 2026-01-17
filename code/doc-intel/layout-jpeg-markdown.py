# import libraries
import os
import glob
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.ai.documentintelligence.models import DocumentContentFormat

# load environment variables from .env file
load_dotenv()

# set endpoint from environment variable
endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
credential = DefaultAzureCredential()

print("Endpoint:", endpoint)


def analyze_jpeg_to_markdown():
    """
    JPEG 이미지 파일들을 분석하여 마크다운으로 변환합니다.
    """
    # JPEG 파일들이 있는 디렉토리
    jpeg_dir = "sample/sample-jpeg"
    
    # 디렉토리 존재 여부 확인
    if not os.path.exists(jpeg_dir):
        print(f"❌ Error: Directory not found at {jpeg_dir}")
        return
    
    # JPEG 파일 목록 가져오기 (정렬)
    jpeg_files = sorted(glob.glob(os.path.join(jpeg_dir, "*.jpeg")))
    jpeg_files.extend(sorted(glob.glob(os.path.join(jpeg_dir, "*.jpg"))))
    jpeg_files = sorted(set(jpeg_files))  # 중복 제거 및 정렬
    
    if not jpeg_files:
        print(f"❌ Error: No JPEG files found in {jpeg_dir}")
        return
    
    print(f"📂 Processing directory: {jpeg_dir}")
    print(f"📄 Found {len(jpeg_files)} JPEG file(s)")
    print("=" * 80)

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=credential
    )

    # 출력 디렉토리 생성
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 전체 마크다운을 저장할 리스트
    all_markdown_content = []
    
    # 각 JPEG 파일 처리
    for idx, file_path in enumerate(jpeg_files, start=1):
        filename = os.path.basename(file_path)
        print(f"\n📸 Processing {idx}/{len(jpeg_files)}: {filename}")
        
        # 로컬 파일을 바이너리로 읽어서 전송
        with open(file_path, "rb") as f:
            file_content = f.read()
        
        # JPEG 파일 분석 시작
        try:
            poller = document_intelligence_client.begin_analyze_document(
                "prebuilt-layout",
                body=file_content,
                content_type="image/jpeg",
                output_content_format=DocumentContentFormat.MARKDOWN
            )
            
            result: AnalyzeResult = poller.result()
            
            # 마크다운 콘텐츠 추출
            if result.content:
                # 이미지별로 구분선과 제목 추가
                page_header = f"\n\n---\n\n# {filename}\n\n"
                all_markdown_content.append(page_header)
                all_markdown_content.append(result.content)
                
                print(f"   ✅ Analyzed: {len(result.content)} characters")
                
                # 기본 정보 출력
                if result.pages:
                    for page in result.pages:
                        print(f"   📐 Dimensions: {page.width} x {page.height} {page.unit}")
                
                if result.paragraphs:
                    print(f"   📝 Paragraphs: {len(result.paragraphs)}")
                
                if result.tables:
                    print(f"   📊 Tables: {len(result.tables)}")
                
                if result.figures:
                    print(f"   🖼️  Figures: {len(result.figures)}")
            else:
                print(f"   ⚠️  No content extracted")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue
    
    # 모든 마크다운을 하나의 파일로 저장
    output_file = os.path.join(output_dir, "output_jpeg_markdown.md")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("".join(all_markdown_content))
    
    print("\n" + "=" * 80)
    print(f"✅ All JPEG files processed!")
    print(f"   Total files: {len(jpeg_files)}")
    print(f"   Markdown saved to: {output_file}")
    print("=" * 80)


if __name__ == "__main__":
    analyze_jpeg_to_markdown()
