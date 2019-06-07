#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# bodhi_release.py - Ansible module to create a new Bodhi release
#
# Copyright (C) 2019 Red Hat, Inc.
# SPDX-License-Identifier: GPL-2.0+
#
DOCUMENTATION = '''
---
author:
  - "Clément Verna <cverna@fedoraproject.org>"
module: bodhi_release
short_description: Create or Edit a Bodhi release
description:
  - Create or Edit a Bodhi release
  - Returns a bodhi release object in JSON
options:
  name:
    description:
      - release name
    required: True
  long_name:
    description
      - Long release name (eg: "Fedora 20").
    required: True
  id_prefix:
    description:
      - Release prefix (eg: FEDORA).
    required: True
  version:
    description:
      - Release version number (eg: 20).
    required: True
  branch:
    description:
      - Git branch name (eg: f20).
    required: True
  dist_tag:
    description:
      - Koji dist tag (eg: f20).
    required: True
  stable_tag:
    description:
      - Koji stable tag (eg: f20-updates).
    required: True
  testing_tag:
    description:
      - Koji testing tag (eg: f20-updates-testing).
    required: True
  candidate_tag:
    description:
      - Koji candidate tag (eg: f20-updates-candidate).
    required: True
  pending_stable_tag:
    description:
      - Koji pending tag (eg: f20-updates-pending).
    required: True
  pending_testing_tag:
    description:
      - Koji pending testing tag (eg: f20-updates-pending).
    required: True
  pending_signing_tag:
    description:
      - Koji pending signing tag (eg: f20-updates-pending-signing).
    required: False
  override_tag:
    description:
      - Koji override tag (eg: f20-override).
    required: True
  state:
    description:
      - The state of the release.
    choices: [disabled, pending, current, archived]
    default: pending
  user:
    description:
      - Name of the FAS user used to create the release.
    required: True
  mail_template:
    description:
      - Name of the email template for this release
    required: False
  composed_by_bodhi:
    description:
      - The flag that indicates whether the release is composed by Bodhi or not
    required: False
    default: True
  url:
    description:
      - URL of a Bodhi server
    required: False
    default: "https://bodhi.fedoraproject.org"
'''

EXAMPLES = '''
Meant to be used to create new release in bodhi
- bodhi_release:
    name: "F31"
    long_name: "Fedora 31"
    id_prefix: "FEDORA"
    version: 31
    branch: f31
    dist_tag: f31
    stable_tag: f31-updates
    testing_tag: f31-updates-testing
    candidate_tag: f31-updates-candidate
    pending_stable_tag: f31-updates-pending
    pending_testing_tag: f31-updates-testing-pending
    pending_signing_tag: f31-updates-signing-pending
    override_tag: f31-override
    state: pending
    user: releng

Create the release in staging using the url option.
- bodhi_release:
    name: "F31"
    long_name: "Fedora 31"
    id_prefix: "FEDORA"
    version: 31
    branch: f31
    dist_tag: f31
    stable_tag: f31-updates
    testing_tag: f31-updates-testing
    candidate_tag: f31-updates-candidate
    pending_stable_tag: f31-updates-pending
    pending_testing_tag: f31-updates-testing-pending
    pending_signing_tag: f31-updates-signing-pending
    override_tag: f31-override
    state: pending
    user: releng
    url: "https://bodhi.stg.fedoraproject.org"
'''

from ansible.module_utils.basic import *

def ensure_release(client, module, **kwargs):
    """
    Ensure that this release exists in Bodhi.
    """

    result = {"changed": False, "stdout_lines": []}

    releaseinfo = client.get_releases(name=kwargs["name"]).releases
    if not releaseinfo:
        data = {
            "csrf_token": client.csrf(),
            "name": kwargs["name"],
            "long_name": kwargs["long_name"],
            "id_prefix": kwargs["id_prefix"],
            "version": kwargs["version"],
            "branch": kwargs["branch"],
            "dist_tag": kwargs["dist_tag"],
            "stable_tag": kwargs["stable_tag"],
            "testing_tag": kwargs["testing_tag"],
            "candidate_tag": kwargs["candidate_tag"],
            "pending_stable_tag": kwargs["pending_stable_tag"],
            "pending_testing_tag": kwargs["pending_testing_tag"],
            "pending_signing_tag": kwargs["pending_signing_tag"],
            "override_tag": kwargs["override_tag"],
            "state": kwargs["state"],
            "mail_template": kwargs.get("mail_template"),
            "composed_by_bodhi": kwargs["composed_by_bodhi"],
        }
        res = client.send_request("releases/", verb="POST", data=data)
        if "errors" in res:
            module.fail_json(msg=res.errors, changed=False)
        else:
            result["changed"] = True
            result["stdout_lines"].append(f"Created the bodhi release {module.params['long_name']}")

    return result


def main():

    module_args = dict(
        name=dict(type="str", required=True),
        long_name=dict(type="str", required=True),
        id_prefix=dict(type="str", required=True),
        version=dict(type="str", required=True),
        branch=dict(type="str", required=True),
        dist_tag=dict(type="str", required=True),
        stable_tag=dict(type="str", required=True),
        testing_tag=dict(type="str", required=True),
        candidate_tag=dict(type="str", required=True),
        pending_stable_tag=dict(type="str", required=True),
        pending_testing_tag=dict(type="str", required=True),
        pending_signing_tag=dict(type="str", required=False),
        override_tag=dict(type="str", required=True),
        state=dict(choice=["disabled", "pending", "current", "archived"], default="pending"),
        user=dict(type="str", required=True),
        mail_template=dict(type="str", required=False),
        composed_by_bodhi=dict(type="str", required=False),
        url=dict(type="str", required=False, default="https://bodhi.fedoraproject.org"),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False

    )

    try:
        from bodhi.client.bindings import BodhiClient
    except ImportError:
        module.fail_json(msg="the bodhi python module not found on the target system")

    # Connect to bodhi
    client = BodhiClient(
        base_url=module.params["url"],
        username=module.params["user"],
    )

    result = ensure_release(client, module, **module.params)
    module.exit_json(**result)


main()
