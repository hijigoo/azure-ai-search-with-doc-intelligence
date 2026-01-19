# Azure AI Search with Document Intelligence

Azure Document Intelligence와 Azure AI Search를 활용한 문서 처리 및 지식 기반 검색 튜토리얼입니다.

## 📋 개요

이 프로젝트는 Azure의 AI 서비스를 활용하여 PDF, PPTX 등의 문서에서 콘텐츠를 추출하고, Azure AI Search의 Knowledge Base를 통해 에이전틱 검색(Agentic Retrieval)을 수행하는 방법을 다룹니다.

### 주요 기능
- **Document Intelligence**: PDF/PPTX 문서에서 텍스트, 테이블, 이미지 추출
- **Layout 분석**: 문서 구조 분석 및 Markdown 변환
- **Polygon 좌표 추출**: 문서 요소의 위치 정보 추출
- **Knowledge Base 검색**: Azure AI Search를 통한 지능형 문서 검색

## 🗂️ 프로젝트 구조

```
├── README.md
├── tutorials/                      # 튜토리얼 문서 및 노트북
│   ├── 01-setup.md                 # 환경 설정 가이드
│   ├── 02-entra-id-setup.md        # Microsoft Entra ID 설정
│   ├── 03-doc-intel-extract.md     # Document Intelligence 추출 가이드
│   ├── 04-aisearch-indexing.md     # AI Search 인덱싱 가이드
│   ├── 05-knowledge-base.md        # Knowledge Base 설정 가이드
│   ├── code-01-doc-intel-extract.ipynb  # Document Intelligence 튜토리얼 노트북
│   ├── code-02-knowledge-base.ipynb     # Knowledge Base 튜토리얼 노트북
│   ├── samples/                    # 튜토리얼용 샘플 파일
│   ├── output/                     # 추출 결과 출력 폴더
│   └── images/                     # 튜토리얼 이미지
├── code/                           # 참조 코드
│   ├── doc-intel/                  # Document Intelligence 스크립트
│   └── aisearch-kb/                # AI Search Knowledge Base 스크립트
└── samples/                        # 샘플 PDF 문서
```

## 🚀 시작하기

### 사전 요구사항

- Python 3.10+
- Azure 구독
- Azure Document Intelligence 리소스
- Azure AI Search 리소스
- Azure OpenAI 리소스 (Knowledge Base 사용 시)

### 환경 설정

1. **저장소 클론**
   ```bash
   git clone https://github.com/hijigoo/azure-ai-search-with-doc-intelligence.git
   cd azure-ai-search-with-doc-intelligence
   ```

2. **가상환경 생성 및 활성화**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # .venv\Scripts\activate   # Windows
   ```

3. **환경 변수 설정**
   
   `.env` 파일을 생성하고 다음 변수를 설정합니다:
   ```env
   # Azure Document Intelligence
   AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://your-doc-intel.cognitiveservices.azure.com
   AZURE_DOCUMENT_INTELLIGENCE_KEY=your-doc-intel-key
   
   # Azure AI Search
   AZURE_SEARCH_SERVICE_ENDPOINT=https://your-search.search.windows.net
   AZURE_SEARCH_ADMIN_KEY=your-search-admin-key
   AZURE_KNOWLEDGE_BASE_NAME=kb-documents
   AZURE_KNOWLEDGE_SOURCE_NAME=ks-documents
   
   # Azure OpenAI (Knowledge Base 사용 시)
   AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com
   AZURE_OPENAI_API_KEY=your-openai-key
   AZURE_OPENAI_GPT_DEPLOYMENT=gpt-4o
   AZURE_OPENAI_GPT_MODEL=gpt-4o
   ```

## 📚 튜토리얼

### 📖 단계별 가이드 문서

| 순서 | 문서 | 설명 |
|:----:|------|------|
| 1 | [01-setup.md](tutorials/01-setup.md) | Azure 환경 셋업 - 리소스 그룹, Storage Account, Document Intelligence, AI Search, Microsoft Foundry 생성 |
| 2 | [02-entra-id-setup.md](tutorials/02-entra-id-setup.md) | Microsoft Entra ID 기반 역할 기반 접근 제어(RBAC) 설정 - Managed Identity 활성화 및 역할 할당 |
| 3 | [03-doc-intel-extract.md](tutorials/03-doc-intel-extract.md) | Document Intelligence Studio에서 OCR/Read, Layout 모델을 사용한 문서 분석 테스트 |
| 4 | [04-aisearch-indexing.md](tutorials/04-aisearch-indexing.md) | AI Search의 Import data 마법사로 Multimodal RAG 인덱싱 설정 |
| 5 | [05-knowledge-base.md](tutorials/05-knowledge-base.md) | Knowledge Source 및 Knowledge Base 생성, 에이전틱 검색 테스트 |

### 💻 실습 노트북

#### 1. Document Intelligence - 문서 추출
[code-01-doc-intel-extract.ipynb](tutorials/code-01-doc-intel-extract.ipynb)

- PDF/PPTX 문서 분석
- Layout 모델을 사용한 구조 추출
- Markdown 형식으로 콘텐츠 변환
- Polygon 좌표 정보 추출
- 테이블 및 Figure 분석

#### 2. Knowledge Base - 지식 기반 검색
[code-02-knowledge-base.ipynb](tutorials/code-02-knowledge-base.ipynb)

- Knowledge Base 클라이언트 설정
- 에이전틱 검색(Agentic Retrieval) 수행
- 검색 결과 분석 (응답, Activity, References)
- 참조 문서 요약 출력

## 🔐 인증 방식

두 가지 인증 방식을 지원합니다:

| 방식 | 설명 | 사용 환경 |
|------|------|----------|
| **API 키** | 간단한 키 기반 인증 | 로컬 개발 환경 |
| **DefaultAzureCredential** | Azure AD 기반 인증 (`az login` 필요) | 프로덕션 환경 |

## 📦 주요 패키지

```bash
# Document Intelligence
pip install azure-ai-documentintelligence azure-identity python-dotenv

# AI Search Knowledge Base
pip install azure-search-documents --pre
```

## 🔗 참고 자료

- [Azure Document Intelligence 문서](https://learn.microsoft.com/azure/ai-services/document-intelligence/)
- [Azure AI Search 문서](https://learn.microsoft.com/azure/search/)
- [Azure OpenAI 문서](https://learn.microsoft.com/azure/ai-services/openai/)

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
