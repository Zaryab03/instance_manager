#!/bin/bash

# Instance Manager Installation Script
# This script installs and configures the Instance Manager app

set -e

SITE_NAME="${1:-demo.zq.com}"
BENCH_DIR="/home/zaryab/version-15"
PYTHON_BIN="$BENCH_DIR/env/bin/python"

echo "========================================="
echo "Instance Manager - Installation Script"
echo "========================================="
echo ""

# Check if bench directory exists
if [ ! -d "$BENCH_DIR" ]; then
    echo "❌ Error: Bench directory not found at $BENCH_DIR"
    exit 1
fi

cd "$BENCH_DIR"

# Check if app exists
if [ ! -d "apps/instance_manager" ]; then
    echo "❌ Error: instance_manager app not found at apps/instance_manager"
    exit 1
fi

if [ ! -x "$PYTHON_BIN" ]; then
    echo "❌ Error: Bench Python not found at $PYTHON_BIN"
    exit 1
fi

echo "✓ Bench directory found: $BENCH_DIR"
echo "✓ App directory found: apps/instance_manager"
echo "✓ Bench Python found: $PYTHON_BIN"
echo ""

# Step 1: Install Python package into bench environment
echo "Step 1: Installing Python package into bench environment..."
"$PYTHON_BIN" -m pip install --force-reinstall --no-build-isolation "$BENCH_DIR/apps/instance_manager"
echo "✓ Python package installed"
echo ""

# Step 2: Install app
echo "Step 2: Installing app on site: $SITE_NAME"
bench --site "$SITE_NAME" install-app instance_manager
echo "✓ App installed"
echo ""

# Step 3: Migrate
echo "Step 3: Running migrations..."
bench --site "$SITE_NAME" migrate
echo "✓ Migrations complete"
echo ""

# Step 4: Build
echo "Step 4: Building assets..."
bench build
echo "✓ Assets built"
echo ""

# Step 5: Clear cache
echo "Step 5: Clearing cache..."
bench --site "$SITE_NAME" clear-cache
echo "✓ Cache cleared"
echo ""

echo "========================================="
echo "✓ Installation Complete!"
echo "========================================="
echo ""
echo "Next Steps:"
echo "1. Go to Awesome Bar (Ctrl+K)"
echo "2. Search for 'Instance Settings'"
echo "3. Create a new Instance Settings document"
echo "4. Configure your limits and expiry date"
echo "5. Save the document"
echo ""
echo "The homepage expiry bar will appear on all pages"
echo "when license expires within 30 days."
echo ""
echo "Documentation:"
echo "  - README.md - Quick reference"
echo "  - SETUP_GUIDE.md - Detailed guide"
echo "  - COMPLETE_SUMMARY.md - Full overview"
echo ""
