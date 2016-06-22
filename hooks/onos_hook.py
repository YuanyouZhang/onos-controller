#!/usr/bin/env python

import sys
import shutil


from charmhelpers.core.hookenv import (
    Hooks,
    UnregisteredHookError,
    config,
    log,
    relation_set
)

from charmhelpers.core.host import (
    service_start,
    service_stop
)
from onos_controller_utils import process_onos_cmds
from onos_controller_utils import PROFILES
from subprocess import check_call

hooks = Hooks()


@hooks.hook("config-changed")
def config_changed():
    gatewaymac = config("gateway-mac")
    if (gatewaymac is not None) and len(gatewaymac) > 4:
        if gatewaymac != "default":
            check_call("/opt/onos/bin/onos \'externalgateway-update -m " +
                       gatewaymac + "\'", shell=True)


@hooks.hook("controller-api-relation-joined")
def controller_api_joined():
    relation_set(port=8181, username="admin", password="admin")


@hooks.hook("install.real")
def install():
    # install jdk and onos.
    shutil.copy("files/onos_install.sh", "/opt")
    #shutil.copy("files/onos.conf", "/etc/init")
    shutil.copy("files/onos", "/etc/init.d")
    if config("install-url"):
        url = config("install-url")
        check_call("sh /opt/onos_install.sh "+url, shell=True)


@hooks.hook("start")
def start():
    #service_start("onos")
    check_call("sudo sh /etc/init.d/onos start", shell=True)
    check_call("sleep 60", shell=True)
    if config("profile"):
        process_onos_cmds(PROFILES[config("profile")])
    extport = config("ext-port")
    check_call("/opt/onos/bin/onos \"externalportname-set -n " +
               extport + "\"", shell=True)


@hooks.hook("ovsdb-manager-relation-joined")
def ovsdb_manager_joined():
    relation_set(port=6640, protocol="tcp")


@hooks.hook("stop")
def stop():
    #service_stop("onos")
    check_call("sudo sh /etc/init.d/onos stop", shell=True)


def main():
    try:
        hooks.execute(sys.argv)
    except UnregisteredHookError as e:
        log("Unknown hook {} - skipping.".format(e))


@hooks.hook("upgrade-charm")
def upgrade_charm():
    pass

if __name__ == "__main__":
    main()
