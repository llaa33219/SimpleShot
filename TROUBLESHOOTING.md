# SimpleShot - 문제 해결 가이드

## 빌드 문제

### ❌ "Error making symbolic link" 오류

**증상**:
```
error: Error making symbolic link /path/to/build-dir/var/run: Input/output error
```

**원인**: 
- GoogleDrive, OneDrive, Dropbox 등 클라우드 동기화 폴더는 심볼릭 링크를 지원하지 않습니다
- Flatpak 빌드 시 심볼릭 링크가 필수입니다

**해결책**:
```bash
# 자동 해결: build.sh 사용 (권장)
./build.sh

# 수동 해결: 로컬 파일시스템에 빌드
flatpak-builder --user --install --force-clean /tmp/simpleshot-build net.bloupla.simpleshot.local.yml
```

### ❌ "Runtime not found" 오류

**증상**:
```
error: Runtime org.gnome.Platform/x86_64/49 not found
```

**해결책**:
```bash
# GNOME Platform 설치
flatpak install flathub org.gnome.Platform//49 org.gnome.Sdk//49
```

### ❌ "Permission denied" 오류

**증상**:
```
error: Failed to install: Permission denied
```

**해결책**:
```bash
# User 설치 확인
flatpak-builder --user --install --force-clean /tmp/simpleshot-build net.bloupla.simpleshot.local.yml

# 또는 기존 설치 제거 후 재설치
flatpak uninstall --user net.bloupla.simpleshot
./build.sh
```

## 실행 문제

### ❌ 앱이 실행되지 않음

**확인 사항**:
```bash
# 설치 확인
flatpak list --app | grep simpleshot

# 수동 실행
flatpak run net.bloupla.simpleshot

# 로그 확인
flatpak run net.bloupla.simpleshot 2>&1 | tee simpleshot.log
```

### ❌ 스크린샷/녹화가 작동하지 않음

**Wayland 사용자**:
```bash
# 필요한 도구 설치
sudo pacman -S grim wf-recorder  # Manjaro/Arch
sudo apt install grim wf-recorder # Ubuntu/Debian
```

**X11 사용자**:
```bash
# 필요한 도구 설치
sudo pacman -S imagemagick ffmpeg  # Manjaro/Arch
sudo apt install imagemagick ffmpeg # Ubuntu/Debian
```

### ❌ 파일 저장 권한 오류

**증상**:
```
Permission denied when saving to Pictures/Videos
```

**해결책**:
```bash
# 디렉토리 생성
mkdir -p ~/Pictures/Screenshots
mkdir -p ~/Videos/Recordings

# 권한 확인
flatpak info --show-permissions net.bloupla.simpleshot

# 필요시 권한 추가
flatpak override --user --filesystem=xdg-pictures:create net.bloupla.simpleshot
flatpak override --user --filesystem=xdg-videos:create net.bloupla.simpleshot
```

## 개발 문제

### ❌ Python 구문 오류

**확인**:
```bash
# Python 구문 검사
python3 -m py_compile simpleshot.py

# 실행 권한 확인
chmod +x simpleshot.py
```

### ❌ GTK/Libadwaita 오류

**증상**:
```
ImportError: cannot import name 'Adw' from 'gi.repository'
```

**원인**: 
- GNOME Platform 49가 필요합니다

**해결책**:
```bash
# Runtime 재설치
flatpak install --reinstall flathub org.gnome.Platform//49
```

## Flathub 제출 문제

### ❌ MetaInfo 검증 실패

**검증**:
```bash
# AppStream 도구 설치
sudo pacman -S appstream  # Manjaro/Arch
sudo apt install appstream # Ubuntu/Debian

# 검증 실행
appstreamcli validate net.bloupla.simpleshot.metainfo.xml
```

### ❌ Desktop 파일 검증 실패

**검증**:
```bash
# 검증 도구 설치
sudo pacman -S desktop-file-utils  # Manjaro/Arch
sudo apt install desktop-file-utils # Ubuntu/Debian

# 검증 실행
desktop-file-validate net.bloupla.simpleshot.desktop
```

### ❌ Commit hash 오류

**문제**: manifest의 commit hash가 잘못됨

**해결책**:
```bash
# 올바른 commit hash 확인
git rev-parse v1.0.0

# net.bloupla.simpleshot.yml에서 COMMIT_HASH_HERE를 실제 hash로 교체
```

## 일반 문제

### GoogleDrive 폴더 사용 시 주의사항

**문제점**:
- 심볼릭 링크 미지원
- 빌드 속도 느림
- 파일 동기화 충돌 가능

**권장 방법**:
1. 소스 코드는 GoogleDrive에 보관 ✅
2. 빌드는 `/tmp` 또는 `~/.cache`에서 수행 ✅
3. `build.sh` 스크립트 사용 (자동 처리) ✅

### 로그 수집

**디버깅용 로그**:
```bash
# 상세 로그
flatpak run --verbose net.bloupla.simpleshot 2>&1 | tee debug.log

# 빌드 로그
flatpak-builder --verbose /tmp/simpleshot-build net.bloupla.simpleshot.local.yml 2>&1 | tee build.log
```

## 도움 요청

문제가 해결되지 않으면:

1. **로그 확인**: 위의 로그 수집 명령어 실행
2. **GitHub Issues**: https://github.com/llaa33219/SimpleShot/issues
3. **문서 참조**: 
   - [BUILDING.md](BUILDING.md)
   - [QUICKSTART.md](QUICKSTART.md)
   - [README.md](README.md)

## 자주 묻는 질문 (FAQ)

**Q: GoogleDrive에서 빌드할 수 없나요?**
A: 직접 빌드는 불가능합니다. `./build.sh`를 사용하면 자동으로 `/tmp`에 빌드됩니다.

**Q: 왜 /tmp를 사용하나요?**
A: `/tmp`는 로컬 파일시스템이므로 심볼릭 링크를 지원하며, 재부팅 시 자동 정리됩니다.

**Q: 빌드 파일이 너무 큰데요?**
A: `/tmp`는 재부팅 시 자동 정리됩니다. 수동 정리: `rm -rf /tmp/simpleshot-build`

**Q: GNOME 49가 설치되지 않아요**
A: Flathub 저장소 확인: `flatpak remote-list` 후 `flatpak update`

---

**더 많은 정보**: [README.md](README.md)

