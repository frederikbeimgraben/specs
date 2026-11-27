{
  description = "The development shell of the project";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  # The specs command of the kit. The ref must be the commit in specs.lock.
  inputs.specs.url = "github:frederikbeimgraben/specs/{ref}";

  outputs =
    { nixpkgs, specs, ... }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forAll = f: nixpkgs.lib.genAttrs systems (system: f system nixpkgs.legacyPackages.${system});
    in
    {
      devShells = forAll (
        system: pkgs: {
          default = pkgs.mkShell {
            packages = [ specs.packages.${system}.default ];
          };
        }
      );
    };
}
