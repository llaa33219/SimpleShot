#!/bin/bash
# Quick build script for SimpleShot

set -e

echo "=== Building SimpleShot Flatpak ==="

# Check if flatpak-builder is installed
if ! command -v flatpak-builder &> /dev/null; then
    echo "Error: flatpak-builder is not installed"
    echo "Install it with: sudo pacman -S flatpak-builder"
    exit 1
fi

# Check if GNOME runtime is installed
if ! flatpak list | grep -q "org.gnome.Platform.*49"; then
    echo "Installing GNOME Platform 49..."
    flatpak install -y flathub org.gnome.Platform//49 org.gnome.Sdk//49
fi

# Use temp directory for build (GoogleDrive doesn't support symlinks)
BUILD_DIR="/tmp/simpleshot-build"
STATE_DIR="/tmp/simpleshot-flatpak-builder"

# Clean previous build
if [ -d "$BUILD_DIR" ]; then
    echo "Cleaning previous build..."
    rm -rf "$BUILD_DIR"
fi

if [ -d "$STATE_DIR" ]; then
    rm -rf "$STATE_DIR"
fi

# Build
echo "Building Flatpak..."
echo "Build directory: $BUILD_DIR"
echo "State directory: $STATE_DIR"
flatpak-builder --user --install --force-clean --state-dir="$STATE_DIR" "$BUILD_DIR" net.bloupla.simpleshot.local.yml

echo ""
echo "=== Build Complete ==="
echo "Run with: flatpak run net.bloupla.simpleshot"

