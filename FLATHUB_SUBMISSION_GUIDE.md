# Flathub 제출 가이드

## ✅ Flathub 요구사항 준수 확인

### 1. Required Files (필수 파일)

#### ✅ Manifest
- [x] `net.bloupla.simpleshot.yml` - 최상위 레벨에 위치
- [x] App ID로 명명됨
- [x] Runtime이 Flathub에서 호스팅됨 (org.gnome.Platform)

#### ✅ flathub.json
- [x] 아키텍처 지정 (`x86_64`, `aarch64`)

#### ✅ Metadata Files (업스트림에 통합 필요)

**중요**: [Flathub 문서](https://docs.flathub.org/docs/for-app-authors/requirements#required-files)에 따르면, 다음 파일들은 **업스트림 프로젝트(GitHub 저장소)에 포함**되어야 합니다:

- [x] `net.bloupla.simpleshot.metainfo.xml` - AppStream metadata
- [x] `net.bloupla.simpleshot.desktop` - Desktop entry
- [x] `icons/net.bloupla.simpleshot.svg` - SVG icon
- [x] `LICENSE` - MIT License

### 2. GitHub 저장소 설정

**저장소 URL**: https://github.com/llaa33219/SimpleShot/

#### 업로드해야 할 파일들:
```
SimpleShot/
├── simpleshot.py                       # 메인 코드
├── net.bloupla.simpleshot.desktop      # Desktop file
├── net.bloupla.simpleshot.metainfo.xml # MetaInfo
├── icons/
│   └── net.bloupla.simpleshot.svg      # Icon
├── LICENSE                             # License file
├── README.md                           # 문서
├── BUILDING.md
├── CONTRIBUTING.md
├── QUICKSTART.md
└── ... (기타 문서)
```

**제외할 파일** (Flathub 제출 시에만 사용):
- `net.bloupla.simpleshot.yml` (Flathub 저장소에만)
- `flathub.json` (Flathub 저장소에만)

### 3. Flathub 제출 프로세스

#### Step 1: GitHub에 코드 업로드

```bash
cd /home/luke/GoogleDrive/Code/프로그램/SimpleShot

# Git 초기화 (아직 안 했다면)
git init
git add simpleshot.py net.bloupla.simpleshot.desktop net.bloupla.simpleshot.metainfo.xml
git add icons/ LICENSE README.md BUILDING.md CONTRIBUTING.md QUICKSTART.md
git add PROJECT_STRUCTURE.md PROJECT_SUMMARY.md START_HERE.md
git add .gitignore .editorconfig

# 커밋
git commit -m "Initial release v1.0.0"

# 리모트 추가
git remote add origin https://github.com/llaa33219/SimpleShot.git

# 푸시
git branch -M main
git push -u origin main

# 태그 생성 (중요!)
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

#### Step 2: Commit Hash 업데이트

태그를 푸시한 후:
```bash
# Commit hash 확인
git rev-parse v1.0.0

# 출력된 hash를 manifest 파일에 업데이트
```

`net.bloupla.simpleshot.yml` 수정:
```yaml
sources:
  - type: git
    url: https://github.com/llaa33219/SimpleShot.git
    tag: v1.0.0
    commit: <실제-commit-hash>  # 위에서 확인한 hash
```

#### Step 3: Flathub 저장소 준비

1. **Flathub GitHub 방문**: https://github.com/flathub/flathub

2. **새 저장소 생성 요청**:
   - Flathub에 새 앱을 추가하려면 먼저 이슈 생성
   - 또는 기존 앱이면 해당 저장소 fork

3. **새 앱인 경우**:
   - 이슈를 통해 `flathub/net.bloupla.simpleshot` 저장소 생성 요청
   - 승인되면 fork 후 작업

4. **저장소에 파일 추가**:
   ```bash
   git clone https://github.com/flathub/net.bloupla.simpleshot.git
   cd net.bloupla.simpleshot
   
   # manifest와 flathub.json만 추가
   cp /path/to/SimpleShot/net.bloupla.simpleshot.yml .
   cp /path/to/SimpleShot/flathub.json .
   
   git add net.bloupla.simpleshot.yml flathub.json
   git commit -m "Initial Flathub submission"
   git push
   ```

5. **Pull Request 생성**:
   - Flathub 리뷰어가 검토
   - 피드백 반영
   - 승인 후 Flathub에 게시

### 4. 검증 체크리스트

#### 필수 확인 사항:

- [ ] GitHub 저장소가 public임
- [ ] 태그 `v1.0.0` 생성됨
- [ ] Commit hash가 manifest에 정확히 입력됨
- [ ] MetaInfo 검증 통과:
  ```bash
  appstreamcli validate net.bloupla.simpleshot.metainfo.xml
  ```
- [ ] Desktop 파일 검증 통과:
  ```bash
  desktop-file-validate net.bloupla.simpleshot.desktop
  ```
- [ ] 로컬 빌드 테스트 성공:
  ```bash
  flatpak-builder --user --install --force-clean build-dir net.bloupla.simpleshot.yml
  flatpak run net.bloupla.simpleshot
  ```

#### 권한 확인:

현재 권한이 최소한으로 설정되어 있는지 확인:
```yaml
finish-args:
  - --socket=wayland          # ✅ 필수
  - --socket=fallback-x11     # ✅ 필수 (호환성)
  - --device=dri              # ✅ GPU 가속
  - --talk-name=org.freedesktop.portal.Desktop  # ✅ Portal 사용
  - --filesystem=xdg-pictures:create  # ✅ 최소 권한 (Pictures만)
  - --filesystem=xdg-videos:create    # ✅ 최소 권한 (Videos만)
```

❌ **과도한 권한 없음**:
- `--filesystem=home` (전체 홈 디렉토리)
- `--filesystem=host` (전체 시스템)
- `--share=network` (네트워크 접근)

### 5. 도메인 검증

App ID가 `net.bloupla.simpleshot`이므로 도메인 `bloupla.net`에 대한 제어권을 증명해야 합니다.

#### 방법 1: .well-known 파일

1. `https://bloupla.net/.well-known/org.flathub.VerifiedApps.txt` 생성
2. Flathub에서 제공하는 토큰 추가

#### 방법 2: 명시적 연결

웹사이트에 SimpleShot 프로젝트 링크 표시

### 6. 제출 후 프로세스

1. **리뷰 대기**
   - Flathub 리뷰어가 검토
   - 일반적으로 며칠 ~ 1주일 소요

2. **피드백 대응**
   - 리뷰어 코멘트에 응답
   - 필요시 수정 후 커밋

3. **승인**
   - 모든 요구사항 충족 시 승인
   - Flathub에 자동 게시

4. **게시 후**
   - Flathub 웹사이트에 표시
   - 사용자가 설치 가능:
     ```bash
     flatpak install flathub net.bloupla.simpleshot
     ```

### 7. 업데이트 프로세스

새 버전 릴리스 시:

1. GitHub에 새 버전 푸시:
   ```bash
   # 코드 수정 후
   git commit -am "Version 1.1.0: New features"
   git tag -a v1.1.0 -m "Release v1.1.0"
   git push origin main v1.1.0
   ```

2. Flathub manifest 업데이트:
   ```yaml
   sources:
     - type: git
       url: https://github.com/llaa33219/SimpleShot.git
       tag: v1.1.0
       commit: <new-commit-hash>
   ```

3. Pull Request 생성

4. 자동 빌드 및 배포

### 8. 문제 해결

#### "MetaInfo validation failed"
```bash
# 검증 도구 설치
sudo pacman -S appstream

# 검증 실행
appstreamcli validate net.bloupla.simpleshot.metainfo.xml
```

#### "Desktop file validation failed"
```bash
# 검증 도구 설치
sudo pacman -S desktop-file-utils

# 검증 실행
desktop-file-validate net.bloupla.simpleshot.desktop
```

#### "Build failed"
- 로컬에서 먼저 테스트
- 로그 확인
- 의존성 문제 확인

### 9. 참고 문서

- **Flathub Requirements**: https://docs.flathub.org/docs/for-app-authors/requirements
- **Flathub Submission**: https://docs.flathub.org/docs/for-app-authors/submission
- **MetaInfo Guidelines**: https://docs.flathub.org/docs/for-app-authors/metainfo-guidelines
- **GitHub 저장소**: https://github.com/llaa33219/SimpleShot

### 10. 체크리스트 요약

제출 전 최종 확인:

- [ ] GitHub 저장소 생성 및 코드 업로드
- [ ] 릴리스 태그 생성 (v1.0.0)
- [ ] Manifest에 정확한 commit hash
- [ ] MetaInfo 검증 통과
- [ ] Desktop file 검증 통과
- [ ] 로컬 빌드 테스트 성공
- [ ] 도메인 검증 준비
- [ ] Flathub 저장소에 manifest + flathub.json
- [ ] Pull Request 생성
- [ ] 리뷰어 피드백 대기

---

**모든 준비가 완료되었습니다!** 🎉

GitHub에 코드를 업로드하고 Flathub에 제출하세요!

