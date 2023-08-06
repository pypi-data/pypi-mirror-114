from pkgdependencymanager import PackageConfig
import argparse
parser = argparse.ArgumentParser(prog="pkgdependencymanager")
parser.add_argument("--file", default="packages.yml")
args = parser.parse_args()
pkg_config = PackageConfig(args.file)
pkg_config.install()