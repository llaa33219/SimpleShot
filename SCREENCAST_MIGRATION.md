# ScreenCast Portal Migration

## Overview
SimpleShot has been migrated from using mixed screen capture methods to using `org.freedesktop.portal.ScreenCast` exclusively for both screenshots and screen recordings.

## What Changed

### Previous Implementation
- **Screenshots**: Used `org.freedesktop.portal.Screenshot` portal
- **Recording**: Used direct X11 grab via ffmpeg (`-f x11grab`)
- **Limitations**: X11-only for recordings, not compatible with Wayland

### New Implementation
- **Screenshots**: Uses `org.freedesktop.portal.ScreenCast` with PipeWire stream
- **Recording**: Uses `org.freedesktop.portal.ScreenCast` with PipeWire stream
- **Benefits**: 
  - Unified portal-based approach
  - Full Wayland compatibility
  - Better security and sandboxing
  - Works across all display servers

## Technical Details

### New Components

#### `ScreenCastSession` Class
Manages the entire lifecycle of a ScreenCast portal session:
1. **Session Creation**: Creates a ScreenCast session via D-Bus
2. **Source Selection**: Prompts user to select screen/window to capture
3. **Stream Start**: Initializes PipeWire streaming
4. **PipeWire Access**: Opens PipeWire remote for media capture
5. **Capture Operations**: Provides screenshot and recording functionality

#### Portal Flow
```
CreateSession -> SelectSources -> Start -> OpenPipeWireRemote
     |              |              |            |
  Session        User picks     Get PipeWire  Access
  handle         source         node ID       stream
```

### Screenshot Implementation
1. User selects area on screen (visual feedback only)
2. ScreenCast session captures full screen via PipeWire
3. Uses gstreamer (`gst-launch-1.0 pipewiresrc`) to grab single frame
4. Falls back to ffmpeg (`-f pipewire`) if gstreamer unavailable
5. Crops captured image to selected area
6. Saves to Pictures/Screenshots directory

### Recording Implementation
1. User selects area on screen (currently visual feedback only)
2. ScreenCast session starts recording via PipeWire
3. Uses ffmpeg to encode stream: `ffmpeg -f pipewire -i <node_id>`
4. Encodes to WebM with VP9 codec
5. Saves to Videos/Recordings directory
6. Clean shutdown on stop with proper process termination

### Dependencies

#### Runtime Requirements
- **PipeWire**: Media streaming framework
- **ffmpeg**: With PipeWire support (`--enable-libpipewire`)
- **GStreamer** (optional): For screenshot capture
  - gst-plugins-base
  - gst-plugins-good (includes pipewiresrc)

#### Flatpak Manifest Updates
- Updated ffmpeg from 4.4.4 to 6.1.1
- Added `--enable-libpipewire` flag
- Removed `--enable-x11grab` (no longer needed)
- Added GStreamer plugins for better PipeWire support

## Known Limitations

### Area Selection for Recording
Currently, area selection for recordings is **visual feedback only**. The recording captures the full selected source (screen/window), not the specific area. This is because:
- ScreenCast portal provides the full source stream
- Cropping video in real-time requires additional processing
- Future improvement: Post-process video with ffmpeg filters to crop

### Workaround Options
1. **Use window selection**: Select specific window instead of full screen
2. **Post-processing**: Crop video after recording with ffmpeg:
   ```bash
   ffmpeg -i input.webm -filter:v "crop=w:h:x:y" output.webm
   ```

## Migration Guide

### For Users
No changes required! The app works the same way:
1. Click "Start Capture"
2. Select screen/window (new portal dialog will appear)
3. Draw selection area
4. Click screenshot or record button

### For Developers
If modifying the code:
- All capture operations go through `ScreenCastSession`
- Session must be created before showing selection UI
- PipeWire node ID is used for all ffmpeg/gstreamer operations
- Session cleanup is automatic on window close

## Testing

### Prerequisites
```bash
# Ensure PipeWire is running
systemctl --user status pipewire

# Check portal availability
busctl --user call org.freedesktop.portal.Desktop \
  /org/freedesktop/portal/desktop \
  org.freedesktop.DBus.Introspectable Introspect
```

### Test Cases
1. ✅ Screenshot with area selection
2. ✅ Recording start/stop
3. ✅ Session cleanup on cancel (Escape key)
4. ✅ Multiple capture sessions
5. ✅ Wayland compatibility
6. ✅ X11 fallback compatibility

## Future Improvements

1. **Area-specific recording**: Implement real-time video cropping
2. **Audio support**: Add microphone/system audio to recordings
3. **Format options**: Allow user to choose video codec and format
4. **Quality settings**: Configurable bitrate and resolution
5. **Preview**: Show preview before saving

## Troubleshooting

### "Failed to create ScreenCast session"
- Check if PipeWire is running
- Verify portal is available: `flatpak run --command=busctl net.bloupla.simpleshot`
- Check journal logs: `journalctl --user -xe`

### "Screenshot failed" or blank images
- Ensure gstreamer or ffmpeg has PipeWire support
- Check PipeWire node is accessible
- Try running outside sandbox for testing

### Recording produces empty file
- Verify ffmpeg has `--enable-libpipewire`
- Check PipeWire node ID is valid
- Monitor ffmpeg stderr for errors

## References
- [ScreenCast Portal Documentation](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.ScreenCast.html)
- [PipeWire Documentation](https://docs.pipewire.org/)
- [FFmpeg PipeWire Support](https://trac.ffmpeg.org/wiki/Capture/PipeWire)

