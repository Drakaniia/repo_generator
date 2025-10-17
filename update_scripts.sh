#!/bin/bash
# Quick script updater with UTF-8 fixes
# Run: bash update_scripts.sh

echo "================================================"
echo "  Updating Python Scripts with UTF-8 Fixes"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create backups
echo "Creating backups..."
for file in daily_activity.py auto_update.py update_profile.py test_automation.py; do
    if [ -f "$file" ]; then
        cp "$file" "${file}.backup"
        echo -e "  ${GREEN}✓${NC} $file backed up"
    fi
done

echo ""
echo "Files backed up with .backup extension"
echo ""

# Test if scripts run
echo "================================================"
echo "  Testing Scripts"
echo "================================================"
echo ""

# Detect Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
elif command -v py &> /dev/null; then
    PYTHON_CMD=py
else
    echo -e "${RED}✗ Python not found!${NC}"
    exit 1
fi

echo -e "Using: ${GREEN}$PYTHON_CMD${NC}"
echo ""

# Test each script
for script in daily_activity.py auto_update.py update_profile.py; do
    if [ -f "$script" ]; then
        echo "Testing $script..."
        if $PYTHON_CMD "$script" > /dev/null 2>&1; then
            echo -e "  ${GREEN}✓ $script works!${NC}"
        else
            echo -e "  ${YELLOW}⚠ $script has issues (may need manual fix)${NC}"
        fi
    else
        echo -e "  ${RED}✗ $script not found${NC}"
    fi
done

echo ""
echo "================================================"
echo "  Done!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Copy the fixed scripts from the artifacts"
echo "2. Run: $PYTHON_CMD test_automation.py"
echo "3. Commit changes: git add . && git commit -m 'Fix UTF-8 encoding'"
echo ""