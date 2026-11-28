{
  description = "The spezi command: check and manage the specs of a project";

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
      version = "0.0.0+${self.shortRev or "dirty"}";
      vsix =
        pkgs:
        pkgs.buildNpmPackage {
          pname = "spezi-vscode";
          inherit version;
          src = ./editors/code;
          npmDepsHash = "sha256-QnFcSREAPCSW9q8rf6KJd76DblQvhKHoU7YKTRvasu8=";
          dontNpmBuild = true;
          nativeBuildInputs = [
            pkgs.esbuild
            pkgs.typescript
            pkgs.vsce
          ];
          buildPhase = ''
            runHook preBuild
            tsc -p .
            esbuild src/extension.ts --bundle --minify --platform=node --format=cjs \
              --external:vscode --outfile=out/extension.js
            vsce package --no-dependencies --skip-license --out spezi.vsix
            runHook postBuild
          '';
          installPhase = ''
            runHook preInstall
            install -Dm644 spezi.vsix $out/spezi.vsix
            runHook postInstall
          '';
        };
    in
    {
      packages = forAll (pkgs: {
        vsix = vsix pkgs;
        default = pkgs.python313Packages.buildPythonApplication {
          pname = "spezi-kit";
          inherit version;
          pyproject = true;
          src = self;
          build-system = [
            pkgs.python313Packages.setuptools
            pkgs.python313Packages.setuptools-scm
          ];
          env.SETUPTOOLS_SCM_PRETEND_VERSION = version;
          dependencies = with pkgs.python313Packages; [
            jsonschema
            mcp
            pygls
            pyyaml
            questionary
            rich
            tomlkit
          ];
          makeWrapperArgs = [
            "--set"
            "SPEZI_KIT_SOURCE"
            "${self}"
            "--set"
            "SPEZI_KIT_REV"
            rev
            "--set"
            "SPEZI_VSIX"
            "${vsix pkgs}/spezi.vsix"
            "--prefix"
            "PATH"
            ":"
            (pkgs.lib.makeBinPath [ pkgs.git ])
          ];
          meta.mainProgram = "spezi";
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
              ps.pygls
              ps.pytest
              ps.pyyaml
              ps.questionary
              ps.rich
              ps.tomlkit
              ps.types-pyyaml
            ]))
            pkgs.ruff
            pkgs.basedpyright
          ];
        };
      });
    };
}
