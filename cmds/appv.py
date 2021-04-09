"""
Application Vulnerabilities Commands
"""

import collections
import operator

import utils.table as table
import utils.color_print as color_print
import utils.checkers as checkers
import utils.filters as filters
import config
import cmds.internal as internal_cmds
from core.vuln_app_manager import load_vulns


def install(args):
    vulns = load_vulns.load_vulns_by_dir(config.vuln_app_dir_wildcard)
    vuln = filters.filter_vuln_by_name(vulns=vulns, name=args.appv)
    if not vuln:
        color_print.error_and_exit(
            'error: no application vulnerability named {appv}'.format(
                appv=args.appv))
    if not checkers.docker_kubernetes_installed():  # should install docker or k8s firstly
        return

    internal_cmds.deploy_vuln_resources_in_k8s(vuln)


def remove(args):
    vulns = load_vulns.load_vulns_by_dir(config.vuln_app_dir_wildcard)
    vuln = filters.filter_vuln_by_name(vulns=vulns, name=args.appv)
    if not vuln:
        color_print.error_and_exit(
            'error: no vulnerability named {appv}'.format(
                appv=args.appv))

    internal_cmds.delete_vuln_resources_in_k8s(vuln)


def retrieve(args):
    vulns = load_vulns.load_vulns_by_dir(config.vuln_app_dir_wildcard)
    vulns_stripped = list()
    for vuln in vulns:
        vuln_stripped = collections.OrderedDict()
        vuln_stripped['name'] = vuln['name']
        vuln_stripped['class'] = vuln['class']
        vuln_stripped['type'] = vuln['type']
        vulns_stripped.append(vuln_stripped)
    table.show_table(
        vulns_stripped, sort_key=operator.itemgetter(
            2, 1), sortby='class')
