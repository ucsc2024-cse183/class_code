#! /bin/bash
cd $(dirname "$0")
if [ $USER != "mdipierro" ]; then
    echo "git reset --hard origin/main"
fi
echo "Installing/upgrading Nix and required packages (not worries, not affecting your OS)"
daemon=${1:---daemon}
export NIXPKGS_ALLOW_UNSUPPORTED_SYSTEM=1
which nix-shell || curl -k -L https://nixos.org/nix/install | sh -s -- $daemon
cat <<\EOF > shell.nix
let
  nixpkgs-src = builtins.fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11";
  };

  pkgs = import nixpkgs-src {
    config = {
      allowUnfree = true;
    };
  };
  shell = pkgs.mkShell {
    buildInputs = [
      # development environment
      pkgs.git
      pkgs.python311
   ];

    shellHook = ''
      # Allow the use of wheels.
      VENV_PATH=venv2
      # Setup the virtual environment if it does not already exist.
      if test ! -d $VENV_PATH; then
        python -m venv $VENV_PATH
      fi
      $VENV_PATH/bin/pip install -U pip
      $VENV_PATH/bin/pip install -U requests
      $VENV_PATH/bin/pip install -U mechanize
      $VENV_PATH/bin/pip install -U selenium
      $VENV_PATH/bin/pip install -U beautifulsoup4
      $VENV_PATH/bin/pip install -U webdriver-manager
      $VENV_PATH/bin/pip install -U py4web
      source $VENV_PATH/bin/activate
      alias grade=`realpath grader/grade.py`
    '';
  };
in shell
EOF
nix-shell shell.nix
