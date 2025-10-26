# Building SimpleShot

## Prerequisites

- Flatpak
- Flatpak Builder
- GNOME Platform runtime

## Install Dependencies

```bash
# Add Flathub repository (if not already added)
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Install GNOME runtime and SDK
flatpak install flathub org.gnome.Platform//49
flatpak install flathub org.gnome.Sdk//49
```

## Build and Install

### Build the Flatpak (Local Development)

```bash
# Quick build (recommended)
./build.sh

# Manual build
# Use the local manifest for development
flatpak-builder --user --install --force-clean \
  --state-dir=/tmp/simpleshot-flatpak-builder \
  /tmp/simpleshot-build \
  net.bloupla.simpleshot.local.yml
```

**Important Notes**: 
- `net.bloupla.simpleshot.local.yml` - 로컬 개발용 (로컬 파일 사용)
- `net.bloupla.simpleshot.yml` - Flathub 제출용 (GitHub에서 소스 다운로드)
- **빌드 디렉토리**: `/tmp/simpleshot-build` 사용 (GoogleDrive는 심볼릭 링크 미지원)

### Run the Application

```bash
flatpak run net.bloupla.simpleshot
```

## Development Mode

For faster iteration during development:

```bash
# Build without cleaning
flatpak-builder --user --install build-dir net.bloupla.simpleshot.yml

# Run with debug output
flatpak run net.bloupla.simpleshot
```

## Testing

### Test the Application

1. Launch the application
2. Configure save locations if needed
3. Click "Start Capture"
4. Select an area by dragging
5. Test screenshot (camera icon)
6. Test recording (record icon)

### Manifest Files

프로젝트에는 두 개의 manifest 파일이 있습니다:

1. **`net.bloupla.simpleshot.local.yml`** (로컬 개발용)
   - 로컬 파일 경로 사용
   - 빠른 반복 개발에 적합
   - `./build.sh`가 이 파일 사용

2. **`net.bloupla.simpleshot.yml`** (Flathub 제출용)
   - GitHub 저장소에서 소스 다운로드
   - Flathub 제출 시 사용
   - 태그와 commit hash 필요

### Verify Permissions

Check that the application has the correct permissions:

```bash
flatpak info --show-permissions net.bloupla.simpleshot
```

Expected permissions:
- `wayland` - Wayland socket access
- `fallback-x11` - X11 fallback support
- `dri` - GPU acceleration
- Portal access for screenshots/screencasts

## Common Issues

### Issue: Screenshot/Recording doesn't work

**Solution**: Make sure you have the required tools installed in the Flatpak:
- For screenshots: XDG Screenshot Portal or `grim` (Wayland) / `import` (X11)
- For recordings: `wf-recorder` (Wayland) / `ffmpeg` (X11)

### Issue: Can't save to Pictures/Videos

**Solution**: Check filesystem permissions in the manifest. The app should have:
```yaml
- --filesystem=xdg-pictures:create
- --filesystem=xdg-videos:create
```

### Issue: Clipboard not working

**Solution**: Make sure the Wayland socket is accessible.

## Cleanup

Remove the build:

```bash
# Build directories are in /tmp, so they will be automatically cleaned on reboot
# Manual cleanup if needed:
rm -rf /tmp/simpleshot-build /tmp/simpleshot-flatpak-builder
```

Uninstall:

```bash
flatpak uninstall --user net.bloupla.simpleshot
```

## Creating a Bundle

To create a distributable bundle:

```bash
# Build the application
flatpak-builder --repo=repo build-dir net.bloupla.simpleshot.yml

# Create a single-file bundle
flatpak build-bundle repo simpleshot.flatpak net.bloupla.simpleshot
```

Install the bundle:

```bash
flatpak install simpleshot.flatpak
```

## Submitting to Flathub

1. Fork the Flathub repository template
2. Add your manifest and required files
3. Test thoroughly
4. Submit a pull request
5. Address reviewer feedback

See [Flathub submission guidelines](https://docs.flathub.org/docs/for-app-authors/submission) for details.

