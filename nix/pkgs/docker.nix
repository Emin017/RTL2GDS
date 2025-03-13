{ pkgs, rtl2gds, ... }:
let
  self = pkgs.dockerTools.buildImage {
    name = "rtl2gds-docker";
    tag = "latest";
    copyToRoot = pkgs.buildEnv {
      name = "image-root";
      paths = with pkgs; [
        git
        file
        which
        coreutils
        nix

        bashInteractive
        dockerTools.binSh
        dockerTools.usrBinEnv

        rtl2gds
      ];
      pathsToLink = [ "/bin" ];
    };
    config = {
      Env = [
        "NIX_PAGER=cat"
        # A user is required by nix
        # https://github.com/NixOS/nix/blob/9348f9291e5d9e4ba3c4347ea1b235640f54fd79/src/libutil/util.cc#L478
        "USER=nobody"
        "EDITOR=nvim"
      ];
    };
  };
in
self
