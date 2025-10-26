#!/usr/bin/env python3
"""
SimpleShot - A simple screen capture and recording tool
Uses XDG Portals for screenshot and screencast functionality
"""

import sys
import os
import gi
from datetime import datetime
from pathlib import Path

gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw, GLib, Gio, GdkPixbuf

class SimpleShotConfig:
    """Configuration manager for SimpleShot"""
    
    def __init__(self):
        self.config_dir = Path.home() / '.var' / 'app' / 'net.bloupla.simpleshot' / 'config'
        self.config_file = self.config_dir / 'settings.conf'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Default save locations
        self.picture_dir = str(Path.home() / 'Pictures' / 'Screenshots')
        self.video_dir = str(Path.home() / 'Videos' / 'Recordings')
        
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    for line in f:
                        key, value = line.strip().split('=', 1)
                        if key == 'picture_dir':
                            self.picture_dir = value
                        elif key == 'video_dir':
                            self.video_dir = value
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                f.write(f"picture_dir={self.picture_dir}\n")
                f.write(f"video_dir={self.video_dir}\n")
        except Exception as e:
            print(f"Error saving config: {e}")


class SettingsWindow(Adw.ApplicationWindow):
    """Main settings window for SimpleShot"""
    
    def __init__(self, app, config):
        super().__init__(application=app)
        self.config = config
        self.set_title("SimpleShot")
        self.set_default_size(500, 400)
        
        # Create main box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        # Header bar
        header = Adw.HeaderBar()
        main_box.append(header)
        
        # Content
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        content_box.set_margin_top(20)
        content_box.set_margin_bottom(20)
        content_box.set_margin_start(20)
        content_box.set_margin_end(20)
        
        # Title
        title = Gtk.Label(label="SimpleShot")
        title.add_css_class("title-1")
        content_box.append(title)
        
        subtitle = Gtk.Label(label="Screen Capture & Recording")
        subtitle.add_css_class("dim-label")
        content_box.append(subtitle)
        
        # Settings group
        settings_group = Adw.PreferencesGroup()
        settings_group.set_title("Settings")
        
        # Picture directory row
        picture_row = Adw.ActionRow()
        picture_row.set_title("Screenshots Location")
        picture_row.set_subtitle(self.config.picture_dir)
        picture_button = Gtk.Button(label="Choose")
        picture_button.set_valign(Gtk.Align.CENTER)
        picture_button.connect("clicked", self.on_choose_picture_dir)
        picture_row.add_suffix(picture_button)
        settings_group.add(picture_row)
        self.picture_row = picture_row
        
        # Video directory row
        video_row = Adw.ActionRow()
        video_row.set_title("Recordings Location")
        video_row.set_subtitle(self.config.video_dir)
        video_button = Gtk.Button(label="Choose")
        video_button.set_valign(Gtk.Align.CENTER)
        video_button.connect("clicked", self.on_choose_video_dir)
        video_row.add_suffix(video_button)
        settings_group.add(video_row)
        self.video_row = video_row
        
        content_box.append(settings_group)
        
        # Start button
        start_button = Gtk.Button(label="Start Capture")
        start_button.add_css_class("suggested-action")
        start_button.add_css_class("pill")
        start_button.set_size_request(200, 50)
        start_button.set_halign(Gtk.Align.CENTER)
        start_button.connect("clicked", self.on_start_capture)
        content_box.append(start_button)
        
        # Command info
        info_label = Gtk.Label()
        info_label.set_markup('<span size="small">Command: <tt>flatpak run net.bloupla.simpleshot</tt></span>')
        info_label.add_css_class("dim-label")
        content_box.append(info_label)
        
        main_box.append(content_box)
        self.set_content(main_box)
    
    def on_choose_picture_dir(self, button):
        """Open directory chooser for pictures"""
        dialog = Gtk.FileDialog()
        dialog.set_title("Choose Screenshots Location")
        dialog.select_folder(None, None, self.on_picture_dir_selected)
    
    def on_picture_dir_selected(self, dialog, result):
        """Handle picture directory selection"""
        try:
            folder = dialog.select_folder_finish(result)
            if folder:
                path = folder.get_path()
                self.config.picture_dir = path
                self.picture_row.set_subtitle(path)
                self.config.save_config()
        except Exception as e:
            print(f"Error selecting folder: {e}")
    
    def on_choose_video_dir(self, button):
        """Open directory chooser for videos"""
        dialog = Gtk.FileDialog()
        dialog.set_title("Choose Recordings Location")
        dialog.select_folder(None, None, self.on_video_dir_selected)
    
    def on_video_dir_selected(self, dialog, result):
        """Handle video directory selection"""
        try:
            folder = dialog.select_folder_finish(result)
            if folder:
                path = folder.get_path()
                self.config.video_dir = path
                self.video_row.set_subtitle(path)
                self.config.save_config()
        except Exception as e:
            print(f"Error selecting folder: {e}")
    
    def on_start_capture(self, button):
        """Start the capture selection interface"""
        self.hide()
        # Launch selection window
        selection_win = SelectionWindow(self.get_application(), self.config)
        selection_win.present()


class SelectionWindow(Gtk.Window):
    """Fullscreen overlay for area selection"""
    
    def __init__(self, app, config):
        super().__init__(application=app)
        self.config = config
        
        # Window setup
        self.set_decorated(False)
        self.fullscreen()
        
        # Selection state
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.is_selecting = False
        self.is_recording = False
        
        # Drawing area
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_draw_func(self.on_draw)
        self.set_child(self.drawing_area)
        
        # Event controllers
        # Mouse press
        press_gesture = Gtk.GestureClick()
        press_gesture.connect("pressed", self.on_mouse_press)
        self.drawing_area.add_controller(press_gesture)
        
        # Mouse release
        release_gesture = Gtk.GestureClick()
        release_gesture.connect("released", self.on_mouse_release)
        self.drawing_area.add_controller(release_gesture)
        
        # Mouse motion
        motion_controller = Gtk.EventControllerMotion()
        motion_controller.connect("motion", self.on_mouse_motion)
        self.drawing_area.add_controller(motion_controller)
        
        # Keyboard
        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self.on_key_press)
        self.add_controller(key_controller)
        
        # Screenshot via portal
        self.portal = None
    
    def on_draw(self, area, cr, width, height):
        """Draw the selection overlay"""
        # Semi-transparent dark overlay
        cr.set_source_rgba(0, 0, 0, 0.5)
        cr.paint()
        
        if self.is_selecting or (self.end_x != 0 and self.end_y != 0):
            # Clear selected area
            x = min(self.start_x, self.end_x)
            y = min(self.start_y, self.end_y)
            w = abs(self.end_x - self.start_x)
            h = abs(self.end_y - self.start_y)
            
            # Clear rectangle (show through)
            cr.set_operator(0)  # OPERATOR_CLEAR
            cr.rectangle(x, y, w, h)
            cr.fill()
            
            # Draw border
            cr.set_operator(2)  # OPERATOR_OVER
            if self.is_recording:
                cr.set_source_rgb(1, 0, 0)  # Red for recording
                cr.set_line_width(4)
            else:
                cr.set_source_rgb(0.3, 0.6, 1)  # Blue
                cr.set_line_width(2)
            cr.rectangle(x, y, w, h)
            cr.stroke()
            
            # Draw menu if selection is complete
            if not self.is_selecting and w > 50 and h > 50:
                self.draw_menu(cr, width, height, x, y, w, h)
    
    def draw_menu(self, cr, screen_w, screen_h, sel_x, sel_y, sel_w, sel_h):
        """Draw the action menu"""
        # Menu dimensions
        menu_width = 200
        menu_height = 60
        menu_x = (screen_w - menu_width) / 2
        menu_y = screen_h - menu_height - 40
        
        # Menu background
        cr.set_source_rgba(0.2, 0.2, 0.2, 0.95)
        self.draw_rounded_rect(cr, menu_x, menu_y, menu_width, menu_height, 10)
        cr.fill()
        
        # Menu border
        cr.set_source_rgb(0.4, 0.4, 0.4)
        cr.set_line_width(1)
        self.draw_rounded_rect(cr, menu_x, menu_y, menu_width, menu_height, 10)
        cr.stroke()
        
        # Buttons
        button_size = 40
        spacing = 20
        
        # Capture button (camera icon)
        capture_x = menu_x + 40
        capture_y = menu_y + 10
        cr.set_source_rgb(0.3, 0.6, 1)
        cr.arc(capture_x + button_size/2, capture_y + button_size/2, button_size/2, 0, 2 * 3.14159)
        cr.fill()
        
        # Camera icon
        cr.set_source_rgb(1, 1, 1)
        cr.arc(capture_x + button_size/2, capture_y + button_size/2, 10, 0, 2 * 3.14159)
        cr.fill()
        
        # Record button (red dot icon)
        record_x = menu_x + 40 + button_size + spacing
        record_y = menu_y + 10
        if self.is_recording:
            cr.set_source_rgb(0.5, 0.5, 0.5)  # Gray when recording
        else:
            cr.set_source_rgb(1, 0.2, 0.2)  # Red
        cr.arc(record_x + button_size/2, record_y + button_size/2, button_size/2, 0, 2 * 3.14159)
        cr.fill()
        
        # Record icon
        cr.set_source_rgb(1, 1, 1)
        if self.is_recording:
            # Stop square
            cr.rectangle(record_x + button_size/2 - 8, record_y + button_size/2 - 8, 16, 16)
        else:
            # Record circle
            cr.arc(record_x + button_size/2, record_y + button_size/2, 10, 0, 2 * 3.14159)
        cr.fill()
        
        # Store button positions for click detection
        self.capture_button = (capture_x, capture_y, button_size, button_size)
        self.record_button = (record_x, record_y, button_size, button_size)
    
    def draw_rounded_rect(self, cr, x, y, width, height, radius):
        """Draw a rounded rectangle"""
        cr.arc(x + radius, y + radius, radius, 3.14159, 3 * 3.14159 / 2)
        cr.arc(x + width - radius, y + radius, radius, 3 * 3.14159 / 2, 0)
        cr.arc(x + width - radius, y + height - radius, radius, 0, 3.14159 / 2)
        cr.arc(x + radius, y + height - radius, radius, 3.14159 / 2, 3.14159)
        cr.close_path()
    
    def on_mouse_press(self, gesture, n_press, x, y):
        """Handle mouse press"""
        if not self.is_selecting and self.end_x != 0:
            # Check if clicking on menu buttons
            if hasattr(self, 'capture_button'):
                bx, by, bw, bh = self.capture_button
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    self.take_screenshot()
                    return
            
            if hasattr(self, 'record_button'):
                bx, by, bw, bh = self.record_button
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    self.toggle_recording()
                    return
            
            # Reset selection
            self.start_x = x
            self.start_y = y
            self.end_x = 0
            self.end_y = 0
        else:
            self.start_x = x
            self.start_y = y
            self.end_x = x
            self.end_y = y
        
        self.is_selecting = True
        self.drawing_area.queue_draw()
    
    def on_mouse_release(self, gesture, n_press, x, y):
        """Handle mouse release"""
        if self.is_selecting:
            self.end_x = x
            self.end_y = y
            self.is_selecting = False
            self.drawing_area.queue_draw()
    
    def on_mouse_motion(self, controller, x, y):
        """Handle mouse motion"""
        if self.is_selecting:
            self.end_x = x
            self.end_y = y
            self.drawing_area.queue_draw()
    
    def on_key_press(self, controller, keyval, keycode, state):
        """Handle keyboard events"""
        if keyval == Gdk.KEY_Escape:
            if self.is_recording:
                self.toggle_recording()  # Stop recording
            self.close_window()
            return True
        return False
    
    def take_screenshot(self):
        """Take a screenshot of selected area using XDG Portal"""
        x = min(self.start_x, self.end_x)
        y = min(self.start_y, self.end_y)
        w = abs(self.end_x - self.start_x)
        h = abs(self.end_y - self.start_y)
        
        if w < 10 or h < 10:
            return
        
        try:
            # Create output directory
            Path(self.config.picture_dir).mkdir(parents=True, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"screenshot_{timestamp}.png"
            self.screenshot_filepath = os.path.join(self.config.picture_dir, filename)
            
            # Use XDG Screenshot Portal
            portal = Gio.DBusProxy.new_for_bus_sync(
                Gio.BusType.SESSION,
                Gio.DBusProxyFlags.NONE,
                None,
                'org.freedesktop.portal.Desktop',
                '/org/freedesktop/portal/desktop',
                'org.freedesktop.portal.Screenshot',
                None
            )
            
            # Request screenshot
            options = {
                'interactive': GLib.Variant('b', False),
                'modal': GLib.Variant('b', True)
            }
            
            result = portal.call_sync(
                'Screenshot',
                GLib.Variant('(ssa{sv})', ('', options)),
                Gio.DBusCallFlags.NONE,
                -1,
                None
            )
            
            if result:
                handle = result[0]
                print(f"Screenshot requested, handle: {handle}")
                # Portal will handle the actual screenshot
                # For now, we'll create a simple notification
                self.show_notification("Screenshot captured")
            
        except Exception as e:
            print(f"Error taking screenshot via portal: {e}")
            # Fallback: try using grim (Wayland) or import (X11)
            self.take_screenshot_fallback()
        
        GLib.timeout_add(500, self.close_window)
    
    def take_screenshot_fallback(self):
        """Fallback screenshot method using grim/import"""
        try:
            import subprocess
            
            x = int(min(self.start_x, self.end_x))
            y = int(min(self.start_y, self.end_y))
            w = int(abs(self.end_x - self.start_x))
            h = int(abs(self.end_y - self.start_y))
            
            # Try grim for Wayland
            try:
                result = subprocess.run([
                    'grim',
                    '-g', f"{x},{y} {w}x{h}",
                    self.screenshot_filepath
                ], capture_output=True, timeout=5)
                
                if result.returncode == 0:
                    self.copy_to_clipboard(self.screenshot_filepath)
                    print(f"Screenshot saved: {self.screenshot_filepath}")
                    return
            except:
                pass
            
            # Try import for X11
            try:
                result = subprocess.run([
                    'import',
                    '-window', 'root',
                    '-crop', f"{w}x{h}+{x}+{y}",
                    self.screenshot_filepath
                ], capture_output=True, timeout=5)
                
                if result.returncode == 0:
                    self.copy_to_clipboard(self.screenshot_filepath)
                    print(f"Screenshot saved: {self.screenshot_filepath}")
                    return
            except:
                pass
                
        except Exception as e:
            print(f"Fallback screenshot failed: {e}")
    
    def copy_to_clipboard(self, filepath):
        """Copy image to clipboard"""
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(filepath)
            clipboard = Gdk.Display.get_default().get_clipboard()
            clipboard.set_texture(Gdk.Texture.new_for_pixbuf(pixbuf))
            print("Copied to clipboard")
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
    
    def show_notification(self, message):
        """Show a notification"""
        notification = Gio.Notification.new("SimpleShot")
        notification.set_body(message)
        self.get_application().send_notification(None, notification)
    
    def toggle_recording(self):
        """Toggle screen recording"""
        if self.is_recording:
            # Stop recording
            self.stop_recording()
        else:
            # Start recording
            self.start_recording()
    
    def start_recording(self):
        """Start screen recording using XDG Screencast Portal"""
        x = min(self.start_x, self.end_x)
        y = min(self.start_y, self.end_y)
        w = abs(self.end_x - self.start_x)
        h = abs(self.end_y - self.start_y)
        
        if w < 10 or h < 10:
            return
        
        try:
            # Create output directory
            Path(self.config.video_dir).mkdir(parents=True, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"recording_{timestamp}.webm"
            self.recording_filepath = os.path.join(self.config.video_dir, filename)
            
            # For simplicity, use fallback recording method
            # Full portal implementation would be more complex
            self.start_recording_fallback()
            
        except Exception as e:
            print(f"Error starting recording: {e}")
    
    def start_recording_fallback(self):
        """Fallback recording using wf-recorder or ffmpeg"""
        try:
            import subprocess
            
            x = int(min(self.start_x, self.end_x))
            y = int(min(self.start_y, self.end_y))
            w = int(abs(self.end_x - self.start_x))
            h = int(abs(self.end_y - self.start_y))
            
            # Try wf-recorder for Wayland
            try:
                self.recording_process = subprocess.Popen([
                    'wf-recorder',
                    '-g', f"{w}x{h}+{x}+{y}",
                    '-f', self.recording_filepath
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                self.is_recording = True
                self.drawing_area.queue_draw()
                print(f"Recording started: {self.recording_filepath}")
                return
            except FileNotFoundError:
                pass
            
            # Try ffmpeg for X11
            try:
                display = os.environ.get('DISPLAY', ':0')
                self.recording_process = subprocess.Popen([
                    'ffmpeg',
                    '-f', 'x11grab',
                    '-s', f"{w}x{h}",
                    '-i', f"{display}+{x},{y}",
                    '-codec:v', 'libvpx',
                    self.recording_filepath
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                self.is_recording = True
                self.drawing_area.queue_draw()
                print(f"Recording started: {self.recording_filepath}")
                return
            except:
                pass
            
            print("No recording tool found (wf-recorder or ffmpeg)")
            
        except Exception as e:
            print(f"Fallback recording failed: {e}")
    
    def stop_recording(self):
        """Stop screen recording"""
        if hasattr(self, 'recording_process') and self.recording_process:
            try:
                self.recording_process.terminate()
                self.recording_process.wait(timeout=5)
                print(f"Recording saved to: {self.recording_filepath}")
                self.show_notification(f"Recording saved")
            except Exception as e:
                print(f"Error stopping recording: {e}")
        
        self.is_recording = False
        self.close_window()
    
    def close_window(self):
        """Close selection window and show settings again"""
        self.close()
        # Reopen settings window
        settings_win = SettingsWindow(self.get_application(), self.config)
        settings_win.present()


class SimpleShotApp(Adw.Application):
    """Main application class"""
    
    def __init__(self):
        super().__init__(application_id='net.bloupla.simpleshot',
                        flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.config = SimpleShotConfig()
    
    def do_activate(self):
        """Application activation"""
        win = SettingsWindow(self, self.config)
        win.present()


def main():
    """Main entry point"""
    app = SimpleShotApp()
    return app.run(sys.argv)


if __name__ == '__main__':
    sys.exit(main())

