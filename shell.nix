{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  nativeBuildInputs = with pkgs.buildPackages; [
  mpremote
  python313Packages.watchdog
  ];
}

