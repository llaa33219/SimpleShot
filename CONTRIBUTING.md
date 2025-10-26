# Contributing to SimpleShot

Thank you for your interest in contributing to SimpleShot!

## Development Setup

1. Clone the repository
2. Install Flatpak and Flatpak Builder
3. Install GNOME Platform runtime (version 49)
4. Build the application (see BUILDING.md)

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and small

## Making Changes

1. Create a new branch for your feature/fix
2. Make your changes
3. Test thoroughly
4. Ensure the Flatpak builds correctly
5. Submit a pull request

## Testing

Before submitting:

- [ ] Application builds successfully
- [ ] Screenshot feature works
- [ ] Recording feature works
- [ ] Settings are saved correctly
- [ ] UI is responsive
- [ ] No console errors

## Areas for Improvement

Some areas that could use contributions:

### High Priority
- Full XDG Portal implementation (replace fallback methods)
- Better error handling and user feedback
- Add keyboard shortcuts
- Improve recording quality settings

### Medium Priority
- Add annotation tools (arrows, text, shapes)
- Support for delayed capture
- Multiple monitor support improvements
- Video format selection (WebM, MP4)

### Low Priority
- Themes/customization
- Cloud upload integration
- GIF creation from recordings
- History/gallery view

## Portal Implementation

The current implementation uses fallback methods for screenshots and recordings. 
A proper implementation should use:

- `org.freedesktop.portal.Screenshot` for screenshots
- `org.freedesktop.portal.Screencast` for recordings

This would make the application more secure and compatible across different 
desktop environments.

## Reporting Issues

When reporting issues, include:

- Your distribution and version
- Desktop environment (GNOME, KDE, etc.)
- Wayland or X11
- Steps to reproduce
- Expected vs actual behavior
- Any console output

## Questions?

Feel free to open an issue for questions or discussions.

