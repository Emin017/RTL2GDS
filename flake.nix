{
  description = "A tool to compile your RTL files into GDSII layouts.";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    iedaBump.url = "github:Emin017/nixpkgs/bump-ieda-25-3-12";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      iedaBump,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        overlay = import ./nix/overlay.nix;
        iedaPkgs = iedaBump.legacyPackages.${system};
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ overlay ];
          config.packageOverrides = pkgs: {
            ieda = iedaPkgs.ieda;
          };
        };
      in
      {
        formatter = pkgs.nixfmt-rfc-style;
        packages = {
          default = pkgs.rtl2gds;
          inherit (pkgs) rtl2gds rtl2gdsDocker;
        };
        app.rtl2gds = pkgs.rtl2gds;
        devShells.default = pkgs.mkShell {
          inputsFrom = [
            pkgs.rtl2gds
          ];
          buildInputs =
            with pkgs;
            [
              uv
              yosys
            ]
            ++ iedaPkgs.ieda;
          shellHook = ''
            source .venv/bin/activate
            export PYTHONPATH=`pwd`/src
          '';
        };
      }
    );
}
