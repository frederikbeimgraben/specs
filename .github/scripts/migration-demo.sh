#!/usr/bin/env bash
# Migrate one demo project from one start commit with the program of this checkout (W 000090).
# Usage: migration-demo.sh <start commit> <kit|init>
set -euo pipefail

kit=$(git rev-parse --show-toplevel)
start=$(git -C "$kit" rev-parse "$1")
demo=$2
dir=$(mktemp -d)
commit() { git -C "$dir" -c user.name=ci -c user.email=ci@example.invalid commit -q --allow-empty -m "$1"; }

case $demo in
  kit)
    git -C "$kit" worktree add -q --detach "$dir" "$start"
    repo=$(sed -n 's/^KIT_REPO = "\(.*\)"$/\1/p' "$dir/src/specs_kit/project.py")
    printf '\n[upstream."%s"]\nref = "%s"\n' "$repo" "$start" >> "$dir/specs.toml"
    ;;
  init)
    git -C "$dir" init -q
    git -C "$dir" remote add origin https://github.com/example/demo
    commit empty
    (cd "$dir" && nix run "git+file://$kit?rev=$start" -- init --forge github --raw)
    ;;
  *)
    echo "unknown demo $demo; use kit or init" >&2
    exit 2
    ;;
esac

git -C "$dir" add -A
commit start
(cd "$dir" && nix run "$kit" -- install --raw)
git -C "$dir" add -A
commit migrated
(cd "$dir" && nix run "$kit" -- install --raw)
changed=$(git -C "$dir" status --porcelain)
if [ -n "$changed" ]; then
  echo "the second install changed files:" >&2
  echo "$changed" >&2
  exit 1
fi
