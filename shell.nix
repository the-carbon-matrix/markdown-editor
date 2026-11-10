{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  packages = with pkgs; [
    # Python Tooling
    (python313.withPackages (python-pkgs:
      with python-pkgs; [
        uv
        ruff
      ]))
    basedpyright

    # JS/TS Tooling
    nodejs_24
    typescript-language-server
    vue-language-server
    vscode-langservers-extracted
    emmet-language-server
    prettier
  ];

  env = {
    LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
      pkgs.libz
    ];

    FLASK_DEBUG = 1;
  };
}
