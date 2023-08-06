import yaml
import pkgdependencymanager.util as util
import subprocess
PACKAGE_COMMANDS = {
    "Linux/Arch": "sudo pacman -Sy",
    "Linux/Ubuntu": "sudo apt-get install",
    "macOS": "brew install"
}
class PackageConfig:
    def __init__(self, config_path: str):
        with open(config_path, "r") as stream:
            data = yaml.load(stream, Loader=yaml.Loader)
            stream.close()
        platform = util.get_platform()
        try:
            self.command = PACKAGE_COMMANDS[platform]
        except KeyError:
            self.command = None
        self.packages = list[str]()
        node = util.get_tree_element(platform, data)
        if node != None:
            try:
                self.command = str(node["command"]).strip()
            except KeyError:
                pass # if the install command isnt specified, simply use the default
            try:
                for package in node["packages"]:
                    self.packages.append(str(package))
            except KeyError:
                pass # if the packages list wasnt specified, we assume there are no packages to install
    def install(self):
        if self.command == None:
            print("No command was given and there is no default for this platform - cannot install packages")
            return 1
        if len(self.packages) == 0:
            print("No packages to install for this platform")
            return 1
        arguments = self.command.split()
        for package in self.packages:
            arguments.append(package.strip())
        return subprocess.call(arguments)