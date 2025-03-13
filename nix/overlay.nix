final: prev: {
  rtl2gds = final.python3Packages.callPackage ./pkgs/rtl2gds.nix { };
  rtl2gdsDocker = final.callPackage ./pkgs/docker.nix { };
  klayout-pypi = final.python3Packages.callPackage ./pkgs/klayout.nix { };
}
