# 06. 인덱싱된 데이터 검색하기

이 문서에서는 AI Search의 인덱스와 Knowledge Store를 활용하여 다양한 검색 기능을 실습하는 방법을 안내합니다.

## 📋 목차

1. [개요](#1-개요)
2. [Search Explorer로 기본 검색](#2-search-explorer로-기본-검색)
3. [전문 검색 (Full-text Search)](#3-전문-검색-full-text-search)
4. [필터 및 패싯 검색](#4-필터-및-패싯-검색)
5. [시맨틱 검색 (Semantic Search)](#5-시맨틱-검색-semantic-search)
6. [벡터 검색 (Vector Search)](#6-벡터-검색-vector-search)
7. [하이브리드 검색](#7-하이브리드-검색)
8. [검색 결과 활용](#8-검색-결과-활용)

---

## 1. 개요

### AI Search 검색 기능

AI Search는 다양한 검색 기능을 제공하여 사용자의 요구에 맞는 검색 경험을 구현할 수 있습니다.

| 검색 유형 | 설명 | 사용 사례 |
|----------|------|----------|
| **Full-text** | 키워드 기반 전문 검색 | 일반 문서 검색 |
| **Filter** | 조건 기반 필터링 | 날짜, 카테고리 필터 |
| **Facet** | 집계 및 분류 | 검색 결과 분류 |
| **Semantic** | AI 기반 의미 검색 | 자연어 질문 검색 |
| **Vector** | 벡터 유사도 검색 | 의미 기반 유사 문서 검색 |
| **Hybrid** | 전문 + 벡터 결합 | 정확도 향상 |

---

## 2. Search Explorer로 기본 검색

### 2.1 Search Explorer 접속

1. **Azure Portal > AI Search 리소스로 이동**
2. **왼쪽 메뉴에서 `Search explorer` 클릭**

   ![Search Explorer](./images/06-01-search-explorer.png)

### 2.2 인덱스 선택

1. **Index 드롭다운에서 `idx-documents` 선택**
2. **API version 확인** (최신 버전 권장)

   ![인덱스 선택](./images/06-02-index-select.png)

### 2.3 기본 검색 실행

1. **Query string에 검색어 입력**
2. **Search 버튼 클릭**

**모든 문서 검색:**
```
*
```

**특정 키워드 검색:**
```
계약서
```

   ![기본 검색](./images/06-03-basic-search.png)

---

## 3. 전문 검색 (Full-text Search)

### 3.1 단순 쿼리 문법

**View 선택: JSON으로 변경**

```json
{
  "search": "인공지능 머신러닝",
  "searchMode": "any",
  "count": true
}
```

| 파라미터 | 설명 |
|----------|------|
| `search` | 검색 키워드 |
| `searchMode` | `any` (OR) 또는 `all` (AND) |
| `count` | 결과 수 반환 |

   ![전문 검색](./images/06-04-fulltext-search.png)

### 3.2 Lucene 쿼리 문법

고급 검색을 위한 Lucene 쿼리 문법을 사용합니다.

```json
{
  "search": "content:\"인공지능\" AND content:머신러닝",
  "queryType": "full",
  "searchMode": "all",
  "count": true
}
```

| 연산자 | 설명 | 예시 |
|--------|------|------|
| `AND` | 모두 포함 | `AI AND 머신러닝` |
| `OR` | 하나 이상 포함 | `AI OR 딥러닝` |
| `NOT` | 제외 | `AI NOT 딥러닝` |
| `"..."` | 구문 검색 | `"인공지능 기술"` |
| `*` | 와일드카드 | `인공*` |
| `~` | 퍼지 검색 | `인공지능~1` |

   ![Lucene 쿼리](./images/06-05-lucene-query.png)

### 3.3 결과 필드 선택

특정 필드만 반환받습니다.

```json
{
  "search": "계약",
  "select": "metadata_storage_name, content, keyphrases",
  "count": true,
  "top": 5
}
```

| 파라미터 | 설명 |
|----------|------|
| `select` | 반환할 필드 (쉼표 구분) |
| `top` | 반환할 결과 수 |
| `skip` | 건너뛸 결과 수 (페이징) |

   ![필드 선택](./images/06-06-select-fields.png)

---

## 4. 필터 및 패싯 검색

### 4.1 필터 검색

조건에 맞는 문서만 검색합니다.

```json
{
  "search": "*",
  "filter": "metadata_content_type eq 'application/pdf'",
  "count": true
}
```

| 연산자 | 설명 | 예시 |
|--------|------|------|
| `eq` | 같음 | `type eq 'pdf'` |
| `ne` | 같지 않음 | `type ne 'pdf'` |
| `gt` / `lt` | 크다/작다 | `size gt 1000` |
| `ge` / `le` | 크거나 같다/작거나 같다 | `size ge 1000` |
| `and` / `or` | 논리 연산 | `type eq 'pdf' and size gt 1000` |

   ![필터 검색](./images/06-07-filter-search.png)

### 4.2 패싯 검색

필드별 집계를 수행합니다.

```json
{
  "search": "*",
  "facets": ["metadata_content_type", "keyphrases,count:10"],
  "count": true
}
```

**결과 예시:**
```json
{
  "@search.facets": {
    "metadata_content_type": [
      { "value": "application/pdf", "count": 5 },
      { "value": "image/png", "count": 3 }
    ],
    "keyphrases": [
      { "value": "인공지능", "count": 4 },
      { "value": "머신러닝", "count": 3 }
    ]
  }
}
```

   ![패싯 검색](./images/06-08-facet-search.png)

---

## 5. 시맨틱 검색 (Semantic Search)

시맨틱 검색은 AI 모델을 사용하여 검색어의 의미를 이해하고 관련성 높은 결과를 반환합니다.

### 5.1 시맨틱 구성 확인

1. **AI Search > Settings > Semantic configurations 메뉴**
2. **기존 구성 확인 또는 새 구성 생성**

   ![시맨틱 구성](./images/06-09-semantic-config.png)

### 5.2 시맨틱 구성 생성

1. **`+ Add` 클릭**
2. **다음 설정 입력**:

   | 필드 | 값 |
   |------|-----|
   | Name | `semantic-config` |
   | Title field | `metadata_storage_name` |
   | Content fields | `content` |
   | Keyword fields | `keyphrases` |

   ![시맨틱 구성 생성](./images/06-10-semantic-config-create.png)

### 5.3 시맨틱 검색 실행

```json
{
  "search": "문서에서 중요한 정보를 어떻게 추출하나요?",
  "queryType": "semantic",
  "semanticConfiguration": "semantic-config",
  "captions": "extractive",
  "answers": "extractive",
  "count": true
}
```

| 파라미터 | 설명 |
|----------|------|
| `queryType` | `semantic` 지정 |
| `semanticConfiguration` | 시맨틱 구성 이름 |
| `captions` | 관련 문장 추출 |
| `answers` | 직접 답변 추출 |

   ![시맨틱 검색](./images/06-11-semantic-search.png)

### 5.4 시맨틱 검색 결과

```json
{
  "@search.answers": [
    {
      "text": "Document Intelligence를 사용하여 PDF에서 텍스트를 추출합니다...",
      "highlights": "...<em>Document Intelligence</em>를 사용하여...",
      "score": 0.95
    }
  ],
  "value": [
    {
      "@search.captions": [
        {
          "text": "문서 분석을 위해 Layout 모델을 사용합니다.",
          "highlights": "..."
        }
      ]
    }
  ]
}
```

   ![시맨틱 결과](./images/06-12-semantic-result.png)

---

## 6. 벡터 검색 (Vector Search)

벡터 검색은 텍스트를 벡터로 변환하여 의미적으로 유사한 문서를 찾습니다.

### 6.1 벡터 검색 요구사항

| 요구사항 | 설명 |
|----------|------|
| 벡터 필드 | 인덱스에 벡터 필드 정의 필요 |
| 임베딩 모델 | text-embedding-3-large 등 |
| 벡터 프로필 | 벡터 검색 알고리즘 구성 |

### 6.2 벡터 인덱스 구성 확인

1. **AI Search > Indexes > `idx-documents`**
2. **Fields에서 벡터 필드 확인**

   ![벡터 필드 확인](./images/06-13-vector-field-check.png)

### 6.3 벡터 검색 실행

> ⚠️ **참고**: 벡터 검색은 쿼리 텍스트를 먼저 임베딩으로 변환해야 합니다.

```json
{
  "search": "",
  "vectorQueries": [
    {
      "kind": "text",
      "text": "인공지능을 활용한 문서 처리 방법",
      "fields": "content_vector",
      "k": 5
    }
  ],
  "count": true
}
```

| 파라미터 | 설명 |
|----------|------|
| `vectorQueries` | 벡터 쿼리 배열 |
| `kind` | `text` 또는 `vector` |
| `text` | 검색할 텍스트 (자동 임베딩) |
| `fields` | 벡터 필드 이름 |
| `k` | 반환할 결과 수 |

   ![벡터 검색](./images/06-14-vector-search.png)

---

## 7. 하이브리드 검색

전문 검색과 벡터 검색을 결합하여 더 정확한 결과를 얻습니다.

### 7.1 하이브리드 검색 실행

```json
{
  "search": "문서 분석",
  "vectorQueries": [
    {
      "kind": "text",
      "text": "문서 분석",
      "fields": "content_vector",
      "k": 5
    }
  ],
  "select": "metadata_storage_name, content",
  "count": true
}
```

   ![하이브리드 검색](./images/06-15-hybrid-search.png)

### 7.2 하이브리드 + 시맨틱 검색

```json
{
  "search": "효율적인 문서 관리 방법은?",
  "vectorQueries": [
    {
      "kind": "text",
      "text": "효율적인 문서 관리 방법은?",
      "fields": "content_vector",
      "k": 5
    }
  ],
  "queryType": "semantic",
  "semanticConfiguration": "semantic-config",
  "captions": "extractive",
  "answers": "extractive",
  "count": true
}
```

   ![하이브리드 시맨틱](./images/06-16-hybrid-semantic.png)

---

## 8. 검색 결과 활용

### 8.1 검색 API 엔드포인트

애플리케이션에서 검색 API를 호출합니다.

**엔드포인트:**
```
POST https://{search-service-name}.search.windows.net/indexes/{index-name}/docs/search?api-version=2024-07-01
```

**헤더:**
```
Content-Type: application/json
Authorization: Bearer {access-token}
```

### 8.2 Python SDK 예제

```python
from azure.search.documents import SearchClient
from azure.identity import DefaultAzureCredential

# 클라이언트 생성
credential = DefaultAzureCredential()
client = SearchClient(
    endpoint="https://search-doc-lab-0115.search.windows.net",
    index_name="idx-documents",
    credential=credential
)

# 검색 실행
results = client.search(
    search_text="인공지능",
    select=["metadata_storage_name", "content"],
    top=5
)

for result in results:
    print(f"파일: {result['metadata_storage_name']}")
    print(f"내용: {result['content'][:200]}...")
    print("---")
```

### 8.3 RAG (Retrieval Augmented Generation) 활용

검색 결과를 GPT-4o와 결합하여 질문에 답변합니다.

```python
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

# 검색 실행
search_client = SearchClient(
    endpoint="https://search-doc-lab-0115.search.windows.net",
    index_name="idx-documents",
    credential=credential
)

query = "문서에서 테이블을 추출하는 방법은?"
search_results = search_client.search(search_text=query, top=3)

# 컨텍스트 구성
context = "\n".join([r["content"][:1000] for r in search_results])

# GPT-4o로 답변 생성
openai_client = AzureOpenAI(
    azure_endpoint="https://ms-foundry-lab-0115.openai.azure.com",
    azure_ad_token_provider=credential.get_token,
    api_version="2024-02-15-preview"
)

response = openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": f"다음 문서 내용을 바탕으로 질문에 답변하세요:\n{context}"},
        {"role": "user", "content": query}
    ]
)

print(response.choices[0].message.content)
```

   ![RAG 활용](./images/06-17-rag-usage.png)

---

## ✅ 체크리스트

검색 기능 실습이 완료되었는지 확인하세요:

- [ ] Search Explorer 접속 완료
- [ ] 기본 검색 테스트 완료
- [ ] 전문 검색 (Full-text) 실행 완료
- [ ] Lucene 쿼리 문법 테스트 완료
- [ ] 필터 검색 실행 완료
- [ ] 패싯 검색 실행 완료
- [ ] 시맨틱 검색 구성 및 실행 완료
- [ ] 벡터 검색 테스트 완료 (벡터 필드 구성된 경우)
- [ ] 하이브리드 검색 테스트 완료

---

## 🎉 튜토리얼 완료

축하합니다! Azure AI Search와 Document Intelligence를 활용한 문서 처리 및 검색 시스템 구축을 완료했습니다.

### 학습한 내용 요약

| 튜토리얼 | 내용 |
|----------|------|
| 01-setup | Azure 리소스 생성 |
| 02-entra-id-setup | Entra ID 기반 보안 연동 |
| 03-doc-intel-extract | Document Intelligence로 문서 분석 |
| 04-indexing | AI Search 인덱싱 파이프라인 |
| 05-knowledge-store | Knowledge Store 생성 및 활용 |
| 06-search | 다양한 검색 기능 실습 |

### 다음 학습 추천

- [Azure AI Search 공식 문서](https://learn.microsoft.com/azure/search/)
- [Document Intelligence 공식 문서](https://learn.microsoft.com/azure/ai-services/document-intelligence/)
- [RAG 패턴 구현 가이드](https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview)

---

## 🆘 문제 해결

### Q: 시맨틱 검색이 작동하지 않습니다.
**A:** 시맨틱 검색은 Basic 이상 SKU에서만 사용 가능합니다. Free tier에서는 지원되지 않습니다.

### Q: 벡터 검색 결과가 없습니다.
**A:** 인덱스에 벡터 필드가 정의되어 있고, 인덱싱 시 벡터가 생성되었는지 확인하세요.

### Q: 검색 결과가 예상과 다릅니다.
**A:** `searchMode`, `queryType`, 필터 조건을 확인하세요. Lucene 쿼리 문법이 올바른지도 확인하세요.

### Q: API 호출 시 인증 오류가 발생합니다.
**A:** Managed Identity 또는 API Key 인증이 올바르게 설정되어 있는지 확인하세요.

### Q: 검색 속도가 느립니다.
**A:** 인덱스 크기, 쿼리 복잡도, SKU를 확인하세요. 필요시 파티션/레플리카를 조정하세요.
