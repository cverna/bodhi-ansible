# bodhi-ansible
 Ansible modules to manage Bodhi resources

This is not a role use to install [Bodhi](https://github.com/fedora-infra/bodhi), but a way to manage ressources in Bodhi using Ansible instead of the CLI.

## bodhi_release

The `bodhi_release` module creates a release within Bodhi.

```yaml
- name: Create the Fedora 31 Release
  bodhi_releases:
    name: "F31"
    long_name: "Fedora 31"
    id_prefix: "FEDORA"
    version: "31"
    branch: "f31"
    dist_tag: "f31"
    stable_tag: "f31-updates"
    testing_tag: "f31-updates-testing"
    candidate_tag: "f31-updates-candidate"
    pending_stable_tag: "f31-updates-pending"
    pending_testing_tag: "f31-updates-testing-pending"
    pending_signing_tag: "f31-signing-pending"
    override_tag: "f31-override"
    state: "pending"
    user: "releng"
    url: "https://bodhi.fedoraproject.org"
```
