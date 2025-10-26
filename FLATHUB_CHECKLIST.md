# Flathub Submission Checklist

이 체크리스트는 SimpleShot이 Flathub 요구사항을 준수하는지 확인합니다.

## ✅ Application ID

- [x] ID는 reverse-DNS 형식: `net.bloupla.simpleshot`
- [x] 3개의 컴포넌트 (net.bloupla.simpleshot)
- [x] 도메인 제어 필요: `bloupla.net` (확인 필요)
- [x] 모든 메타데이터 파일에서 ID가 일치함

## ✅ Required Files

### Manifest
- [x] `net.bloupla.simpleshot.yml` 존재 (Flathub 제출용)
- [x] `net.bloupla.simpleshot.local.yml` 존재 (로컬 개발용)
- [x] GitHub에서 소스 다운로드하도록 설정됨
- [x] Runtime은 Flathub에서 호스팅됨 (org.gnome.Platform//49)
- [x] 최신 런타임 버전 사용 (GNOME 49)

### Metadata (업스트림 프로젝트에 통합)
- [x] `net.bloupla.simpleshot.metainfo.xml` 존재
- [x] MetaInfo 파일이 유효함
- [x] 라이선스 명시 (MIT)
- [x] 설명 포함
- [x] 릴리즈 정보 포함
- [x] URL들이 GitHub 저장소로 업데이트됨
  - Homepage: https://github.com/llaa33219/SimpleShot
  - Bugtracker: https://github.com/llaa33219/SimpleShot/issues
  - VCS: https://github.com/llaa33219/SimpleShot
  - Contribute: https://github.com/llaa33219/SimpleShot/blob/main/CONTRIBUTING.md

### Desktop File
- [x] `net.bloupla.simpleshot.desktop` 존재
- [x] 적절한 카테고리 (Graphics, Utility)
- [x] 아이콘 지정

### Icon
- [x] SVG 아이콘 제공 (`icons/net.bloupla.simpleshot.svg`)
- [x] 아이콘 이름이 App ID와 일치

### Other Files
- [x] `LICENSE` 파일 존재 (MIT)
- [x] `README.md` 존재
- [x] `flathub.json` 존재 (아키텍처 명시)

## ✅ Permissions (finish-args)

- [x] Wayland 지원 (`--socket=wayland`)
- [x] X11 fallback (`--socket=fallback-x11`)
- [x] GPU 가속 (`--device=dri`)
- [x] Portal 사용 (`--talk-name=org.freedesktop.portal.Desktop`)
- [x] 최소 파일시스템 접근 (`xdg-pictures:create`, `xdg-videos:create`)
- [x] 네트워크 접근 없음 ✓ (보안 우수)

## ✅ Sandboxing

- [x] XDG Portal 사용 (스크린샷/녹화)
- [x] 샌드박스 친화적 구현
- [x] 과도한 권한 요청 없음
- [x] 외부 도구 의존성 최소화

## ✅ Build Requirements

- [x] 네트워크 접근 없이 빌드 가능
- [x] 모든 의존성이 manifest에 명시됨
- [x] 바이너리 파일 미포함 (소스만 포함)

## ✅ Inclusion Policy

- [x] 기능적인 애플리케이션 (스크린샷 & 녹화)
- [x] 그래픽 데스크톱 애플리케이션
- [x] 최소 기능 이상 제공
- [x] 적절한 사용자 경험
- [x] Linux 데스크톱에 적합

## ⚠️ 제출 전 확인 사항

### GitHub 저장소
- [ ] 저장소 생성: https://github.com/llaa33219/SimpleShot/
- [ ] 저장소가 public임
- [ ] 다음 파일들이 업로드됨:
  - [ ] `simpleshot.py`
  - [ ] `net.bloupla.simpleshot.desktop`
  - [ ] `net.bloupla.simpleshot.metainfo.xml`
  - [ ] `icons/net.bloupla.simpleshot.svg`
  - [ ] `LICENSE`
  - [ ] `README.md` 및 기타 문서
- [ ] 릴리즈 태그 생성: `v1.0.0`
- [ ] Commit hash 확인 및 manifest에 업데이트

### 도메인 검증
- [ ] `bloupla.net` 도메인 소유권 확인
- [ ] HTTPS 접근 가능한지 확인
- [ ] Flathub 검증 토큰 배치 준비
  - `https://bloupla.net/.well-known/org.flathub.VerifiedApps.txt`

### 기능 테스트
- [ ] Wayland에서 스크린샷 동작 확인
- [ ] X11에서 스크린샷 동작 확인
- [ ] Wayland에서 녹화 동작 확인
- [ ] X11에서 녹화 동작 확인
- [ ] 클립보드 복사 동작 확인
- [ ] 설정 저장 동작 확인

### 메타데이터 검증
```bash
# AppStream 검증
appstreamcli validate net.bloupla.simpleshot.metainfo.xml

# Desktop 파일 검증
desktop-file-validate net.bloupla.simpleshot.desktop
```

### 빌드 테스트
```bash
# 깨끗한 빌드 테스트
./build.sh

# 실행 테스트
flatpak run net.bloupla.simpleshot
```

## 📝 제출 프로세스

1. GitHub에 저장소 생성 (public)
2. 도메인 검증 또는 코드 호스팅 ID 사용
3. Flathub GitHub에서 새 앱 제출
4. 리뷰어 피드백 대응
5. 승인 후 Flathub에 게시

## 🔍 개선 가능 영역

### 우선순위 높음
- [ ] 전체 XDG Portal 구현 (fallback 제거)
- [ ] 더 나은 오류 처리
- [ ] 스크린샷 미리보기

### 우선순위 중간
- [ ] 주석 도구 (화살표, 텍스트)
- [ ] 지연 캡처 옵션
- [ ] 다중 모니터 개선

## 📚 참고 문서

- [Flathub Requirements](https://docs.flathub.org/docs/for-app-authors/requirements)
- [Flathub Submission](https://docs.flathub.org/docs/for-app-authors/submission)
- [MetaInfo Guidelines](https://docs.flathub.org/docs/for-app-authors/metainfo-guidelines)
- [App Verification](https://docs.flathub.org/docs/for-app-authors/verification)

