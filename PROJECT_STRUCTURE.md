# SimpleShot Project Structure

## 📁 파일 구조

```
SimpleShot/
├── net.bloupla.simpleshot.yml      # Flatpak manifest (메인 빌드 파일)
├── net.bloupla.simpleshot.metainfo.xml  # AppStream metadata
├── net.bloupla.simpleshot.desktop  # Desktop entry file
├── flathub.json                    # Flathub 설정 (아키텍처)
├── simpleshot.py                   # 메인 애플리케이션 코드
├── icons/
│   └── net.bloupla.simpleshot.svg  # 애플리케이션 아이콘
├── LICENSE                         # MIT 라이선스
├── README.md                       # 사용자 문서
├── BUILDING.md                     # 빌드 가이드
├── CONTRIBUTING.md                 # 기여 가이드
├── FLATHUB_CHECKLIST.md           # Flathub 제출 체크리스트
├── PROJECT_STRUCTURE.md           # 이 파일
├── build.sh                        # 빌드 스크립트
└── .gitignore                      # Git ignore 파일
```

## 📝 주요 파일 설명

### Flatpak Manifest (`net.bloupla.simpleshot.yml`)

애플리케이션 빌드 방법을 정의하는 YAML 파일:
- App ID: `net.bloupla.simpleshot`
- Runtime: GNOME Platform 47
- 권한 (finish-args): Wayland, X11, portals, 파일시스템
- 빌드 모듈: simpleshot Python 스크립트 및 메타데이터 설치

### MetaInfo (`net.bloupla.simpleshot.metainfo.xml`)

AppStream 메타데이터:
- 앱 이름, 설명, 스크린샷
- 라이선스 정보 (MIT)
- 릴리즈 정보
- 개발자 정보
- 카테고리 및 키워드

### Desktop File (`net.bloupla.simpleshot.desktop`)

데스크톱 통합:
- 애플리케이션 런처 정보
- 실행 명령: `simpleshot`
- 카테고리: Graphics, Utility
- 아이콘 및 이름

### Main Application (`simpleshot.py`)

Python/GTK 4 애플리케이션:

#### 클래스 구조:

1. **SimpleShotConfig**
   - 설정 관리 (저장 위치)
   - `~/.var/app/net.bloupla.simpleshot/config/settings.conf`에 저장

2. **SettingsWindow** (Adw.ApplicationWindow)
   - 메인 설정 창
   - 저장 위치 선택
   - "Start Capture" 버튼

3. **SelectionWindow** (Gtk.Window)
   - 전체화면 오버레이
   - 영역 선택 UI
   - 캡처/녹화 메뉴
   - 드로잉: 반투명 오버레이, 선택 영역, 버튼 메뉴

4. **SimpleShotApp** (Adw.Application)
   - 메인 애플리케이션 클래스
   - App ID: `net.bloupla.simpleshot`

#### 주요 기능:

**스크린샷 (`take_screenshot`)**:
1. XDG Screenshot Portal 시도
2. Fallback: `grim` (Wayland) 또는 `import` (X11)
3. 클립보드에 자동 복사
4. `~/Pictures/Screenshots/` 저장

**녹화 (`start_recording`/`stop_recording`)**:
1. XDG Screencast Portal (계획)
2. Fallback: `wf-recorder` (Wayland) 또는 `ffmpeg` (X11)
3. `~/Videos/Recordings/` 저장
4. 빨간 테두리로 녹화 중 표시

**UI 요소**:
- 드래그로 영역 선택
- 중앙 하단 메뉴 (카메라 아이콘, 녹화 아이콘)
- ESC로 취소
- 녹화 중 빨간 테두리 표시

### Icon (`icons/net.bloupla.simpleshot.svg`)

SVG 벡터 아이콘:
- 카메라 렌즈 디자인
- 파란 그라디언트 배경
- 뷰파인더 모서리
- 빨간 녹화 표시점

## 🔧 기술 스택

- **언어**: Python 3
- **GUI**: GTK 4, Libadwaita 1
- **Runtime**: GNOME Platform 47
- **패키징**: Flatpak
- **보안**: XDG Portals (screenshot, screencast)
- **그래픽**: Cairo (drawing)

## 🔐 보안 & 샌드박싱

### 권한 (Minimal Permissions):
```yaml
--socket=wayland              # Wayland 디스플레이
--socket=fallback-x11         # X11 폴백
--device=dri                  # GPU 가속
--talk-name=org.freedesktop.portal.Desktop  # Portals
--filesystem=xdg-pictures:create  # 스크린샷 저장
--filesystem=xdg-videos:create    # 녹화 저장
```

### Portal 사용:
- Screenshot Portal: 스크린 캡처
- Screencast Portal: 화면 녹화
- File Chooser Portal: 디렉토리 선택

## 🚀 빌드 & 실행

### 빌드:
```bash
./build.sh
# 또는
flatpak-builder --user --install --force-clean build-dir net.bloupla.simpleshot.yml
```

### 실행:
```bash
flatpak run net.bloupla.simpleshot
```

### 개발:
```bash
# 수정 후 재빌드
flatpak-builder --user --install build-dir net.bloupla.simpleshot.yml

# 디버그 출력 확인
flatpak run net.bloupla.simpleshot
```

## 📦 배포

### 로컬 번들:
```bash
flatpak build-bundle repo simpleshot.flatpak net.bloupla.simpleshot
```

### Flathub 제출:
1. Flathub GitHub fork
2. 매니페스트 및 메타데이터 추가
3. 테스트
4. Pull Request 제출
5. 리뷰 통과

## 🎯 디자인 결정

### 왜 GTK 4 + Libadwaita?
- 현대적인 GNOME 스타일 UI
- Flatpak과 완벽한 통합
- Portal 지원 우수
- 최신 디자인 가이드라인 준수

### 왜 Python?
- 빠른 프로토타이핑
- GTK 바인딩 우수
- 코드 가독성 좋음
- Flatpak에서 쉽게 패키징

### 샌드박싱 우선:
- Flathub 정책 준수
- 보안 우수
- Portal 우선, fallback은 보조적

### 간단함 유지:
- 복잡한 설정 없음
- 핵심 기능에 집중
- 직관적인 UI
- 빠른 작업 흐름

## 🔄 데이터 흐름

1. **시작** → SettingsWindow 표시
2. **Start Capture** → SelectionWindow (fullscreen)
3. **영역 선택** → 드래그로 선택
4. **캡처** → Portal/grim/import → 저장 + 클립보드
5. **녹화** → Portal/wf-recorder/ffmpeg → 파일 저장
6. **완료** → SettingsWindow로 복귀

## 📊 설정 저장 위치

- **설정 파일**: `~/.var/app/net.bloupla.simpleshot/config/settings.conf`
- **스크린샷**: `~/Pictures/Screenshots/` (사용자 설정 가능)
- **녹화**: `~/Videos/Recordings/` (사용자 설정 가능)

## 🐛 알려진 제한사항

1. **녹화**: 완전한 Portal 구현 필요 (현재 fallback 사용)
2. **다중 모니터**: 추가 테스트 필요
3. **주석 도구**: 미구현 (향후 추가 가능)
4. **지연 캡처**: 미구현

## 🎨 UI/UX 특징

- **다크 오버레이**: 선택되지 않은 영역 어둡게
- **파란 테두리**: 선택 영역 표시
- **빨간 테두리**: 녹화 중 표시
- **중앙 메뉴**: 쉬운 접근성
- **아이콘 기반**: 텍스트 없이 직관적
- **ESC 취소**: 빠른 종료

## 📚 코드 참조

### 핵심 함수:

- `SimpleShotConfig.load_config()` - 설정 로드
- `SettingsWindow.on_start_capture()` - 캡처 시작
- `SelectionWindow.on_draw()` - UI 렌더링
- `SelectionWindow.take_screenshot()` - 스크린샷
- `SelectionWindow.start_recording()` - 녹화 시작

### Portal 연동:

```python
portal = Gio.DBusProxy.new_for_bus_sync(
    Gio.BusType.SESSION,
    'org.freedesktop.portal.Desktop',
    '/org/freedesktop/portal/desktop',
    'org.freedesktop.portal.Screenshot'
)
```

## 🔍 디버깅

```bash
# 상세 로그 출력
flatpak run net.bloupla.simpleshot

# 권한 확인
flatpak info --show-permissions net.bloupla.simpleshot

# 파일 위치 확인
flatpak run --command=sh net.bloupla.simpleshot
```

## ✨ 향후 개선 사항

보다 자세한 내용은 `CONTRIBUTING.md` 참조.

