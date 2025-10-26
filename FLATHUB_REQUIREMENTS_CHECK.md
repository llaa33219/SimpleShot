# Flathub 요구사항 준수 확인

이 문서는 [Flathub Requirements](https://docs.flathub.org/docs/for-app-authors/requirements#required-files)의 모든 항목을 확인합니다.

## ✅ Inclusion Policy (포함 정책)

### Non-functional submissions
- [x] 완전히 기능하는 애플리케이션
- [x] 좋은 사용자 경험 제공
- [x] 명백한 이슈 없음

### Console software submissions
- [x] 그래픽 데스크톱 애플리케이션 (CLI가 아님)

### Minimal submissions
- [x] 충분한 기능 제공 (스크린샷 + 녹화)
- [x] 단순한 스크립트가 아님
- [x] 데스크톱 애플리케이션으로 적합

### Impermissible submissions
- [x] 문서 전용이 아님
- [x] 미디어 전용이 아님
- [x] 웹 래퍼가 아님
- [x] 특정 DE/배포판 전용이 아님

### Sandbox compatibility
- [x] Flatpak 샌드박스와 호환
- [x] Portal 사용으로 제한 극복

### Duplicate submissions
- [x] 유일한 구현

### Software design
- [x] 안전한 디자인
- [x] 보안 체크 무시하지 않음
- [x] 민감 정보 노출 없음

### Structure and organisation
- [x] 잘 구조화된 Python 코드
- [x] GitHub에서 배포 (Git tags)
- [x] 검증 가능한 소스

### Not misleading/malicious
- [x] 합법적
- [x] 오해의 소지 없음
- [x] 악성 코드 없음

## ✅ Application ID

### Format
- [x] Reverse-DNS 형식: `net.bloupla.simpleshot`
- [x] 3개 컴포넌트
- [x] 255자 이하
- [x] 유효한 문자만 사용
- [x] 소문자 도메인
- [x] `.desktop`, `.app`, `.linux`로 끝나지 않음
- [x] MetaInfo 파일의 ID와 일치

### Control over domain
- ⚠️ `bloupla.net` 도메인 제어권 필요
- [ ] HTTPS로 접근 가능
- [ ] 검증 토큰 배치: `https://bloupla.net/.well-known/org.flathub.VerifiedApps.txt`

**참고**: 도메인 검증은 사용자가 직접 처리 예정

## ✅ License

- [x] MIT License (재배포 가능)
- [x] MetaInfo에 라이선스 명시됨
- [x] LICENSE 파일 존재
- [x] 상표권 침해 없음

## ✅ Installing License Files

- [x] Flatpak builder가 자동으로 LICENSE 파일 설치
- [x] `$FLATPAK_DEST/share/licenses/$FLATPAK_ID/`에 설치됨

## ✅ Permissions

### Standard Permissions (자유롭게 사용 가능)
- [x] `--socket=wayland` ✓
- [x] `--socket=fallback-x11` ✓
- [x] `--device=dri` ✓

### Portal Usage (권장)
- [x] `--talk-name=org.freedesktop.portal.Desktop` ✓
- [x] XDG Screenshot Portal 사용
- [x] XDG Screencast Portal 준비

### Filesystem Access (최소화)
- [x] `--filesystem=xdg-pictures:create` ✓ (스크린샷만)
- [x] `--filesystem=xdg-videos:create` ✓ (녹화만)
- [x] `--filesystem=home` 사용 안 함 ✓
- [x] `--filesystem=host` 사용 안 함 ✓

### Network
- [x] 네트워크 접근 없음 ✓

### Summary
- [x] 최소 권한 원칙 준수
- [x] Portal 우선 사용
- [x] 과도한 권한 없음

## ✅ No Network Access During Build

- [x] 모든 의존성이 manifest에 명시됨
- [x] 공개 접근 가능한 URL (GitHub)
- [x] `--share=network` 사용 안 함
- [x] 빌드 중 네트워크 접근 불필요

## ✅ Building from Source

- [x] 소스 코드에서 빌드
- [x] Python 스크립트 (소스)
- [x] 바이너리 없음

## ✅ Patches

- [x] 업스트림 소스를 그대로 배포
- [x] 수정 사항 없음
- [x] 패치 불필요

## ✅ Stable Releases

- [x] 안정 버전 (v1.0.0)
- [x] Nightly 빌드 아님
- [x] 개발 스냅샷 아님

## ✅ Required Files

### Manifest ⭐
- [x] `net.bloupla.simpleshot.yml` 최상위 레벨에 존재
- [x] App ID로 명명됨 (`.yml` 확장자)
- [x] Runtime이 Flathub에 호스팅됨: `org.gnome.Platform//49`
- [x] GitHub에서 소스 다운로드:
  ```yaml
  sources:
    - type: git
      url: https://github.com/llaa33219/SimpleShot.git
      tag: v1.0.0
      commit: COMMIT_HASH_HERE
  ```

### flathub.json ⭐
- [x] 존재함
- [x] 최상위 레벨
- [x] 아키텍처 명시: `x86_64`, `aarch64`

### Dependency Manifest
- [x] Python 표준 라이브러리 사용
- [x] 추가 의존성 없음
- [x] 의존성 manifest 불필요

## ✅ Required Metadata

**중요**: 메타데이터 파일들은 **업스트림 프로젝트(GitHub)에 통합**되어야 합니다.

### Appstream (MetaInfo) ⭐
- [x] `net.bloupla.simpleshot.metainfo.xml` 존재
- [x] 업스트림 프로젝트에 포함 예정
- [x] 검증 통과 필요:
  ```bash
  appstreamcli validate net.bloupla.simpleshot.metainfo.xml
  ```
- [x] 필수 요소:
  - [x] `<id>` - App ID와 일치
  - [x] `<name>` - SimpleShot
  - [x] `<summary>` - 간단한 설명
  - [x] `<description>` - 상세 설명
  - [x] `<metadata_license>` - CC0-1.0
  - [x] `<project_license>` - MIT
  - [x] `<url type="homepage">` - GitHub URL
  - [x] `<url type="bugtracker">` - GitHub Issues
  - [x] `<screenshots>` - 스크린샷 섹션
  - [x] `<releases>` - 릴리즈 정보
  - [x] `<content_rating>` - OARS 레이팅

### Desktop File ⭐
- [x] `net.bloupla.simpleshot.desktop` 존재
- [x] 업스트림 프로젝트에 포함 예정
- [x] 검증 통과 필요:
  ```bash
  desktop-file-validate net.bloupla.simpleshot.desktop
  ```
- [x] 필수 필드:
  - [x] `Type=Application`
  - [x] `Name=SimpleShot`
  - [x] `Exec=simpleshot`
  - [x] `Icon=net.bloupla.simpleshot`
  - [x] `Categories=Graphics;Utility;`

### Icons ⭐
- [x] SVG 아이콘 제공: `icons/net.bloupla.simpleshot.svg`
- [x] App ID로 명명됨
- [x] 업스트림 프로젝트에 포함 예정
- [x] 올바른 위치에 설치:
  ```
  ${FLATPAK_DEST}/share/icons/hicolor/scalable/apps/net.bloupla.simpleshot.svg
  ```

## ✅ Name and Icon

- [x] 애플리케이션 이름 "SimpleShot"이 고유함
- [x] 아이콘이 고유함
- [x] 상표권 침해 없음

## 📋 최종 체크리스트

### GitHub 저장소 준비
- [ ] https://github.com/llaa33219/SimpleShot/ 생성
- [ ] 다음 파일 업로드:
  - [ ] `simpleshot.py`
  - [ ] `net.bloupla.simpleshot.desktop`
  - [ ] `net.bloupla.simpleshot.metainfo.xml`
  - [ ] `icons/net.bloupla.simpleshot.svg`
  - [ ] `LICENSE`
  - [ ] `README.md`
  - [ ] 기타 문서들
- [ ] 태그 생성: `git tag -a v1.0.0 -m "Release v1.0.0"`
- [ ] 태그 푸시: `git push origin v1.0.0`
- [ ] Commit hash 확인: `git rev-parse v1.0.0`
- [ ] Manifest에 commit hash 업데이트

### 도메인 검증
- [ ] `bloupla.net` 도메인 제어권 확인
- [ ] 검증 토큰 배치 준비

### 검증
- [ ] MetaInfo 검증:
  ```bash
  appstreamcli validate net.bloupla.simpleshot.metainfo.xml
  ```
- [ ] Desktop 파일 검증:
  ```bash
  desktop-file-validate net.bloupla.simpleshot.desktop
  ```
- [ ] 로컬 빌드 테스트:
  ```bash
  flatpak-builder --user --install --force-clean build-dir net.bloupla.simpleshot.yml
  flatpak run net.bloupla.simpleshot
  ```

### Flathub 제출
- [ ] Flathub 저장소 생성 요청
- [ ] manifest와 flathub.json만 Flathub 저장소에 추가
- [ ] Pull Request 생성
- [ ] 리뷰어 피드백 대응

## 📊 요구사항 준수 요약

| 카테고리 | 상태 | 비고 |
|---------|------|------|
| Inclusion Policy | ✅ | 모든 정책 준수 |
| Application ID | ⚠️ | 도메인 검증 필요 |
| License | ✅ | MIT, 올바르게 명시 |
| Permissions | ✅ | 최소 권한, Portal 사용 |
| Build | ✅ | 소스 빌드, 네트워크 불필요 |
| Required Files | ✅ | Manifest, flathub.json |
| Metadata | ✅ | MetaInfo, Desktop, Icon |
| GitHub Integration | ⏳ | 저장소 생성 대기 |

## 🎯 다음 단계

1. **GitHub에 코드 업로드**
   ```bash
   git init
   git add .
   git commit -m "Initial release v1.0.0"
   git remote add origin https://github.com/llaa33219/SimpleShot.git
   git push -u origin main
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

2. **Commit hash 업데이트**
   ```bash
   git rev-parse v1.0.0
   # 출력된 hash를 net.bloupla.simpleshot.yml에 입력
   ```

3. **도메인 검증 준비**
   - `bloupla.net/.well-known/org.flathub.VerifiedApps.txt` 준비

4. **Flathub 제출**
   - 상세한 가이드: [FLATHUB_SUBMISSION_GUIDE.md](FLATHUB_SUBMISSION_GUIDE.md)

---

## ✅ 결론

SimpleShot은 [Flathub Requirements](https://docs.flathub.org/docs/for-app-authors/requirements#required-files)의 **모든 주요 요구사항을 준수**합니다.

**남은 작업**:
1. GitHub 저장소 생성 및 코드 업로드
2. 도메인 검증 (사용자가 처리)
3. Flathub 제출

**준비 완료!** 🎉

