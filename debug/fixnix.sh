#! /bin/bash

rm -rf /nix || true
sudo systemctl stop nix-daemon.service || true
sudo systemctl disable nix-daemon.socket nix-daemon.service || true
sudo systemctl daemon-reload || true
sudo rm -rf /etc/nix /etc/profile.d/nix.sh /etc/tmpfiles.d/nix-daemon.conf /nix ~root/.nix-channels ~root/.nix-defexpr ~root/.nix-profile || true
curl -k -L https://nixos.org/nix/install | sh -s -- --no-daemon
