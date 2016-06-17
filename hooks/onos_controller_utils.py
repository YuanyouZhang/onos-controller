import subprocess

from charmhelpers.core.decorators import retry_on_exception


PROFILES = {
    "openvswitch-onos": {
        "feature:install": ["onos-app-vtn-onosfw", "onos-openflow-base",
                            "onos-openflow"],
        "port": 8080
    },
    "openvswitch-onos-goldeneye": {
        "feature:install": ["onos-ovsdatabase",
                            "onos-ovsdb-base",
                            "onos-drivers-ovsdb",
                            "onos-ovsdb-provider-host",
                            "onos-app-vtn-onosfw",
                            "onos-openflow-base",
                            "onos-openflow"],
        "port": 8080
    },
}
PROFILES["default"] = PROFILES["openvswitch-onos"]


@retry_on_exception(5, base_delay=10, exc_type=subprocess.CalledProcessError)
def run_onos(cmds):
    run_cmd = ["/opt/onos/bin/onos"]
    run_cmd.extend(cmds)
    output = subprocess.check_output(run_cmd)
    return output


def installed_features():
    installed = []
    out = run_onos(["feature:list"])
    for line in out.split("\n"):
        columns = line.split("|")
        if len(columns) > 2:
            install_flag = columns[2].replace(" ", "")
            if install_flag == "x":
                installed.append(columns[0].replace(" ", ""))
    return installed


def filter_installed(features):
    installed = installed_features()
    whitelist = [feature for feature in features if feature not in installed]
    return whitelist


def process_onos_cmds(onos_cmds):
    features = filter_installed(onos_cmds.get("feature:install", []))
    if features:
        run_onos(["feature:install"] + features)
