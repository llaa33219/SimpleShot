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
if ! flatpak list | grep -q "org.gnome.Platform.*47"; then
    echo "Installing GNOME Platform 47..."
    flatpak install -y flathub org.gnome.Platform//47 org.gnome.Sdk//47
fi

# Clean previous build
if [ -d "build-dir" ]; then
    echo "Cleaning previous build..."
    rm -rf build-dir
fi

# Build
echo "Building Flatpak..."
flatpak-builder --user --install --force-clean build-dir net.bloupla.simpleshot.local.yml

echo ""
echo "=== Build Complete ==="
echo "Run with: flatpak run net.bloupla.simpleshot"

