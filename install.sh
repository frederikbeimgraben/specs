#!/usr/bin/env bash
# Copy the spec kit into a project. A file that exists in the project stays as it is.
# The rules of the kit go to specs/upstream/github.com/frederikbeimgraben/specs/ as an unchanged
# copy (000048). The project numbers its own rules from 000001.
# Usage: install.sh <project-dir> [owner-login]
set -euo pipefail

repo="github.com/frederikbeimgraben/specs"
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
  if [ -n "$owner" ] && [[ "$rel" == specs/TEMPLATE*.md ]]; then
    sed -i.bak -E "s/^owner: .*/owner: $owner/" "$dest" && rm -f "$dest.bak"
  fi
done < <(
  cd "$kit" && find specs/README.md specs/TEMPLATE*.md specs/config.toml scripts/check_specs.py \
    .claude/skills/spec-* .github/workflows/specs.yml -type f -print0
)

ref="$(git -C "$kit" rev-parse HEAD)"
upstream="$target/specs/upstream/$repo"
if [ -e "$upstream" ]; then
  skipped+=("specs/upstream/$repo/")
else
  mkdir -p "$upstream"
  (cd "$kit/specs" && find . -path ./upstream -prune -o -type f -print0) |
    (cd "$kit/specs" && xargs -0 -I{} cp --parents {} "$upstream/")
  copied+=("specs/upstream/$repo/")
fi

config="$target/specs/config.toml"
if ! grep -q "^\[upstream\.\"$repo\"\]" "$config"; then
  printf '\n# The rules of the kit (000048). Update: change ref, then run --fetch.\n[upstream."%s"]\nref = "%s"\n' \
    "$repo" "$ref" >>"$config"
fi

echo "Copied ${#copied[@]} files and folders."
if [ "${#skipped[@]}" -gt 0 ]; then
  echo "Skipped ${#skipped[@]} that exist. Merge them by hand (skill spec-adopt):"
  printf '  %s\n' "${skipped[@]}"
fi
echo "Next: edit specs/config.toml, then run python3 scripts/check_specs.py --write"
