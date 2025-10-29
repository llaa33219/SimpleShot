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
        self.get_application().start_capture_session(self)
        self.set_visible(False)


class SelectionWindow(Gtk.Window):
    """Fullscreen overlay for area selection"""
    
    def __init__(self, app, config, manager, monitor):
        super().__init__(application=app)
        self.config = config
        self.manager = manager
        self.monitor = monitor
        
        # Window setup
        self.set_decorated(False)
        
        display = Gdk.Display.get_default()
        seat = display.get_default_seat()
        pointer = seat.get_pointer()
        
        monitor = display.get_monitor_at_surface(pointer.get_surface_at_position()[0])
        self.fullscreen_on_monitor(monitor)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"window { background-color: transparent; }")
        Gtk.StyleContext.add_provider_for_display(display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

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
        menu_x = sel_x + (sel_w / 2) - (menu_width / 2)
        menu_y = sel_y + sel_h + 20

        # position menu inside selection rectangle if it goes off screen
        if menu_y + menu_height > screen_h:
            menu_y = sel_y - menu_height - 20
        
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
            self.end_x = x
            self.end_y = y
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
            self.manager.end_capture_session()
            return True
        return False
    
    def take_screenshot(self):
        """Take a screenshot of selected area using XDG Portal"""
        x = int(min(self.start_x, self.end_x))
        y = int(min(self.start_y, self.end_y))
        w = int(abs(self.end_x - self.start_x))
        h = int(abs(self.end_y - self.start_y))
        
        if w < 10 or h < 10:
            return
        
        self.manager.hide_all_selection_windows()

        try:
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
            
            options = {
                'interactive': GLib.Variant('b', False),
                'modal': GLib.Variant('b', True)
            }
            
            portal.call(
                'Screenshot',
                GLib.Variant('(sa{sv})', ('', options)),
                Gio.DBusCallFlags.NONE,
                -1,
                None,
                self.on_screenshot_finish,
                None
            )
            
        except Exception as e:
            print(f"Error taking screenshot via portal: {e}")
            self.manager.end_capture_session()

    def on_screenshot_finish(self, proxy, result, user_data):
        try:
            res = proxy.call_finish(result)
            if res:
                handle = res.get_child_value(0).get_string()
                
                # Get request proxy and connect to Response signal
                request_proxy = Gio.DBusProxy.new_for_bus_sync(
                    Gio.BusType.SESSION,
                    Gio.DBusProxyFlags.NONE,
                    None,
                    'org.freedesktop.portal.Desktop',
                    handle,
                    'org.freedesktop.portal.Request',
                    None
                )
                request_proxy.connect("g-signal", self.on_portal_response)
        except Exception as e:
            print(f"Error processing screenshot result: {e}")
            self.manager.end_capture_session()

    def on_portal_response(self, proxy, sender_name, signal_name, parameters):
        if signal_name == 'Response':
            response = parameters.get_child_value(1)
            uri_variant = response.lookup_value('uri')
            if uri_variant:
                uri = uri_variant.get_string().replace('file://', '')
                
                monitor_geometry = self.monitor.get_geometry()
                scale = self.monitor.get_scale_factor()
                
                # Crop the full screenshot using physical pixels
                x = (int(min(self.start_x, self.end_x)) + monitor_geometry.x) * scale
                y = (int(min(self.start_y, self.end_y)) + monitor_geometry.y) * scale
                w = int(abs(self.end_x - self.start_x)) * scale
                h = int(abs(self.end_y - self.start_y)) * scale
                
                try:
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file(uri)
                    cropped_pixbuf = pixbuf.new_subpixbuf(x, y, w, h)
                    
                    # Save the cropped image
                    Path(self.config.picture_dir).mkdir(parents=True, exist_ok=True)
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    filename = f"screenshot_{timestamp}.png"
                    save_path = os.path.join(self.config.picture_dir, filename)
                    
                    cropped_pixbuf.savev(save_path, "png", [], [])
                    
                    self.show_notification(f"Screenshot saved to {save_path}")
                    self.copy_to_clipboard(save_path)
                    
                    # Clean up the original full screenshot
                    os.remove(uri)
                    
                except Exception as e:
                    print(f"Error cropping screenshot: {e}")
                    self.show_notification("Error processing screenshot.")

            else:
                self.show_notification("Screenshot cancelled.")
            
            self.manager.end_capture_session()
    
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
        """Start screen recording using bundled ffmpeg"""
        x = int(min(self.start_x, self.end_x))
        y = int(min(self.start_y, self.end_y))
        w = int(abs(self.end_x - self.start_x))
        h = int(abs(self.end_y - self.start_y))
        
        if w < 10 or h < 10:
            return
            
        self.manager.hide_all_selection_windows()
        
        try:
            # Create output directory
            Path(self.config.video_dir).mkdir(parents=True, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"recording_{timestamp}.webm"
            self.recording_filepath = os.path.join(self.config.video_dir, filename)
            
            # Use ffmpeg for X11
            import subprocess
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
            
        except FileNotFoundError:
            print("ffmpeg not found. Make sure it is bundled with the Flatpak.")
            self.show_notification("Error: ffmpeg not found.")
        except Exception as e:
            print(f"Error starting recording: {e}")

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
        self.manager.end_capture_session()
    
    def close_window(self):
        """Close selection window and show settings again"""
        self.manager.end_capture_session()


class SimpleShotApp(Adw.Application):
    """Main application class"""
    
    def __init__(self):
        super().__init__(application_id='net.bloupla.simpleshot',
                        flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.config = SimpleShotConfig()
        self.selection_windows = []
        self.settings_window = None
    
    def do_activate(self):
        """Application activation"""
        if not self.settings_window:
            self.settings_window = SettingsWindow(self, self.config)
        self.settings_window.present()

    def start_capture_session(self, settings_win):
        """Create selection windows on all monitors"""
        self.settings_window = settings_win
        display = Gdk.Display.get_default()
        monitors = display.get_monitors()
        
        for i in range(monitors.get_n_items()):
            monitor = monitors.get_item(i)
            win = SelectionWindow(self, self.config, self, monitor)
            win.fullscreen_on_monitor(monitor)
            win.present()
            self.selection_windows.append(win)

    def hide_all_selection_windows(self):
        """Hide all selection windows"""
        for win in self.selection_windows:
            win.set_visible(False)

    def end_capture_session(self):
        """Close all selection windows and show the main window"""
        for win in self.selection_windows:
            win.close()
        self.selection_windows = []
        
        if self.settings_window:
            self.settings_window.present()


def main():
    """Main entry point"""
    app = SimpleShotApp()
    return app.run(sys.argv)


if __name__ == '__main__':
    sys.exit(main())

