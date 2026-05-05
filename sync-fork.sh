#!/bin/bash
# =============================================================================
# Alasmia Fork Sync Script - Complete Clean Reset
# =============================================================================
# Run this if you have an old fork and want a 100% clean sync
# WARNING: This DELETES all your local commits permanently
# =============================================================================

echo "🔄 Alasmia Fork Sync Script"
echo "============================================"
echo ""
echo "⚠️  WARNING: This will DELETE all your local commits!"
echo "   Your fork will match the official repo exactly."
echo ""
read -p "Continue? (type 'YES' to confirm): " confirm

if [ "$confirm" != "YES" ]; then
    echo "Cancelled."
    exit 1
fi

# Check if we're in an alasmia repo
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository."
    echo "   Run this from your Alasmia fork folder."
    exit 1
fi

echo ""
echo "📡 Adding official repo as upstream..."
git remote add upstream https://github.com/alasmia/Alasmia.git 2>/dev/null || echo "   upstream already exists"

echo "📥 Fetching latest clean version..."
git fetch upstream

echo "💾 Creating backup branch..."
git branch backup-before-sync

echo "🔄 Resetting to official version..."
git reset --hard upstream/main

echo ""
echo "✅ SYNC COMPLETE!"
echo ""
echo "Your fork is now 100% clean with the official repo."
echo "Backup saved in branch: backup-before-sync"
echo ""
echo "To update your GitHub fork, run:"
echo "   git push --force origin main"
echo ""
