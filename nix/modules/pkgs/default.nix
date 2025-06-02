{
  pkgs,
  ...
}:
let
  iedaUnstable =
    with pkgs;
    ieda.overrideAttrs (oldAttrs: {
      src = pkgs.callPackage ./iedaSrc.nix { };
    });
in
{
  packages = {
    default = pkgs.python3Packages.callPackage ./rtl2gds.nix { inherit iedaUnstable; };
    ieda = iedaUnstable;
  };

}
