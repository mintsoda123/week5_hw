# PRD (Product Requirements Document)
# Week 5 딥러닝 학습 플랫폼

---

## 1. 제품 개요

**제품명:** Week 5 딥러닝 핵심 개념 학습 플랫폼  
**버전:** 1.0.0  
**작성일:** 2026-04-14  

### 목적
딥러닝 5주차 핵심 개념(Regularization, Overfitting/Underfitting, Data Augmentation, Transfer Learning, CNN)을 인터랙티브하게 학습할 수 있는 웹 플랫폼. Google OAuth 로그인과 Freemium 모델(5회 무료 → 유료 전환)을 통해 수익화합니다.

---

## 2. 사용자 여정

### 비로그인 사용자
- 홈페이지에서 컨텐츠 목록 및 미리보기 확인
- 로그인 없이는 컨텐츠 접근 불가

### 로그인 사용자 (무료)
- Google 계정으로 1-클릭 로그인
- 컨텐츠 섹션 5회까지 무료 열람
- 사용 횟수 UI에서 실시간 확인

### 유료 사용자
- 5회 초과 시 결제 팝업 표시
- Polar.sh를 통해 결제 완료 후 무제한 접근

---

## 3. 핵심 기능 (Feature Requirements)

### FR-001: Google OAuth 로그인
- Gmail 계정으로 로그인/회원가입 통합
- 로그인 상태 유지 (JWT 토큰, 7일)
- 로그아웃 기능

### FR-002: 컨텐츠 표시
5개 학습 섹션을 카드 형태로 표시:
1. Regularization (L1/L2, Dropout, Batch Normalization)
2. Overfitting vs Underfitting
3. Data Augmentation
4. Transfer Learning
5. MNIST CNN 실습

각 섹션: 개념 설명, 코드 예시, 결과 해석 포함

### FR-003: 사용량 추적 (Freemium)
- 섹션 1회 열람 = 사용 1회 차감
- 무료 한도: 5회
- 초과 시 결제 유도 모달 표시
- 이미 열람한 섹션 재방문 시 추가 차감 없음 (옵션)

### FR-004: 결제 (Polar.sh)
- 유료 플랜: 월간 or 일회성 구매
- Polar.sh Checkout 링크로 결제
- 결제 완료 후 Webhook으로 프리미엄 상태 업데이트
- 프리미엄 사용자: 무제한 접근

### FR-005: 반응형 UI
- 모바일/태블릿/데스크탑 모두 지원
- Tailwind CSS로 깔끔한 디자인

---

## 4. 비기능 요구사항

| 항목 | 요구사항 |
|------|---------|
| 성능 | 페이지 로드 3초 이내 |
| 보안 | HTTPS, JWT 인증, CORS 설정 |
| 가용성 | 99% 이상 (Vercel/Railway 기준) |
| 확장성 | 사용자 1,000명 이내 (초기) |

---

## 5. 성공 지표
- 가입 전환율: 방문자 중 로그인 비율 > 30%
- 결제 전환율: 무료 사용자 중 유료 전환 > 5%
- 5회 컨텐츠 완료율 > 60%

---

## 6. 범위 외 (Out of Scope v1.0)
- 소셜 공유 기능
- 퀴즈/평가 기능
- 다국어 지원
- 관리자 대시보드
