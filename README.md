# seongnam-ai-agent-public

성남시 도시운영 AI 프로젝트의 공개용 모노레포입니다. 비공개 제품 구현에서 외부 공개가 가능한 실행 골격, 더미 화면, 합성 예제와 개발 절차만 분리해 제공합니다.

실제 데이터 수집·적재, Agent 오케스트레이션, 모델 연동·학습·추론 및 운영 설정은 포함하지 않습니다.

## 시작하기

| 모듈 | 공개 내용 |
| --- | --- |
| `backend/` | Java 21 / Spring Boot 최소 실행 골격 |
| `data/` | 외부 시스템과 연결되지 않은 정적 합성 예제 |
| `ml/` | 공개 범위와 실행 경계 문서 |
| `frontend/` | 원본 아이콘과 더미 상호작용을 포함한 도시운영 AI 목업 |
| `tests/` | 합성 예제와 공개 안전 조건 검사 |

## Frontend 실행

```bash
cd frontend
npm install
npm run dev
```

검증 명령은 다음과 같습니다.

```bash
npm run check
npm run build
```

## Backend 검증

```bash
cd backend
./gradlew test bootJar
```

## 공개 예제 검증

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_public_repo.py
```

자세한 공개 경계는 [공개 아키텍처 개요](docs/architecture/public-overview.md), 화면 범위는 [프론트엔드 안내](frontend/README.md)를 확인해 주세요.
