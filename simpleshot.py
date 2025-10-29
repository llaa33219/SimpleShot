#!/usr/bin/env python3
"""
SimpleShot - A simple screen capture and recording tool
Uses org.freedesktop.portal.ScreenCast for all capture functionality
"""

import sys
import os
import gi
import subprocess
import json
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


class ScreenCastSession:
    """Manages a ScreenCast portal session"""
    
    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.session_handle = None
        self.session_token = None
        self.request_token_counter = 0
        self.pipewire_node = None
        self.pipewire_fd = None
        self.is_recording = False
        self.recording_process = None
        self.recording_filepath = None
        self.screenshot_callback = None
        
        # D-Bus proxies
        self.portal = None
        self.session_proxy = None
        
        # Generate unique sender token
        import random
        self.sender_token = f"simpleshot{random.randint(100000, 999999)}"
        
    def _get_request_token(self):
        """Generate unique request token"""
        self.request_token_counter += 1
        return f"request{self.request_token_counter}"
    
    def _get_session_token(self):
        """Generate unique session token"""
        if not self.session_token:
            import random
            self.session_token = f"session{random.randint(100000, 999999)}"
        return self.session_token
    
    def start_session(self, callback=None):
        """Start a new ScreenCast session"""
        try:
            # Connect to ScreenCast portal
            self.portal = Gio.DBusProxy.new_for_bus_sync(
                Gio.BusType.SESSION,
                Gio.DBusProxyFlags.NONE,
                None,
                'org.freedesktop.portal.Desktop',
                '/org/freedesktop/portal/desktop',
                'org.freedesktop.portal.ScreenCast',
                None
            )
            
            # Create session
            request_token = self._get_request_token()
            session_token = self._get_session_token()
            
            options = {
                'handle_token': GLib.Variant('s', request_token),
                'session_handle_token': GLib.Variant('s', session_token)
            }
            
            # Subscribe to Request signal
            self._subscribe_to_request(request_token, self._on_create_session_response, callback)
            
            # Call CreateSession
            self.portal.call(
                'CreateSession',
                GLib.Variant('(a{sv})', (options,)),
                Gio.DBusCallFlags.NONE,
                -1,
                None,
                None,
                None
            )
            
        except Exception as e:
            print(f"Error starting ScreenCast session: {e}")
            if callback:
                callback(False)
    
    def _subscribe_to_request(self, request_token, handler, user_data=None):
        """Subscribe to portal Request signal"""
        request_path = f"/org/freedesktop/portal/desktop/request/{self.sender_token}/{request_token}"
        
        connection = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        connection.signal_subscribe(
            'org.freedesktop.portal.Desktop',
            'org.freedesktop.portal.Request',
            'Response',
            request_path,
            None,
            Gio.DBusSignalFlags.NONE,
            lambda conn, sender, path, iface, signal, params: handler(params, user_data),
            None
        )
    
    def _on_create_session_response(self, parameters, callback):
        """Handle CreateSession response"""
        response = parameters.get_child_value(0).get_uint32()
        results = parameters.get_child_value(1)
        
        if response != 0:
            print(f"CreateSession failed with response: {response}")
            if callback:
                callback(False)
            return
        
        # Get session handle
        session_variant = results.lookup_value('session_handle', None)
        if session_variant:
            self.session_handle = session_variant.get_string()
            print(f"Session created: {self.session_handle}")
            
            # Next step: select sources
            self._select_sources(callback)
        else:
            print("No session handle returned")
            if callback:
                callback(False)
    
    def _select_sources(self, callback):
        """Select sources for screen casting"""
        try:
            request_token = self._get_request_token()
            
            options = {
                'handle_token': GLib.Variant('s', request_token),
                'types': GLib.Variant('u', 1 | 2),  # MONITOR | WINDOW
                'multiple': GLib.Variant('b', False),
                'cursor_mode': GLib.Variant('u', 2)  # Embedded
            }
            
            # Subscribe to Request signal
            self._subscribe_to_request(request_token, self._on_select_sources_response, callback)
            
            # Call SelectSources
            self.portal.call(
                'SelectSources',
                GLib.Variant('(oa{sv})', (self.session_handle, options)),
                Gio.DBusCallFlags.NONE,
                -1,
                None,
                None,
                None
            )
            
        except Exception as e:
            print(f"Error selecting sources: {e}")
            if callback:
                callback(False)
    
    def _on_select_sources_response(self, parameters, callback):
        """Handle SelectSources response"""
        response = parameters.get_child_value(0).get_uint32()
        
        if response != 0:
            print(f"SelectSources failed with response: {response}")
            if callback:
                callback(False)
            return
        
        print("Sources selected")
        # Next step: start the cast
        self._start_cast(callback)
    
    def _start_cast(self, callback):
        """Start the screen cast"""
        try:
            request_token = self._get_request_token()
            
            options = {
                'handle_token': GLib.Variant('s', request_token)
            }
            
            # Subscribe to Request signal
            self._subscribe_to_request(request_token, self._on_start_response, callback)
            
            # Call Start
            self.portal.call(
                'Start',
                GLib.Variant('(osa{sv})', (self.session_handle, '', options)),
                Gio.DBusCallFlags.NONE,
                -1,
                None,
                None,
                None
            )
            
        except Exception as e:
            print(f"Error starting cast: {e}")
            if callback:
                callback(False)
    
    def _on_start_response(self, parameters, callback):
        """Handle Start response"""
        response = parameters.get_child_value(0).get_uint32()
        results = parameters.get_child_value(1)
        
        if response != 0:
            print(f"Start failed with response: {response}")
            if callback:
                callback(False)
            return
        
        # Get streams information
        streams_variant = results.lookup_value('streams', None)
        if streams_variant:
            streams = streams_variant.unpack()
            if streams:
                # Get the first stream
                node_id, properties = streams[0]
                self.pipewire_node = node_id
                print(f"PipeWire node ID: {self.pipewire_node}")
                
                # Open PipeWire remote
                self._open_pipewire_remote(callback)
            else:
                print("No streams available")
                if callback:
                    callback(False)
        else:
            print("No streams returned")
            if callback:
                callback(False)
    
    def _open_pipewire_remote(self, callback):
        """Open PipeWire remote for the session"""
        try:
            # Call OpenPipeWireRemote
            self.portal.call(
                'OpenPipeWireRemote',
                GLib.Variant('(oa{sv})', (self.session_handle, {})),
                Gio.DBusCallFlags.NONE,
                -1,
                None,
                lambda proxy, result, data: self._on_pipewire_remote_opened(proxy, result, callback),
                None
            )
            
        except Exception as e:
            print(f"Error opening PipeWire remote: {e}")
            if callback:
                callback(False)
    
    def _on_pipewire_remote_opened(self, proxy, result, callback):
        """Handle OpenPipeWireRemote response"""
        try:
            res = proxy.call_finish(result)
            if res:
                fd_list = res.get_child_value(0)
                # The file descriptor is returned as UnixFDList
                # We'll use the node ID directly with gstreamer/ffmpeg
                print("PipeWire remote opened successfully")
                
                if callback:
                    callback(True)
        except Exception as e:
            print(f"Error processing PipeWire remote: {e}")
            if callback:
                callback(False)
    
    def take_screenshot(self, save_path, callback=None):
        """Take a screenshot using the ScreenCast session"""
        if not self.pipewire_node:
            print("No active ScreenCast session")
            if callback:
                callback(False, None)
            return
        
        try:
            # Use gstreamer to capture a single frame
            cmd = [
                'gst-launch-1.0',
                '-q',
                f'pipewiresrc path={self.pipewire_node}',
                '!', 'videoconvert',
                '!', 'pngenc',
                '!', f'filesink location={save_path}',
                'num-buffers=1'
            ]
            
            # Try gstreamer first
            result = subprocess.run(cmd, capture_output=True, timeout=5)
            
            if result.returncode == 0:
                print(f"Screenshot saved: {save_path}")
                if callback:
                    callback(True, save_path)
            else:
                # Fallback to ffmpeg
                self._screenshot_with_ffmpeg(save_path, callback)
                
        except FileNotFoundError:
            # Try ffmpeg if gstreamer not available
            self._screenshot_with_ffmpeg(save_path, callback)
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            if callback:
                callback(False, None)
    
    def _screenshot_with_ffmpeg(self, save_path, callback):
        """Take screenshot using ffmpeg"""
        try:
            cmd = [
                'ffmpeg',
                '-f', 'pipewire',
                '-i', str(self.pipewire_node),
                '-frames:v', '1',
                '-y',
                save_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=5)
            
            if result.returncode == 0:
                print(f"Screenshot saved with ffmpeg: {save_path}")
                if callback:
                    callback(True, save_path)
            else:
                print(f"ffmpeg failed: {result.stderr.decode()}")
                if callback:
                    callback(False, None)
                    
        except Exception as e:
            print(f"Error with ffmpeg screenshot: {e}")
            if callback:
                callback(False, None)
    
    def start_recording(self, filepath):
        """Start recording using the ScreenCast session"""
        if not self.pipewire_node:
            print("No active ScreenCast session")
            return False
        
        if self.is_recording:
            print("Already recording")
            return False
        
        try:
            self.recording_filepath = filepath
            
            # Use ffmpeg to record from PipeWire
            cmd = [
                'ffmpeg',
                '-f', 'pipewire',
                '-i', str(self.pipewire_node),
                '-c:v', 'libvpx-vp9',
                '-b:v', '2M',
                '-crf', '30',
                '-y',
                filepath
            ]
            
            self.recording_process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            self.is_recording = True
            print(f"Recording started: {filepath}")
            return True
            
        except Exception as e:
            print(f"Error starting recording: {e}")
            return False
    
    def stop_recording(self):
        """Stop the current recording"""
        if not self.is_recording or not self.recording_process:
            return False
        
        try:
            # Send SIGINT to ffmpeg for clean shutdown
            self.recording_process.terminate()
            self.recording_process.wait(timeout=10)
            
            print(f"Recording saved: {self.recording_filepath}")
            self.is_recording = False
            return True
            
        except Exception as e:
            print(f"Error stopping recording: {e}")
            # Force kill if terminate fails
            try:
                self.recording_process.kill()
            except:
                pass
            self.is_recording = False
            return False
    
    def close_session(self):
        """Close the ScreenCast session"""
        if self.is_recording:
            self.stop_recording()
        
        # The session will be automatically closed when the app exits
        # or we can explicitly call the Close method if needed
        self.session_handle = None
        self.pipewire_node = None


class SelectionWindow(Gtk.Window):
    """Fullscreen overlay for area selection"""
    
    def __init__(self, app, config, manager, monitor, screencast_session):
        super().__init__(application=app)
        self.config = config
        self.manager = manager
        self.monitor = monitor
        self.screencast_session = screencast_session
        
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
        """Take a screenshot using ScreenCast"""
        x = int(min(self.start_x, self.end_x))
        y = int(min(self.start_y, self.end_y))
        w = int(abs(self.end_x - self.start_x))
        h = int(abs(self.end_y - self.start_y))
        
        if w < 10 or h < 10:
            return
        
        self.manager.hide_all_selection_windows()
        
        # Generate temporary filename
        temp_path = os.path.join('/tmp', f'simpleshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
        
        # Take screenshot using ScreenCast session
        self.screencast_session.take_screenshot(temp_path, 
            lambda success, path: self.on_screenshot_taken(success, path, x, y, w, h))
    
    def on_screenshot_taken(self, success, temp_path, sel_x, sel_y, sel_w, sel_h):
        """Handle screenshot completion"""
        if not success or not temp_path or not os.path.exists(temp_path):
            self.show_notification("Screenshot failed")
            self.manager.end_capture_session()
            return
        
        try:
            # Load the full screenshot
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(temp_path)
            
            # Get monitor geometry for cropping
            monitor_geometry = self.monitor.get_geometry()
            scale = self.monitor.get_scale_factor()
            
            # Calculate crop coordinates (in physical pixels)
            # Note: ScreenCast gives us full screen, need to crop to selection
            crop_x = (sel_x + monitor_geometry.x) * scale
            crop_y = (sel_y + monitor_geometry.y) * scale
            crop_w = sel_w * scale
            crop_h = sel_h * scale
            
            # Ensure coordinates are within bounds
            img_width = pixbuf.get_width()
            img_height = pixbuf.get_height()
            
            crop_x = max(0, min(crop_x, img_width - 1))
            crop_y = max(0, min(crop_y, img_height - 1))
            crop_w = min(crop_w, img_width - crop_x)
            crop_h = min(crop_h, img_height - crop_y)
            
            # Crop to selected area
            cropped_pixbuf = pixbuf.new_subpixbuf(int(crop_x), int(crop_y), int(crop_w), int(crop_h))
            
            # Save to final location
            Path(self.config.picture_dir).mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"screenshot_{timestamp}.png"
            save_path = os.path.join(self.config.picture_dir, filename)
            
            cropped_pixbuf.savev(save_path, "png", [], [])
            
            self.show_notification(f"Screenshot saved")
            self.copy_to_clipboard(save_path)
            
            # Clean up temp file
            try:
                os.remove(temp_path)
            except:
                pass
                
        except Exception as e:
            print(f"Error processing screenshot: {e}")
            self.show_notification("Error saving screenshot")
        
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
        """Start screen recording using ScreenCast"""
        x = int(min(self.start_x, self.end_x))
        y = int(min(self.start_y, self.end_y))
        w = int(abs(self.end_x - self.start_x))
        h = int(abs(self.end_y - self.start_y))
        
        if w < 10 or h < 10:
            return
        
        # Note: We're recording the full screen via ScreenCast
        # Area selection is currently for visual feedback only
        # TODO: Implement cropping for recordings if needed
        
        try:
            # Create output directory
            Path(self.config.video_dir).mkdir(parents=True, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"recording_{timestamp}.webm"
            filepath = os.path.join(self.config.video_dir, filename)
            
            # Start recording via ScreenCast session
            if self.screencast_session.start_recording(filepath):
                self.is_recording = True
                self.drawing_area.queue_draw()
                self.show_notification("Recording started")
            else:
                self.show_notification("Failed to start recording")
                
        except Exception as e:
            print(f"Error starting recording: {e}")
            self.show_notification("Error starting recording")

    def stop_recording(self):
        """Stop screen recording"""
        if self.is_recording:
            if self.screencast_session.stop_recording():
                self.show_notification("Recording saved")
            else:
                self.show_notification("Error stopping recording")
        
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
        self.screencast_session = None
    
    def do_activate(self):
        """Application activation"""
        if not self.settings_window:
            self.settings_window = SettingsWindow(self, self.config)
        self.settings_window.present()

    def start_capture_session(self, settings_win):
        """Create ScreenCast session and selection windows on all monitors"""
        self.settings_window = settings_win
        
        # Create ScreenCast session
        self.screencast_session = ScreenCastSession(self, self.config)
        
        # Start the session, then show selection UI
        self.screencast_session.start_session(self._on_screencast_ready)
    
    def _on_screencast_ready(self, success):
        """Called when ScreenCast session is ready"""
        if not success:
            print("Failed to create ScreenCast session")
            if self.settings_window:
                self.settings_window.present()
            # Show error notification
            notification = Gio.Notification.new("SimpleShot")
            notification.set_body("Failed to initialize screen capture. Please try again.")
            self.send_notification(None, notification)
            return
        
        print("ScreenCast session ready, showing selection UI")
        
        # Create selection windows on all monitors
        display = Gdk.Display.get_default()
        monitors = display.get_monitors()
        
        for i in range(monitors.get_n_items()):
            monitor = monitors.get_item(i)
            win = SelectionWindow(self, self.config, self, monitor, self.screencast_session)
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
        
        # Close ScreenCast session
        if self.screencast_session:
            self.screencast_session.close_session()
            self.screencast_session = None
        
        if self.settings_window:
            self.settings_window.present()


def main():
    """Main entry point"""
    app = SimpleShotApp()
    return app.run(sys.argv)


if __name__ == '__main__':
    sys.exit(main())












