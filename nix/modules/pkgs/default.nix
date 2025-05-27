{
  pkgs,
  ...
}:
let
  iedaUnstable =
    with pkgs;
    ieda.overrideAttrs (oldAttrs: {
      src = iedaSrcFetcher {
        pr = 48;
        iedaVersion = "0.1.0";
        hash = "sha256-qmMg98xMVducma6sn0I3qneXVVcG8zO0TInR/AwtsW0=";
        remoteUrl = "https://gitee.com/oscc-project/iEDA";
        patches = [
          # This patch is to fix the compile error on the newer version of gcc/g++
          # which is caused by some incorrect declarations and usages of the Boost library.
          # Should be removed after we upstream these changes.
          ./patches/idrc-compile.patch
          ./patches/iir-compile.patch
        ];
      };
      buildPhase = ''
        cmake --build . -j "$NIX_BUILD_CORES" --target iEDA
      '';
    });
in
{
  packages = {
    default = pkgs.python3Packages.callPackage ./rtl2gds.nix { inherit iedaUnstable; };
    ieda = iedaUnstable;
  };

}
