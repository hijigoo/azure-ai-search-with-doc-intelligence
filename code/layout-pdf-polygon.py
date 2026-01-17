# import libraries
import os
import json
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


def extract_polygon_and_images():
    """
    PDF 파일에서 figure의 polygon 정보를 추출하고 JSON 파일로 저장합니다.
    또한 polygon 좌표를 사용해서 이미지를 추출합니다.
    """
    # PDF 파일 경로
    file_path = "sample/sample-pdf.pdf"
    
    # 파일 존재 여부 확인
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at {file_path}")
        return
    
    print(f"📂 Processing file: {file_path}")
    print("=" * 80)

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=credential
    )

    # 로컬 파일을 바이너리로 읽어서 전송
    with open(file_path, "rb") as f:
        file_content = f.read()
        
    # PDF 파일 분석 시작
    print("🔍 Analyzing document...")
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout",
        body=file_content,
        content_type="application/pdf",
        output_content_format=DocumentContentFormat.MARKDOWN
    )

    result: AnalyzeResult = poller.result()
    print("✅ Analysis complete!")
    print("=" * 80)

    # 출력 디렉토리 생성
    output_dir = "output"
    polygon_dir = os.path.join(output_dir, "polygons")
    images_dir = os.path.join(output_dir, "polygon_images")
    os.makedirs(polygon_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    if not result.figures:
        print("❌ No figures found in the document.")
        return

    print(f"\n📊 Found {len(result.figures)} figures")
    print("=" * 80)

    # 전체 polygon 데이터를 담을 리스트
    all_polygons = []
    
    # PyMuPDF로 이미지 추출을 위해 PDF 열기
    try:
        import fitz
        pdf_document = fitz.open(file_path)
        pdf_available = True
    except ImportError:
        print("⚠️  PyMuPDF not installed. Image extraction will be skipped.")
        print("   To enable image extraction, run: pip install PyMuPDF")
        pdf_available = False

    # 각 figure 처리
    for idx, figure in enumerate(result.figures):
        if not figure.bounding_regions:
            continue
        
        figure_num = idx + 1
        bounding_region = figure.bounding_regions[0]
        page_num = bounding_region.page_number
        polygon = bounding_region.polygon
        
        # polygon 정보 구조화
        polygon_data = {
            "figure_id": figure_num,
            "page_number": page_num,
            "polygon_coordinates": polygon,
            "polygon_points": [
                {"x": polygon[i], "y": polygon[i+1]} 
                for i in range(0, len(polygon), 2)
            ],
            "caption": figure.caption.content if hasattr(figure, 'caption') and figure.caption else None,
            "elements_count": len(figure.elements) if hasattr(figure, 'elements') and figure.elements else 0
        }
        
        # bounding box 계산
        if len(polygon) >= 8:
            coords = [(polygon[i], polygon[i+1]) for i in range(0, len(polygon), 2)]
            x_coords = [c[0] for c in coords]
            y_coords = [c[1] for c in coords]
            
            polygon_data["bounding_box"] = {
                "x_min": min(x_coords),
                "y_min": min(y_coords),
                "x_max": max(x_coords),
                "y_max": max(y_coords),
                "width": max(x_coords) - min(x_coords),
                "height": max(y_coords) - min(y_coords)
            }
        
        all_polygons.append(polygon_data)
        
        # 개별 polygon JSON 파일로 저장
        figure_json_file = os.path.join(polygon_dir, f"figure_{figure_num:03d}_page{page_num:02d}_polygon.json")
        with open(figure_json_file, "w", encoding="utf-8") as f:
            json.dump(polygon_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📐 Figure {figure_num} (Page {page_num}):")
        print(f"   Polygon file: {figure_json_file}")
        
        if polygon_data.get("caption"):
            print(f"   Caption: {polygon_data['caption'][:60]}...")
        
        # 이미지 추출 (PyMuPDF 사용 가능한 경우)
        if pdf_available and len(polygon) >= 8:
            try:
                page = pdf_document[page_num - 1]  # 0-based index
                
                # polygon에서 bounding box 계산
                coords = [(polygon[i], polygon[i+1]) for i in range(0, len(polygon), 2)]
                x_coords = [c[0] for c in coords]
                y_coords = [c[1] for c in coords]
                x0, y0 = min(x_coords), min(y_coords)
                x1, y1 = max(x_coords), max(y_coords)
                
                # 좌표를 PyMuPDF 형식으로 변환 (inch -> points, 1 inch = 72 points)
                rect = fitz.Rect(x0 * 72, y0 * 72, x1 * 72, y1 * 72)
                
                # 영역을 이미지로 추출 (2x scale for better quality)
                pix = page.get_pixmap(clip=rect, matrix=fitz.Matrix(2, 2))
                
                # 파일명 생성
                image_file = os.path.join(images_dir, f"figure_{figure_num:03d}_page{page_num:02d}.png")
                pix.save(image_file)
                
                print(f"   Image saved: {image_file}")
                print(f"   Image size: {pix.width}x{pix.height} pixels")
                
            except Exception as e:
                print(f"   ⚠️  Error extracting image: {e}")
    
    if pdf_available:
        pdf_document.close()
    
    # 전체 polygon 데이터를 하나의 JSON 파일로 저장
    all_polygons_file = os.path.join(output_dir, "all_polygons.json")
    summary_data = {
        "source_file": file_path,
        "total_figures": len(all_polygons),
        "total_pages": len(result.pages) if result.pages else 0,
        "figures": all_polygons
    }
    
    with open(all_polygons_file, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print(f"✅ Polygon extraction complete!")
    print(f"   Total figures processed: {len(all_polygons)}")
    print(f"   Individual polygon files: {polygon_dir}/")
    print(f"   All polygons summary: {all_polygons_file}")
    if pdf_available:
        print(f"   Extracted images: {images_dir}/")
    print("=" * 80)


if __name__ == "__main__":
    extract_polygon_and_images()
