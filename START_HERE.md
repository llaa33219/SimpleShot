# 🎉 SimpleShot에 오신 것을 환영합니다!

## 🚀 바로 시작하기

### 1️⃣ 의존성 설치 (최초 1회)

```bash
# Flatpak 및 빌드 도구 설치
sudo pacman -S flatpak flatpak-builder

# GNOME Runtime 설치
flatpak install -y flathub org.gnome.Platform//49 org.gnome.Sdk//49
```

### 2️⃣ 빌드 & 실행

```bash
# 프로젝트 디렉토리로 이동
cd /home/luke/GoogleDrive/Code/프로그램/SimpleShot

# 빌드 (간단!)
./build.sh

# 실행
flatpak run net.bloupla.simpleshot
```

**그게 전부입니다!** 🎊

---

## 📖 무엇을 먼저 읽어야 할까요?

### 사용자라면:
1. **[QUICKSTART.md](QUICKSTART.md)** ⭐ - 5분 안에 시작
2. **[README.md](README.md)** - 전체 기능 소개

### 개발자라면:
1. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** ⭐ - 프로젝트 개요
2. **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - 상세 구조
3. **[BUILDING.md](BUILDING.md)** - 빌드 가이드
4. **[CONTRIBUTING.md](CONTRIBUTING.md)** - 기여 방법

### Flathub 제출 준비라면:
1. **[FLATHUB_CHECKLIST.md](FLATHUB_CHECKLIST.md)** ⭐ - 제출 체크리스트

---

## 🎯 이 프로젝트는 무엇인가요?

**SimpleShot**은 Linux용 화면 캡처 및 녹화 도구입니다.

### 핵심 기능:
- 📸 **스크린샷**: 영역 선택 → 캡처 → 자동 저장 + 클립보드 복사
- 🎥 **녹화**: 영역 선택 → 녹화 시작 → 자동 저장
- ⚙️ **설정**: 저장 위치 자유롭게 선택
- 🎨 **직관적 UI**: 간단하고 현대적인 인터페이스

### 기술적 특징:
- 🔒 **안전함**: Flatpak 샌드박스, XDG Portal 사용
- 🚀 **현대적**: GTK 4, Libadwaita, GNOME 49
- 📦 **배포 준비**: Flathub 제출 준비 완료
- 🌍 **호환성**: Wayland & X11 모두 지원

---

## 📁 파일 구조 한눈에 보기

```
SimpleShot/
├── 🚀 START_HERE.md              ← 지금 읽고 있는 파일
├── 📖 README.md                  ← 메인 문서
├── ⚡ QUICKSTART.md              ← 빠른 시작
├── 📘 PROJECT_SUMMARY.md         ← 프로젝트 요약
├── 📗 PROJECT_STRUCTURE.md       ← 상세 구조
├── 🔨 BUILDING.md                ← 빌드 가이드
├── 🤝 CONTRIBUTING.md            ← 기여 가이드
├── ✅ FLATHUB_CHECKLIST.md       ← Flathub 체크리스트
│
├── 📦 net.bloupla.simpleshot.yml ← Flatpak manifest
├── 🐍 simpleshot.py              ← 메인 코드
├── 🖼️ icons/                     ← 앱 아이콘
├── 📋 net.bloupla.simpleshot.desktop
├── 📋 net.bloupla.simpleshot.metainfo.xml
├── ⚙️ flathub.json
├── 📜 LICENSE (MIT)
└── 🔧 build.sh                   ← 빌드 스크립트
```

---

## 💡 빠른 팁

### 빌드가 실패한다면?
```bash
# 런타임이 설치되어 있는지 확인
flatpak list | grep org.gnome.Platform

# 없다면 설치
flatpak install flathub org.gnome.Platform//47 org.gnome.Sdk//47
```

### 실행이 안 된다면?
```bash
# 설치 확인
flatpak list | grep simpleshot

# 재설치
./build.sh
```

### 스크린샷/녹화가 안 된다면?
```bash
# Wayland용 도구 설치
sudo pacman -S grim wf-recorder

# X11용 도구 설치
sudo pacman -S imagemagick ffmpeg
```

---

## 🎓 주요 개념

### Flatpak이란?
- Linux 앱 패키징 시스템
- 샌드박스 보안
- 배포 통합 (Flathub)

### XDG Portal이란?
- 샌드박스 앱이 시스템 기능 접근
- 보안적으로 스크린샷/녹화
- 사용자 권한 제어

### GTK 4 / Libadwaita란?
- 현대적 Linux UI 프레임워크
- GNOME 스타일 디자인
- 반응형, 접근성 우수

---

## 🔍 다음 단계

### 사용자:
1. ✅ 빌드 & 실행 (`./build.sh`)
2. 📖 [QUICKSTART.md](QUICKSTART.md) 읽기
3. 🎨 스크린샷/녹화 테스트
4. ⭐ 피드백 제공

### 개발자:
1. 📘 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) 읽기
2. 🔍 코드 탐색 (`simpleshot.py`)
3. 🔨 기능 추가/개선
4. 🤝 기여하기

### 배포자:
1. ✅ [FLATHUB_CHECKLIST.md](FLATHUB_CHECKLIST.md) 확인
2. 🧪 다양한 환경에서 테스트
3. 📦 Flathub 제출 준비
4. 🚀 릴리즈!

---

## 🆘 도움이 필요하신가요?

### 문서:
- 📖 일반 사용: [QUICKSTART.md](QUICKSTART.md)
- 🔨 개발: [BUILDING.md](BUILDING.md)
- 🤝 기여: [CONTRIBUTING.md](CONTRIBUTING.md)

### 문제 발생시:
- 🐛 버그 리포트: GitHub Issues
- 💬 질문: GitHub Discussions
- 📧 이메일: [문의처]

---

## ⭐ 프로젝트 특징

이 프로젝트는 다음을 준수합니다:
- ✅ Flathub 모든 요구사항
- ✅ GNOME HIG (Human Interface Guidelines)
- ✅ FreeDesktop.org 표준
- ✅ 보안 best practices
- ✅ 완전한 문서화

---

## 🎊 시작하세요!

```bash
# 지금 바로!
./build.sh && flatpak run net.bloupla.simpleshot
```

**즐거운 스크린샷/녹화 되세요!** 📸🎥

---

<p align="center">
  Made with ❤️ for the Linux community
</p>

<p align="center">
  <strong>SimpleShot - Simple • Secure • Modern</strong>
</p>

