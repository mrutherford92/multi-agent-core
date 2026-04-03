#!/bin/bash
# system_cleanup.sh — Safe, comprehensive development cache cleanup
# Usage:
#   ./system_cleanup.sh          # Dry-run: shows what would be deleted
#   ./system_cleanup.sh --run    # Actually deletes caches
#   ./system_cleanup.sh --run --skip-docker  # Skip Docker pruning

set -euo pipefail

DRY_RUN=true
SKIP_DOCKER=false

for arg in "$@"; do
  case "$arg" in
    --run) DRY_RUN=false ;;
    --skip-docker) SKIP_DOCKER=true ;;
    *) echo "Unknown option: $arg"; echo "Usage: $0 [--run] [--skip-docker]"; exit 1 ;;
  esac
done

if $DRY_RUN; then
  echo "🔍 DRY RUN — showing what would be deleted (use --run to actually delete)"
else
  echo "🧹 CLEANING — files will be permanently deleted"
fi
echo ""

# Track total space
TOTAL_FREED=0

# Helper: get size of a path in bytes (macOS compatible)
get_size() {
  if [ -e "$1" ]; then
    du -sk "$1" 2>/dev/null | awk '{print $1}'  # KB
  else
    echo "0"
  fi
}

# Helper: human-readable size
human_size() {
  local kb=$1
  if [ "$kb" -ge 1048576 ]; then
    echo "$(echo "scale=1; $kb/1048576" | bc)G"
  elif [ "$kb" -ge 1024 ]; then
    echo "$(echo "scale=1; $kb/1024" | bc)M"
  else
    echo "${kb}K"
  fi
}

# Helper: delete or report
clean_path() {
  local path="$1"
  local label="$2"
  if [ -e "$path" ]; then
    local size
    size=$(get_size "$path")
    TOTAL_FREED=$((TOTAL_FREED + size))
    if $DRY_RUN; then
      echo "  Would delete: $path ($(human_size "$size"))"
    else
      echo "  Deleting: $path ($(human_size "$size"))"
      rm -rf "$path"
    fi
  fi
}

# Helper: find and delete directories by pattern
clean_find() {
  local search_dir="$1"
  local pattern="$2"
  local label="$3"
  if [ -d "$search_dir" ]; then
    local found
    found=$(find "$search_dir" -name "$pattern" -type d -prune 2>/dev/null || true)
    if [ -n "$found" ]; then
      while IFS= read -r dir; do
        clean_path "$dir" "$label"
      done <<< "$found"
    fi
  fi
}

# Helper: find and delete files by pattern
clean_find_files() {
  local search_dir="$1"
  local pattern="$2"
  local label="$3"
  if [ -d "$search_dir" ]; then
    local found
    found=$(find "$search_dir" -name "$pattern" -type f 2>/dev/null || true)
    if [ -n "$found" ]; then
      while IFS= read -r f; do
        clean_path "$f" "$label"
      done <<< "$found"
    fi
  fi
}

# ============================================================
# PROJECT-LEVEL CACHES (searched from current directory)
# ============================================================
echo "━━━ Project-Level Caches (from $(pwd)) ━━━"

echo "📦 Node.js"
clean_find "." "node_modules" "node_modules"
clean_find "." ".next" "Next.js build cache"
clean_find "." ".turbo" "Turborepo cache"
clean_find "." ".firebase" "Firebase deploy cache"
clean_find_files "." ".eslintcache" "ESLint cache"
clean_find_files "." ".tsbuildinfo" "TypeScript build info"

echo "🐍 Python"
clean_find "." ".venv" "Python virtual environment"
clean_find "." "venv" "Python virtual environment"
clean_find "." "__pycache__" "Python bytecode cache"
clean_find "." ".pytest_cache" "pytest cache"
clean_find "." ".mypy_cache" "mypy cache"
clean_find "." ".ruff_cache" "ruff cache"
clean_find_files "." "*.pyc" "Compiled Python files"

echo "🦋 Flutter/Dart"
# Only clean build/ dirs that are Flutter/Dart project build outputs
# (i.e., sibling to a pubspec.yaml file), not build/ inside node_modules etc.
if [ -d "." ]; then
  found=$(find "." -name "build" -type d \
    -not -path "*/node_modules/*" \
    -not -path "*/.venv/*" \
    -not -path "*/venv/*" \
    -not -path "*/.next/*" \
    -not -path "*/.dart_tool/*" \
    -prune 2>/dev/null || true)
  if [ -n "$found" ]; then
    while IFS= read -r dir; do
      # Only delete if sibling pubspec.yaml exists (Flutter/Dart project)
      parent_dir=$(dirname "$dir")
      if [ -f "$parent_dir/pubspec.yaml" ]; then
        clean_path "$dir" "Flutter/Dart build artifacts"
      fi
    done <<< "$found"
  fi
fi
clean_find "." ".dart_tool" "Dart tool cache"

echo ""

# ============================================================
# GLOBAL CACHES (home directory)
# ============================================================
echo "━━━ Global Caches ━━━"

echo "☕ Gradle"
clean_path "$HOME/.gradle/caches" "Gradle caches"

echo "🦀 Cargo/Rust"
clean_path "$HOME/.cargo/registry" "Cargo registry"
clean_path "$HOME/.cargo/git" "Cargo git cache"

echo "📦 npm/Yarn"
clean_path "$HOME/.npm/_cacache" "npm cache"

echo "🐍 pip"
clean_path "$HOME/Library/Caches/pip" "pip cache"

echo "🦋 Flutter/Dart"
clean_path "$HOME/.pub-cache" "Dart pub cache"

echo "🍎 Xcode"
clean_path "$HOME/Library/Developer/Xcode/DerivedData" "Xcode DerivedData"

echo "🫛 CocoaPods"
clean_path "$HOME/Library/Caches/CocoaPods" "CocoaPods cache"

echo ""

# ============================================================
# DOCKER (optional)
# ============================================================
if ! $SKIP_DOCKER; then
  echo "━━━ Docker ━━━"
  if command -v docker &> /dev/null; then
    if $DRY_RUN; then
      echo "  Would run: docker system prune -a -f"
      docker system df 2>/dev/null || echo "  (Docker not running)"
    else
      echo "  Running docker system prune -a -f..."
      docker system prune -a -f
    fi
  else
    echo "  Docker not installed. Skipping."
  fi
  echo ""
fi

# ============================================================
# SUMMARY
# ============================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if $DRY_RUN; then
  echo "🔍 Space that would be freed: $(human_size $TOTAL_FREED)"
  echo "   Run with --run to actually delete."
else
  echo "🧹 Total space freed: $(human_size $TOTAL_FREED)"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"