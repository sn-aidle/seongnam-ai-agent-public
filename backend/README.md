# Backend 공개 골격

Java 21과 Spring Boot로 구성된 최소 실행 골격입니다. 애플리케이션 시작과 빌드 가능 여부만 공개합니다.

다음 항목은 공개 저장소에 포함하지 않습니다.

- Agent 오케스트레이션과 의사결정 흐름
- 모델 Provider 및 외부 서비스 연동
- 실제 데이터 조회와 저장소 구현
- 내부 API 계약, DB schema와 운영 설정

```bash
./gradlew test bootJar
```
