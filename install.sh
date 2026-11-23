#!/usr/bin/env bash
# Copy the spec kit into a project. A file that exists in the project stays as it is.
# Usage: install.sh <project-dir> [owner-login]
set -euo pipefail

kit="$(cd "$(dirname "$0")" && pwd)"
target="${1:?usage: install.sh <project-dir> [owner-login]}"
owner="${2:-}"
target="$(cd "$target" && pwd)"

if [ "$kit" = "$target" ]; then
  echo "install.sh: the project must not be the kit itself" >&2
  exit 1
fi

copied=()
skipped=()
while IFS= read -r -d '' rel; do
  rel="${rel#./}"
  file="$kit/$rel"
  dest="$target/$rel"
  if [ -e "$dest" ]; then
    skipped+=("$rel")
    continue
  fi
  mkdir -p "$(dirname "$dest")"
  cp "$file" "$dest"
  copied+=("$rel")
  if [ -n "$owner" ] && [[ "$rel" == specs/*.md ]]; then
    sed -i.bak -E "s/^owner: .*/owner: $owner/" "$dest" && rm -f "$dest.bak"
  fi
done < <(
  cd "$kit" && find specs scripts/check_specs.py .claude/skills/spec-* .github/workflows/specs.yml \
    -type f -print0
)

echo "Copied ${#copied[@]} files."
if [ "${#skipped[@]}" -gt 0 ]; then
  echo "Skipped ${#skipped[@]} files that exist. Merge them by hand (skill spec-adopt):"
  printf '  %s\n' "${skipped[@]}"
fi
echo "Next: edit specs/config.toml, then run python3 scripts/check_specs.py --write"
