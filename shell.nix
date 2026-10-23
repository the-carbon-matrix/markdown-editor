{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  packages = with pkgs; [
    # Python Tooling
    python313
    python313Packages.pip
    basedpyright
    ruff

    # JS/TS Tooling
    nodejs_24
  ];

  env = {
    LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
      pkgs.libz
    ];

    FLASK_DEBUG = 1;
  };
}
