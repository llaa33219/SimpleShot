# SimpleShot - Quick Start Guide

SimpleShot을 빠르게 시작하기 위한 가이드입니다.

## 🚀 5분 안에 시작하기

### 1단계: 의존성 설치

```bash
# Flatpak 설치 (Manjaro에 기본 포함)
sudo pacman -S flatpak flatpak-builder

# Flathub 추가
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# GNOME Runtime 설치
flatpak install -y flathub org.gnome.Platform//49 org.gnome.Sdk//49
```

### 2단계: 빌드

```bash
cd /home/luke/GoogleDrive/Code/프로그램/SimpleShot
./build.sh
```

### 3단계: 실행

```bash
flatpak run net.bloupla.simpleshot
```

## 📖 사용 방법

### 스크린샷 찍기

1. **SimpleShot 실행**
   ```bash
   flatpak run net.bloupla.simpleshot
   ```

2. **"Start Capture" 버튼 클릭**

3. **영역 선택**
   - 마우스로 클릭 & 드래그하여 영역 선택

4. **캡처**
   - 화면 하단 중앙의 **파란 카메라 아이콘** 클릭
   - 자동으로 저장되고 클립보드에 복사됨!

### 화면 녹화하기

1. **SimpleShot 실행 및 Start Capture**

2. **영역 선택** (드래그)

3. **녹화 시작**
   - 화면 하단 중앙의 **빨간 녹화 아이콘** 클릭
   - 선택 영역 테두리가 빨간색으로 변경됨

4. **녹화 중지**
   - 다시 **녹화 아이콘** 클릭 (정사각형으로 표시됨)
   - 또는 **ESC** 키 누르기
   - 비디오 파일이 자동 저장됨!

### 저장 위치 변경

1. SimpleShot 메인 창에서:
   - **"Screenshots Location"** → "Choose" 버튼
   - **"Recordings Location"** → "Choose" 버튼
   - 원하는 폴더 선택

2. 설정은 자동으로 저장됩니다!

## ⌨️ 키보드 단축키

- `ESC` - 선택 취소 또는 녹화 중지

## 💾 기본 저장 위치

- **스크린샷**: `~/Pictures/Screenshots/`
  - 파일명: `screenshot_2025-10-25_14-30-45.png`

- **녹화**: `~/Videos/Recordings/`
  - 파일명: `recording_2025-10-25_14-30-45.webm`

## 🎨 UI 가이드

### 메인 창
```
┌─────────────────────────────┐
│      SimpleShot             │
│  Screen Capture & Recording │
│                             │
│  Settings                   │
│  ├─ Screenshots Location    │
│  └─ Recordings Location     │
│                             │
│     [Start Capture]         │
│                             │
│  Command: flatpak run ...   │
└─────────────────────────────┘
```

### 선택 화면
```
화면 전체가 어두워짐 (반투명 오버레이)
┌─────────────────────────────┐
│  어두움                      │
│    ┌─────────────┐          │  ← 선택 영역 (밝음)
│    │ 선택 영역    │          │     파란 테두리
│    └─────────────┘          │
│                             │
│         [📷] [⏺]           │  ← 중앙 하단 메뉴
└─────────────────────────────┘
      캡처  녹화
```

## 🔧 문제 해결

### "Screenshot doesn't work"

**Wayland 사용자:**
```bash
# grim 설치 (권장)
sudo pacman -S grim
```

**X11 사용자:**
```bash
# ImageMagick 설치
sudo pacman -S imagemagick
```

### "Recording doesn't work"

**Wayland 사용자:**
```bash
# wf-recorder 설치 (권장)
sudo pacman -S wf-recorder
```

**X11 사용자:**
```bash
# FFmpeg 설치
sudo pacman -S ffmpeg
```

### "Can't find saved files"

설정 창에서 저장 위치를 확인하세요:
```bash
# 기본 위치 확인
ls ~/Pictures/Screenshots/
ls ~/Videos/Recordings/
```

### "Permission denied"

Flatpak이 해당 폴더에 접근할 수 있는지 확인:
```bash
# 권한 확인
flatpak info --show-permissions net.bloupla.simpleshot

# 필요시 권한 추가
flatpak override --user --filesystem=home net.bloupla.simpleshot
```

## 📱 명령줄 사용

직접 실행:
```bash
flatpak run net.bloupla.simpleshot
```

별칭 만들기:
```bash
echo "alias simpleshot='flatpak run net.bloupla.simpleshot'" >> ~/.bashrc
source ~/.bashrc

# 이제 간단히:
simpleshot
```

## 🎯 팁 & 트릭

1. **빠른 스크린샷**
   - 실행 → Start Capture → 영역 선택 → 카메라 아이콘
   - 클립보드에 자동 복사되므로 바로 붙여넣기 가능!

2. **정확한 선택**
   - 천천히 드래그하여 정확한 영역 선택
   - 잘못 선택했으면 ESC 누르고 다시 시작

3. **녹화 팁**
   - 녹화 시작 전 영역을 정확히 선택
   - 빨간 테두리로 녹화 중임을 확인
   - ESC로 언제든 중지 가능

4. **저장 위치 조직화**
   - 프로젝트별 폴더 생성
   - 설정에서 빠르게 변경 가능

## 🌟 다음 단계

- 더 자세한 정보: `README.md` 참조
- 빌드 방법: `BUILDING.md` 참조
- 기여하기: `CONTRIBUTING.md` 참조
- Flathub 제출: `FLATHUB_CHECKLIST.md` 참조

## 📞 도움이 필요하신가요?

- 버그 리포트: GitHub Issues
- 기능 요청: GitHub Issues
- 질문: GitHub Discussions

## ⚡ 즐거운 스크린샷/녹화 되세요!

SimpleShot을 사용해 주셔서 감사합니다! 🎉

