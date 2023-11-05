{
  description = "A Python 3.10 project";

  inputs.nixpkgs.url = github:NixOS/nixpkgs/nixos-unstable;
  inputs.flake-utils.url = github:numtide/flake-utils;

  outputs = { self, nixpkgs, flake-utils }: flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
      makePackage = with pkgs; python3Packages.buildPythonApplication rec {
        name = "my-python-project";
        buildInputs = [
          stderred
        ];
        
        src = ./.;

        shellHook = ''
          export PYTHON_LD_LIBRARY_PATH=$(echo ${lib.makeLibraryPath [
            stdenv.cc.cc.lib
            zlib
            glib
            xorg.libX11
          ]})  
          export PYTHONHOME=${python38}   // You might want to replace `python38` with your specific python version.
          export PYTHONBIN=${python38}/bin/python3
          export LANG=en_US.UTF-8
          export STDERREDBIN=${stderred}/bin/stderred
        '';
      };
    in {
      defaultPackage = makePackage;
    }
  );
}

