# 02. Microsoft Entra ID 기반 리소스 연동 설정

이 문서에서는 Key 기반 인증 대신 **Microsoft Entra ID (구 Azure AD)** 기반의 역할 기반 접근 제어(RBAC)를 사용하여 Azure 리소스 간 보안 연동을 설정하는 방법을 안내합니다.

## 📋 목차

1. [개요](#1-개요)
2. [AI Search Managed Identity 활성화](#2-ai-search-managed-identity-활성화)
3. [Storage Account에 역할 할당](#3-storage-account에-역할-할당)
4. [Document Intelligence에 역할 할당](#4-document-intelligence에-역할-할당)
5. [엔드포인트 정보 확인](#5-엔드포인트-정보-확인)
6. [역할 할당 확인](#6-역할-할당-확인)

---

## 1. 개요

> 🔐 **보안 권장사항**: Entra ID 기반 인증은 키 유출 위험이 없고, 세밀한 권한 제어가 가능하며, 감사 로그를 통한 추적이 용이합니다.

### Key 기반 vs Entra ID 기반 인증 비교

| 항목 | Key 기반 | Entra ID 기반 |
|------|----------|---------------|
| 보안성 | 키 유출 위험 있음 | 키 없이 안전한 연동 |
| 권한 관리 | 전체 접근 또는 차단 | 세밀한 역할 기반 제어 |
| 감사 | 제한적 | 상세한 감사 로그 |
| 키 회전 | 수동 관리 필요 | 자동 관리 |

### 설정할 역할 요약

| 리소스 | 할당할 역할 | 대상 |
|--------|------------|------|
| Storage Account | Storage Blob Data Reader | AI Search |
| Document Intelligence | Cognitive Services User | AI Search |

---

## 2. AI Search Managed Identity 활성화

AI Search가 다른 Azure 리소스에 안전하게 접근할 수 있도록 System Managed Identity를 활성화합니다.

### 단계별 가이드

1. **AI Search 리소스로 이동**
   - Azure Portal에서 앞서 생성한 AI Search 서비스로 이동

2. **Identity 메뉴 이동**
   - 왼쪽 메뉴에서 `Settings` > `Identity` 클릭

3. **System assigned Identity 활성화**
   - `System assigned` 탭 선택
   - Status를 `On`으로 변경

4. **Save 클릭**

   ![AI Search Identity 설정](./images/02-01-ai-search-identity.png)

5. **Object ID 메모** (역할 할당 시 사용)

   > 💡 **참고**: Save 후 Object ID가 생성됩니다. 이 ID가 AI Search의 고유 식별자입니다.

   ![AI Search Object ID](./images/02-02-ai-search-object-id.png)

---

## 3. Storage Account에 역할 할당

AI Search가 Blob Storage의 문서를 읽을 수 있도록 역할을 할당합니다.

### 단계별 가이드

1. **Storage Account로 이동**
   - Azure Portal에서 앞서 생성한 Storage Account로 이동

2. **Access Control (IAM) 메뉴 이동**
   - 왼쪽 메뉴에서 `Access Control (IAM)` 클릭

3. **역할 할당 추가**
   - `+ Add` > `Add role assignment` 클릭

   ![Storage IAM 추가](./images/02-03-storage-iam-add.png)

4. **Role 탭에서 역할 선택**
   - 검색창에 "Storage Blob Data Reader" 입력
   - `Storage Blob Data Reader` 선택
   - `Next` 클릭

   | 역할 | 권한 |
   |------|------|
   | Storage Blob Data Reader | Blob 데이터 읽기 전용 |
   | Storage Blob Data Contributor | Blob 데이터 읽기/쓰기 |

   ![Storage 역할 선택](./images/02-04-storage-role-select.png)

5. **Members 탭에서 멤버 추가**
   - `Assign access to`: **Managed identity** 선택
   - `+ Select members` 클릭
   - `Managed identity` 드롭다운에서 **Search service** 선택
   - 앞서 생성한 AI Search 서비스 선택
   - `Select` 클릭

   ![Storage 멤버 선택](./images/02-05-storage-member-select.png)

6. **Review + assign 클릭하여 역할 할당 완료**

   ![Storage 역할 할당 완료](./images/02-06-storage-role-assigned.png)

---

## 4. Document Intelligence에 역할 할당

AI Search가 Document Intelligence를 사용할 수 있도록 역할을 할당합니다.

### 단계별 가이드

1. **Document Intelligence 리소스로 이동**
   - Azure Portal에서 앞서 생성한 Document Intelligence로 이동

2. **Access Control (IAM) 메뉴 이동**
   - 왼쪽 메뉴에서 `Access Control (IAM)` 클릭

3. **역할 할당 추가**
   - `+ Add` > `Add role assignment` 클릭

4. **Role 탭에서 역할 선택**
   - 검색창에 "Cognitive Services User" 입력
   - `Cognitive Services User` 선택
   - `Next` 클릭

   | 역할 | 권한 |
   |------|------|
   | Cognitive Services User | API 호출 권한 |
   | Cognitive Services Contributor | 리소스 관리 + API 호출 |

   ![Document Intelligence 역할 선택](./images/02-07-doc-intel-role-select.png)

5. **Members 탭에서 멤버 추가**
   - `Assign access to`: **Managed identity** 선택
   - `+ Select members` 클릭
   - `Managed identity` 드롭다운에서 **Search service** 선택
   - 앞서 생성한 AI Search 서비스 선택
   - `Select` 클릭

   ![Document Intelligence 멤버 선택](./images/02-08-doc-intel-member-select.png)

6. **Review + assign 클릭하여 역할 할당 완료**

---

## 5. 엔드포인트 정보 확인

Entra ID 인증에서는 키 대신 엔드포인트 URL만 필요합니다.

### 5.1 Storage Account

1. **Storage Account > Overview**에서 확인
2. **다음 정보 메모**

   | 항목 | 예시 |
   |------|------|
   | Blob service endpoint | `https://stdocintellab0115.blob.core.windows.net/` |

### 5.2 Document Intelligence

1. **Document Intelligence > Overview**에서 확인
2. **다음 정보 메모**

   | 항목 | 예시 |
   |------|------|
   | Endpoint | `https://doc-intel-lab-0115.cognitiveservices.azure.com/` |

### 5.3 AI Search

1. **AI Search > Overview**에서 확인
2. **다음 정보 메모**

   | 항목 | 예시 |
   |------|------|
   | URL | `https://search-doc-lab-0115.search.windows.net` |

   ![엔드포인트 확인](./images/02-09-endpoints-overview.png)

---

## 6. 역할 할당 확인

각 리소스에서 역할이 올바르게 할당되었는지 확인합니다.

### 확인 방법

1. **각 리소스의 Access Control (IAM) > Role assignments 탭** 클릭
2. **AI Search의 Managed Identity가 목록에 있는지 확인**

   ![역할 할당 확인](./images/02-10-role-assignments-check.png)

### 역할 할당 요약

| 리소스 | 할당된 역할 | 대상 |
|--------|------------|------|
| Storage Account | Storage Blob Data Reader | AI Search |
| Document Intelligence | Cognitive Services User | AI Search |

> ⏱️ **참고**: 역할 할당이 적용되기까지 최대 5분 정도 소요될 수 있습니다.

---

## ✅ 체크리스트

Entra ID 설정이 완료되었는지 확인하세요:

- [ ] AI Search Managed Identity 활성화 완료
- [ ] Storage Account에 Storage Blob Data Reader 역할 할당 완료
- [ ] Document Intelligence에 Cognitive Services User 역할 할당 완료
- [ ] 각 서비스의 엔드포인트 확인 완료
- [ ] 역할 할당 목록에서 AI Search 확인 완료

---

## 🔜 다음 단계

Entra ID 기반 리소스 연동 설정이 완료되면 다음 튜토리얼에서 실제 문서를 업로드하고 처리하는 방법을 학습합니다.

➡️ [03. 문서 업로드 및 인덱싱](./03-document-indexing.md)

---

## 🆘 문제 해결

### Q: Managed Identity를 찾을 수 없습니다.
**A:** AI Search의 Identity 설정에서 System assigned가 `On`으로 설정되어 있는지 확인하세요. Save 후 몇 초 기다려야 합니다.

### Q: 역할 할당 후에도 접근이 안 됩니다.
**A:** 역할 할당이 적용되기까지 최대 5분이 소요될 수 있습니다. 잠시 기다린 후 다시 시도하세요.

### Q: "Storage Blob Data Reader" 역할이 검색되지 않습니다.
**A:** Role 탭에서 "Job function roles" 카테고리에서 검색하세요. 또는 전체 역할 목록에서 스크롤하여 찾을 수 있습니다.

### Q: 구독에 대한 권한이 없다고 나옵니다.
**A:** 역할 할당을 위해서는 해당 리소스에 대한 Owner 또는 User Access Administrator 권한이 필요합니다. 관리자에게 문의하세요.
