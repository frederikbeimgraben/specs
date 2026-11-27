{
  description = "The specs command: check and manage the specs of a project";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { self, nixpkgs }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forAll = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
      rev = self.rev or "dirty";
    in
    {
      packages = forAll (pkgs: {
        default = pkgs.python313Packages.buildPythonApplication {
          pname = "specs";
          version = "0.1.0";
          pyproject = true;
          src = self;
          build-system = [ pkgs.python313Packages.setuptools ];
          dependencies = with pkgs.python313Packages; [
            jsonschema
            mcp
            rich
          ];
          makeWrapperArgs = [
            "--set"
            "SPECS_KIT_SOURCE"
            "${self}"
            "--set"
            "SPECS_KIT_REV"
            rev
            "--prefix"
            "PATH"
            ":"
            (pkgs.lib.makeBinPath [ pkgs.git ])
          ];
          meta.mainProgram = "specs";
        };
      });

      apps = forAll (pkgs: {
        default = {
          type = "app";
          program = pkgs.lib.getExe self.packages.${pkgs.stdenv.hostPlatform.system}.default;
        };
      });

      devShells = forAll (pkgs: {
        default = pkgs.mkShell {
          packages = [
            (pkgs.python313.withPackages (ps: [
              ps.jsonschema
              ps.mcp
              ps.rich
            ]))
            pkgs.ruff
            pkgs.basedpyright
          ];
        };
      });
    };
}
