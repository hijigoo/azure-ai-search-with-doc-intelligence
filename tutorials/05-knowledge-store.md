# 05. Knowledge Store 생성하기

이 문서에서는 AI Search의 Knowledge Store를 생성하여 Document Intelligence로 추출한 데이터를 영구 저장하고 다양한 용도로 활용하는 방법을 안내합니다.

## 📋 목차

1. [개요](#1-개요)
2. [Knowledge Store 아키텍처](#2-knowledge-store-아키텍처)
3. [Knowledge Store 프로젝션 설정](#3-knowledge-store-프로젝션-설정)
4. [인덱서 재실행](#4-인덱서-재실행)
5. [Knowledge Store 데이터 확인](#5-knowledge-store-데이터-확인)
6. [데이터 활용 방법](#6-데이터-활용-방법)

---

## 1. 개요

### Knowledge Store란?

Knowledge Store는 AI Search의 인덱싱 파이프라인에서 추출/변환된 데이터를 Azure Storage에 영구 저장하는 기능입니다. 검색 인덱스와 별개로 데이터를 저장하여 다양한 분석 및 활용이 가능합니다.

### Knowledge Store vs Search Index

| 항목 | Search Index | Knowledge Store |
|------|--------------|-----------------|
| 목적 | 검색 쿼리 응답 | 데이터 저장 및 분석 |
| 저장 위치 | AI Search 내부 | Azure Storage |
| 형식 | 역인덱스 구조 | Table/Blob/File |
| 쿼리 | 검색 API | Storage API/분석 도구 |
| 활용 | 검색 애플리케이션 | BI, ML, 데이터 분석 |

### Knowledge Store 저장 형식

| 프로젝션 유형 | 저장 위치 | 용도 |
|--------------|----------|------|
| **Table** | Table Storage | 구조화된 데이터, BI 분석 |
| **Object** | Blob Storage | JSON 문서, ML 학습 데이터 |
| **File** | Blob Storage | 이미지, 바이너리 파일 |

---

## 2. Knowledge Store 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                    Knowledge Store 아키텍처                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐                          │
│  │ Blob Storage │───▶│   Skillset   │                          │
│  │   (원본 문서)  │    │   (AI 처리)   │                          │
│  └──────────────┘    └──────┬───────┘                          │
│                             │                                   │
│              ┌──────────────┴──────────────┐                   │
│              │                             │                   │
│              ▼                             ▼                   │
│     ┌──────────────┐            ┌──────────────────┐          │
│     │ Search Index │            │ Knowledge Store  │          │
│     │  (검색용)     │            │   (저장/분석용)   │          │
│     └──────────────┘            └────────┬─────────┘          │
│                                          │                     │
│                    ┌─────────────────────┼─────────────────┐  │
│                    │                     │                 │  │
│                    ▼                     ▼                 ▼  │
│            ┌────────────┐       ┌────────────┐     ┌──────────┐│
│            │   Tables   │       │  Objects   │     │  Files   ││
│            │ (구조화 데이터)│       │  (JSON)    │     │ (이미지) ││
│            └────────────┘       └────────────┘     └──────────┘│
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Knowledge Store 프로젝션 설정

기존 스킬셋에 Knowledge Store 프로젝션을 추가합니다.

### 3.1 스킬셋 편집

1. **AI Search > Skillsets 메뉴 클릭**
2. **`ss-doc-extraction` 클릭**
3. **JSON 정의 편집**

   ![스킬셋 편집](./images/05-01-skillset-edit.png)

### 3.2 Knowledge Store 정의 추가

스킬셋 JSON에 `knowledgeStore` 섹션을 추가합니다:

```json
{
  "name": "ss-doc-extraction",
  "description": "Document extraction skillset with Knowledge Store",
  "skills": [...],
  "knowledgeStore": {
    "storageConnectionString": "ResourceId=/subscriptions/{subscription-id}/resourceGroups/rg-doc-intelligence-lab/providers/Microsoft.Storage/storageAccounts/{storage-account-name}",
    "projections": [
      {
        "tables": [
          {
            "tableName": "Documents",
            "generatedKeyName": "DocumentId",
            "source": "/document"
          },
          {
            "tableName": "Pages",
            "generatedKeyName": "PageId",
            "source": "/document/pages/*"
          },
          {
            "tableName": "KeyPhrases",
            "generatedKeyName": "KeyPhraseId",
            "source": "/document/keyphrases/*"
          }
        ],
        "objects": [
          {
            "storageContainer": "knowledge-store",
            "generatedKeyName": "ObjectId",
            "source": "/document"
          }
        ]
      }
    ]
  }
}
```

   ![Knowledge Store JSON](./images/05-02-knowledge-store-json.png)

### 3.3 Storage 연결 문자열 설정

1. **Managed Identity 사용 (권장)**:
```json
"storageConnectionString": "ResourceId=/subscriptions/{subscription-id}/resourceGroups/rg-doc-intelligence-lab/providers/Microsoft.Storage/storageAccounts/stdocintellab0115"
```

2. **연결 정보 확인**:
   - Azure Portal > Storage Account > Settings > Endpoints

   ![Storage 연결](./images/05-03-storage-connection.png)

### 3.4 프로젝션 구성

#### Table 프로젝션 (구조화된 데이터)

| 테이블 | 내용 | 용도 |
|--------|------|------|
| `Documents` | 문서 메타데이터 | 문서 목록 조회 |
| `Pages` | 페이지별 내용 | 페이지 단위 분석 |
| `KeyPhrases` | 핵심 구문 | 키워드 분석 |
| `Entities` | 추출된 엔터티 | 엔터티 관계 분석 |

#### Object 프로젝션 (JSON 문서)

| 컨테이너 | 내용 | 용도 |
|----------|------|------|
| `knowledge-store` | 전체 문서 JSON | ML 학습 데이터 |
| `enriched-documents` | 보강된 문서 | 상세 분석 |

   ![프로젝션 설정](./images/05-04-projection-config.png)

### 3.5 스킬셋 저장

1. **JSON 검증 완료 확인**
2. **Save 클릭**

   ![스킬셋 저장](./images/05-05-skillset-save.png)

---

## 4. 인덱서 재실행

Knowledge Store를 채우기 위해 인덱서를 재실행합니다.

### 4.1 인덱서 리셋

1. **AI Search > Indexers 메뉴 클릭**
2. **`idxr-documents` 클릭**
3. **Reset 버튼 클릭**

   > ⚠️ **주의**: Reset은 인덱서 상태를 초기화합니다. 기존 인덱스 데이터는 유지됩니다.

   ![인덱서 리셋](./images/05-06-indexer-reset.png)

### 4.2 인덱서 실행

1. **Run 버튼 클릭**
2. **실행 완료 대기**

   ![인덱서 실행](./images/05-07-indexer-run.png)

### 4.3 실행 결과 확인

1. **Execution history 탭에서 상태 확인**
2. **Documents succeeded 수 확인**

   | 항목 | 확인 사항 |
   |------|----------|
   | Status | Success |
   | Documents succeeded | 문서 수와 일치 |
   | Warnings | Knowledge Store 관련 경고 없음 |

   ![실행 결과](./images/05-08-execution-result.png)

---

## 5. Knowledge Store 데이터 확인

### 5.1 Table Storage 확인

1. **Azure Portal > Storage Account로 이동**
2. **왼쪽 메뉴 > Data storage > Tables 클릭**
3. **생성된 테이블 확인**

   | 테이블 | 설명 |
   |--------|------|
   | Documents | 문서 메타데이터 |
   | Pages | 페이지 정보 |
   | KeyPhrases | 핵심 구문 |

   ![Table Storage](./images/05-09-table-storage.png)

### 5.2 테이블 데이터 조회

1. **테이블 클릭 (예: Documents)**
2. **Storage Browser에서 데이터 확인**

   ![테이블 데이터](./images/05-10-table-data.png)

### 5.3 Blob Storage 확인 (Object 프로젝션)

1. **왼쪽 메뉴 > Data storage > Containers 클릭**
2. **`knowledge-store` 컨테이너 클릭**
3. **저장된 JSON 파일 확인**

   ![Blob Knowledge Store](./images/05-11-blob-knowledge-store.png)

### 5.4 JSON 내용 확인

1. **JSON 파일 클릭**
2. **다운로드 또는 View 클릭**
3. **추출된 데이터 구조 확인**

```json
{
  "metadata_storage_path": "...",
  "metadata_storage_name": "sample.pdf",
  "content": "추출된 전체 텍스트...",
  "pages": [...],
  "tables": [...],
  "keyphrases": ["키워드1", "키워드2", ...],
  "entities": [...]
}
```

   ![JSON 내용](./images/05-12-json-content.png)

---

## 6. 데이터 활용 방법

### 6.1 Power BI 연동

Table Storage의 데이터를 Power BI로 시각화합니다.

1. **Power BI Desktop 열기**
2. **데이터 가져오기 > Azure > Azure Table Storage**
3. **Storage Account 연결**
4. **테이블 선택 및 로드**

   ![Power BI 연동](./images/05-13-power-bi.png)

### 6.2 Python으로 데이터 분석

```python
from azure.data.tables import TableServiceClient
from azure.identity import DefaultAzureCredential

# Table Storage 연결
credential = DefaultAzureCredential()
table_service = TableServiceClient(
    endpoint="https://stdocintellab0115.table.core.windows.net",
    credential=credential
)

# Documents 테이블 쿼리
table_client = table_service.get_table_client("Documents")
entities = table_client.list_entities()

for entity in entities:
    print(entity['metadata_storage_name'])
```

### 6.3 ML 학습 데이터로 활용

Object 프로젝션의 JSON 데이터를 ML 모델 학습에 활용합니다.

| 활용 방법 | 설명 |
|----------|------|
| 문서 분류 | 추출된 텍스트로 분류 모델 학습 |
| 개체명 인식 | 엔터티 데이터로 NER 모델 개선 |
| 요약 생성 | 문서 내용으로 요약 모델 학습 |
| RAG 시스템 | Knowledge Base로 RAG 구축 |

---

## ✅ 체크리스트

Knowledge Store 생성이 완료되었는지 확인하세요:

- [ ] 스킬셋에 Knowledge Store 정의 추가 완료
- [ ] Storage 연결 문자열 설정 완료
- [ ] Table 프로젝션 구성 완료
- [ ] Object 프로젝션 구성 완료
- [ ] 인덱서 리셋 및 재실행 완료
- [ ] Table Storage에 데이터 저장 확인
- [ ] Blob Storage에 JSON 파일 저장 확인

---

## 🔜 다음 단계

Knowledge Store가 생성되면, 다음 튜토리얼에서 AI Search와 Knowledge Store를 활용하여 실제 검색을 수행하는 방법을 학습합니다.

➡️ [06. 인덱싱된 데이터 검색하기](./06-search.md)

---

## 🆘 문제 해결

### Q: Knowledge Store에 데이터가 저장되지 않습니다.
**A:** 다음을 확인하세요:
- 스킬셋 JSON의 `knowledgeStore` 섹션 문법이 올바른지
- Storage 연결 문자열이 정확한지
- AI Search의 Managed Identity에 Storage 쓰기 권한이 있는지

### Q: Table이 생성되지 않습니다.
**A:** `projections.tables` 배열의 `source` 경로가 올바른지 확인하세요. 스킬셋의 출력과 일치해야 합니다.

### Q: "Storage Blob Data Contributor" 권한 오류가 발생합니다.
**A:** Knowledge Store 쓰기를 위해서는 `Storage Blob Data Contributor` 역할이 필요합니다. 02-entra-id-setup.md를 참고하여 역할을 추가하세요.

### Q: JSON 파일이 비어 있습니다.
**A:** Object 프로젝션의 `source` 경로가 올바른지 확인하세요. `/document` 경로에 데이터가 있어야 합니다.

### Q: 인덱서 실행 시 경고가 발생합니다.
**A:** 경고 메시지를 확인하여 원인을 파악하세요. 일반적으로 특정 문서의 특정 필드가 누락된 경우 발생합니다.
