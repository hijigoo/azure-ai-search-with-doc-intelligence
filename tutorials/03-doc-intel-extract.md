# 03. Document Intelligence로 컨텐츠 추출하기

이 문서에서는 Azure Document Intelligence를 사용하여 PDF, 이미지 등 다양한 문서에서 텍스트와 구조 정보를 추출하는 방법을 안내합니다.

## 📋 목차

1. [개요](#1-개요)
2. [테스트 문서 준비](#2-테스트-문서-준비)
3. [Azure Portal에서 Document Intelligence Studio 접속](#3-azure-portal에서-document-intelligence-studio-접속)
4. [Read 모델로 텍스트 추출](#4-read-모델로-텍스트-추출)
5. [Layout 모델로 문서 분석](#5-layout-모델로-문서-분석)
6. [분석 결과 확인](#6-분석-결과-확인)

---

## 1. 개요

### Document Intelligence란?

Azure Document Intelligence(구 Form Recognizer)는 AI 기반 문서 처리 서비스로, 다양한 형식의 문서에서 텍스트, 테이블, 구조 정보를 자동으로 추출합니다.

### 지원하는 문서 형식

| 형식 | 확장자 |
|------|--------|
| PDF | `.pdf` |
| 이미지 | `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff` |
| Office | `.docx`, `.xlsx`, `.pptx` |

### 주요 분석 모델

| 모델 | 용도 | 특징 |
|------|------|------|
| **Read** | OCR 텍스트 추출 | 가장 빠름, 텍스트만 추출 |
| **Layout** | 문서 구조 분석 | 텍스트 + 테이블 + 레이아웃 |
| **Prebuilt-document** | 일반 문서 | 키-값 쌍 추출 |
| **Prebuilt-invoice** | 송장/인보이스 | 특화된 필드 추출 |
| **Prebuilt-receipt** | 영수증 | 영수증 특화 |

---

## 2. 테스트 문서 준비

### 2.1 샘플 문서 다운로드

실습을 위해 샘플 PDF 문서를 준비합니다.

> 💡 **팁**: 본인의 PDF 문서를 사용해도 됩니다.

### 2.2 Blob Storage에 문서 업로드

1. **Azure Portal > Storage Account로 이동**
2. **왼쪽 메뉴 > Data storage > Containers** 클릭
3. **`documents` 컨테이너 클릭**
4. **`Upload` 버튼 클릭**

   ![Blob Upload](./images/03-01-blob-upload.png)

5. **파일 선택 및 업로드**
   - 준비한 PDF 파일 선택
   - `Upload` 클릭

   ![Upload 완료](./images/03-02-blob-upload-complete.png)

---

## 3. Azure Portal에서 Document Intelligence Studio 접속

### 3.1 Document Intelligence 리소스로 이동

1. **Azure Portal에서 Document Intelligence 리소스로 이동**
2. **Overview 페이지에서 `Document Intelligence Studio` 링크 클릭**

   ![Studio 링크](./images/03-03-doc-intel-studio-link.png)

### 3.2 Document Intelligence Studio 접속

1. **Document Intelligence Studio가 새 탭에서 열림**
2. **필요시 Azure 계정으로 로그인**

   ![Studio 메인](./images/03-04-studio-main.png)

### 3.3 리소스 연결 설정

1. **우측 상단의 Settings(⚙️) 클릭**
2. **Resource 탭에서 연결할 리소스 선택**
   - Subscription: 본인 구독 선택
   - Resource group: `rg-doc-intelligence-lab` 선택
   - Resource: 생성한 Document Intelligence 선택

   ![리소스 연결](./images/03-05-studio-resource-connect.png)

3. **Save 클릭**

---

## 4. Read 모델로 텍스트 추출

Read 모델은 순수 OCR 기능으로, 텍스트만 빠르게 추출할 때 가장 적합합니다.

### 4.1 Read 모델 선택

1. **Document Intelligence Studio 메인 화면에서 `Read` 선택**

   ![Read 선택](./images/03-06-studio-read-select.png)

### 4.2 문서 선택 및 분석

1. **`Analyze options` 섹션에서 소스 선택**
   - **Local file**: 로컬 파일 업로드
   - **From URL**: Blob Storage URL 사용
   - **From storage**: Azure Storage 직접 연결

2. **Blob Storage에서 문서 선택**
   - `From storage` 선택
   - Storage Account 연결
   - `documents` 컨테이너에서 파일 선택

3. **`Run analysis` 버튼 클릭**

   ![Read 분석 실행](./images/03-07-studio-read-analysis.png)

### 4.3 Read 결과 확인

1. **Result 탭에서 추출된 텍스트 확인**
2. **원본 문서와 추출 결과 비교**

   | 항목 | 설명 |
   |------|------|
   | content | 추출된 전체 텍스트 |
   | pages | 페이지별 정보 |
   | languages | 감지된 언어 |

   ![Read 결과](./images/03-08-studio-read-result.png)

> 💡 **참고**: Read 모델은 테이블이나 레이아웃 정보를 추출하지 않습니다. 텍스트만 필요한 경우 가장 빠른 옵션입니다.

---

## 5. Layout 모델로 문서 분석

Layout 모델은 문서의 텍스트, 테이블, 체크박스, 구조 정보를 추출하는 데 가장 적합합니다.

### 5.1 Layout 모델 선택

1. **Document Intelligence Studio 메인 화면에서 `Layout` 선택**

   ![Layout 선택](./images/03-09-studio-layout-select.png)

### 5.2 문서 소스 선택

1. **`Analyze options` 섹션에서 소스 선택**
   - **From URL**: Blob Storage URL 사용
   - **From storage**: Azure Storage 직접 연결
   - **Local file**: 로컬 파일 업로드

2. **Blob Storage에서 문서 선택**
   - `From storage` 선택
   - Storage Account 연결
   - `documents` 컨테이너에서 파일 선택

   ![문서 선택](./images/03-10-studio-select-document.png)

### 5.3 분석 실행

1. **`Run analysis` 버튼 클릭**
2. **분석 진행 대기 (보통 몇 초 소요)**

   ![분석 실행](./images/03-11-studio-run-analysis.png)

### 5.4 Read vs Layout 비교

| 비교 | Read | Layout |
|------|------|--------|
| 속도 | 빠름 | 보통 |
| 텍스트 | ✅ | ✅ |
| 테이블 | ❌ | ✅ |
| 레이아웃 | ❌ | ✅ |
| 키-값 쌍 | ❌ | ✅ |

---

## 6. 분석 결과 확인

### 6.1 추출된 텍스트 확인

1. **Result 탭에서 추출된 텍스트 확인**
2. **원본 문서와 추출 결과 비교**

   ![텍스트 결과](./images/03-12-result-text.png)

### 6.2 테이블 추출 결과

1. **Tables 탭 클릭**
2. **문서에서 감지된 테이블 확인**

   | 정보 | 설명 |
   |------|------|
   | Table count | 감지된 테이블 수 |
   | Rows/Columns | 각 테이블의 행/열 수 |
   | Cell content | 셀 내용 |

   ![테이블 결과](./images/03-13-result-tables.png)

### 6.3 레이아웃 구조 확인

1. **Layout 탭에서 문서 구조 확인**
   - 페이지 구분
   - 단락(Paragraph) 정보
   - 섹션 구분

   ![레이아웃 결과](./images/03-14-result-layout.png)

### 6.4 JSON 결과 확인

1. **JSON 탭 클릭**
2. **API 응답 형식의 전체 결과 확인**

```json
{
  "status": "succeeded",
  "analyzeResult": {
    "apiVersion": "2024-02-29-preview",
    "modelId": "prebuilt-layout",
    "content": "추출된 전체 텍스트...",
    "pages": [...],
    "tables": [...],
    "paragraphs": [...]
  }
}
```

   ![JSON 결과](./images/03-15-result-json.png)

---

## ✅ 체크리스트

Document Intelligence 컨텐츠 추출 실습이 완료되었는지 확인하세요:

- [ ] 테스트 문서를 Blob Storage에 업로드 완료
- [ ] Document Intelligence Studio 접속 완료
- [ ] 리소스 연결 설정 완료
- [ ] Read 모델로 텍스트 추출 실행 완료
- [ ] Layout 모델로 문서 분석 실행 완료
- [ ] 추출된 텍스트 결과 확인 완료
- [ ] 테이블 추출 결과 확인 완료
- [ ] JSON 응답 형식 확인 완료

---

## 🔜 다음 단계

Document Intelligence로 문서 분석을 경험했다면, 다음 튜토리얼에서 AI Search와 연동하여 대량의 문서를 자동으로 인덱싱하는 방법을 학습합니다.

➡️ [04. AI Search로 문서 인덱싱하기](./04-indexing.md)

---

## 🆘 문제 해결

### Q: Document Intelligence Studio에 접속할 수 없습니다.
**A:** Azure Portal에서 Document Intelligence 리소스의 Overview 페이지에서 Studio 링크를 클릭하거나, 직접 https://documentintelligence.ai.azure.com 에 접속하세요.

### Q: 리소스 연결 시 Document Intelligence가 보이지 않습니다.
**A:** Settings에서 올바른 Subscription과 Resource group을 선택했는지 확인하세요.

### Q: 분석 결과가 정확하지 않습니다.
**A:** 문서 품질(해상도, 스캔 상태)을 확인하세요. 고해상도 문서일수록 더 정확한 결과를 얻을 수 있습니다.

### Q: 테이블이 제대로 감지되지 않습니다.
**A:** 테이블의 경계선이 명확하지 않은 경우 감지가 어려울 수 있습니다. Layout 모델 대신 Table 모델을 사용해 보세요.

### Q: 한글이 깨져서 나옵니다.
**A:** Document Intelligence는 한글을 지원합니다. 원본 문서가 이미지인 경우 OCR 품질 문제일 수 있습니다. 고해상도 이미지를 사용하세요.
