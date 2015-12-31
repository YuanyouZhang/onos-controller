#!/usr/bin/env python

import os
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

from subprocess import check_call

hooks = Hooks()
config = config()

@hooks.hook("config-changed")
def config_changed():
    pass 

@hooks.hook("controller-api-relation-joined")
def controller_api_joined():
    relation_set(port=8181, username="admin", password="admin")

@hooks.hook()
def install():
        #install jdk and onos
        shutil.copy("files/onos_install.sh", "/opt")
        shutil.copy("files/onos.conf", "/etc/init")
        check_call("sh /opt/onos_install.sh",shell=True)


@hooks.hook()
def start():
        service_start("onos")
        check_call("sleep 60", shell=True)
        check_call(["/opt/onos/bin/onos", "-r", "61",
                "feature:install", "onos-app-vtn-onosfw", "onos-openflow-base","onos-openflow"])
        check_call("/opt/onos/bin/onos \"externalportname-set -n eth1\"", shell=True)

@hooks.hook("ovsdb-manager-relation-joined")
def ovsdb_manager_joined():
    relation_set(port=6640, protocol="tcp")


@hooks.hook()
def stop():
        service_stop("onos")

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
