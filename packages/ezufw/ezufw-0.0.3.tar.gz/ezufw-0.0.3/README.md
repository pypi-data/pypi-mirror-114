# EzUFW - wrapper for Uncomplicated Firewall

Package allows control UFW from python side.

## Table of contents
* [Installation](#Installation)
* [Description](#Description)
* [Usage](#Usage)


## Installation
```
pip install ezufw
```

## Description

EzUFW is based on class. To manipulate UFW (iptables) rules first initialize the object and execute its methods.

List of methods:
```
enable() 
disable()
rules() # get all registered rules
execute(*cmd, force=False) # execute command 
reset(default_policies=True, force=True) # reset UFW setup and apply basic policies by default
delete_by_port(*ports) # delete rules which are related to the given ports
delete_by_ip(*ip_address) # delete rules which are related with given IPs
```

## Usage

```
from ezufw import EzUFW

ufw = EzUFW()
```
#### Example 1
```

```



