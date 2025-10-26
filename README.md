# SimpleShot

<p align="center">
  <img src="icons/net.bloupla.simpleshot.svg" width="128" height="128" alt="SimpleShot Icon">
</p>

<p align="center">
  <strong>간단하고 가벼운 Linux용 화면 캡처 및 녹화 도구</strong>
</p>

<p align="center">
  A simple and lightweight screen capture and recording tool for Linux desktop
</p>

## Features

- 📸 **Screenshot Capture**: Quickly capture any area of your screen
- 🎥 **Screen Recording**: Record screen activity with visual feedback
- 📋 **Clipboard Integration**: Screenshots are automatically copied to clipboard
- ⚙️ **Configurable Save Locations**: Choose where to save screenshots and recordings
- 🎨 **Intuitive Interface**: Simple area selection with drag and drop

## 🚀 Quick Start

**빠른 시작 가이드는 [QUICKSTART.md](QUICKSTART.md)를 참조하세요!**

## Installation

### From Flathub (준비 중)

```bash
flatpak install flathub net.bloupla.simpleshot
```

### Building from Source

```bash
# Quick build (권장)
./build.sh

# Manual build (로컬 개발용)
flatpak-builder --user --install --force-clean build-dir net.bloupla.simpleshot.local.yml

# Run
flatpak run net.bloupla.simpleshot
```

**상세한 빌드 방법은 [BUILDING.md](BUILDING.md)를 참조하세요.**

**Flathub 제출 방법은 [FLATHUB_SUBMISSION_GUIDE.md](FLATHUB_SUBMISSION_GUIDE.md)를 참조하세요.**

## Usage

1. Launch SimpleShot from your application menu or run:
   ```bash
   flatpak run net.bloupla.simpleshot
   ```

2. Configure your preferred save locations for screenshots and recordings

3. Click "Start Capture" to begin

4. **Select Area**: Click and drag to select the area you want to capture

5. **Choose Action**:
   - **Camera Icon** (Blue): Take a screenshot
   - **Record Icon** (Red): Start/stop screen recording

6. **Keyboard Shortcuts**:
   - `ESC`: Cancel selection or stop recording

## How it Works

SimpleShot uses modern Linux desktop technologies:

- **XDG Desktop Portals**: For secure screenshot and screencast capabilities
- **GTK 4 & Libadwaita**: Modern GNOME-style interface
- **Wayland & X11 Support**: Works on both display servers
- **Sandbox-Friendly**: Respects Flatpak sandboxing with proper portal usage

## Default Save Locations

- **Screenshots**: `~/Pictures/Screenshots/`
- **Recordings**: `~/Videos/Recordings/`

Both locations can be customized in the settings window.

## File Naming

- Screenshots: `screenshot_YYYY-MM-DD_HH-MM-SS.png`
- Recordings: `recording_YYYY-MM-DD_HH-MM-SS.webm`

## Development

This application is built with:
- Python 3
- GTK 4
- Libadwaita 1
- GNOME Platform 49

## License

MIT License - See LICENSE file for details

## Requirements for Flathub Submission

This application follows Flathub requirements:

- ✅ Uses XDG Portals for screen access
- ✅ Minimal filesystem access (only Pictures and Videos directories)
- ✅ Proper AppStream metadata
- ✅ Desktop integration files
- ✅ SVG icon included
- ✅ Application ID follows reverse-DNS format: `net.bloupla.simpleshot`

## 📚 Documentation

### 사용자 가이드
- **[START_HERE.md](START_HERE.md)** ⭐ - 처음 시작하는 분들을 위한 가이드
- **[QUICKSTART.md](QUICKSTART.md)** - 5분 안에 시작하기

### 개발자 가이드
- **[BUILDING.md](BUILDING.md)** - 빌드 및 개발 가이드
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - 기여 가이드
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - 프로젝트 구조 상세
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - 프로젝트 요약

### Flathub 제출 가이드
- **[FLATHUB_REQUIREMENTS_CHECK.md](FLATHUB_REQUIREMENTS_CHECK.md)** ⭐ - 전체 요구사항 확인
- **[FLATHUB_SUBMISSION_GUIDE.md](FLATHUB_SUBMISSION_GUIDE.md)** - 단계별 제출 가이드
- **[FLATHUB_CHECKLIST.md](FLATHUB_CHECKLIST.md)** - 간단한 체크리스트

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support

For issues, questions, or contributions, please visit:
- Homepage: https://bloupla.net
- Bug Tracker: https://bloupla.net/simpleshot/issues

## 📋 Flathub Compliance

This application complies with Flathub's [submission requirements](https://docs.flathub.org/docs/for-app-authors/requirements):
- ✅ Sandboxed with minimal permissions
- ✅ Uses portals for privileged operations
- ✅ Provides required metadata (metainfo, desktop file, icon)
- ✅ Open source (MIT License)
- ✅ No network access during build
- ✅ All sources publicly accessible

See [FLATHUB_CHECKLIST.md](FLATHUB_CHECKLIST.md) for the complete checklist.

