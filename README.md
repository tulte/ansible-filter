# Ansible Filter

Script to filter for ansible changes.

## Install

```shell
cp ansible-filter.py /usr/local/bin/ansible-filter
mkdir +x /usr/local/bin/ansible-filter
```

## Execute

```shell
ansible-filter -i dev -l master -u root --check site.yml
```

## Ignore Entries

Create a File ansible-filter.ignore in the project folder. Add row seperated by semicolon. First col matcg is task and second is current line.

```
<task1>;<line>
<task2>;<line>
```

