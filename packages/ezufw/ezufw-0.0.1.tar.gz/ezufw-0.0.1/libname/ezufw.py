"""
### ufw default policies
# sudo ufw default deny incoming
# sudo ufw default allow outgoing

# sudo ufw allow ssh
# sudo ufw allow http
# sudo ufw allow https
# sudo ufw allow ssl

# sudo ufw allow from 10.0.0.1

## deny all ssh, but allow from ip
# sudo ufw allow from 10.0.0.1 to any port 22
# sudo ufw allow from <ip> to any port 80

## deny
# ufw status numbered
# sudo ufw delete [:rule-number]

# sudo ufw deny icmp
# sudo ufw deny from <ip>
"""

from ufw.common import programName
from ufw.frontend import UFWFrontend, parse_command
import gettext
import logging
import re


gettext.install(programName)

LOGGER = logging.getLogger('ufw')


class EzUFW(UFWFrontend):
 
    SPLITTER = re.compile(r'\s+')
    PORT_SPLITTER = re.compile(r',')
    IPV4_REGEX = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    EMPTY = ""

    def __init__(self, dry_run=False):
        super().__init__(dry_run)

    def rules(self):
        return self.backend.get_rules()

    def _command(self, *cmd):
        command = [programName]
        for c in cmd:
            command.extend(self.SPLITTER.split(str(c)))

        return parse_command(command)

    def execute(self, *cmd, force=False):
        ufw_cmd = self._command(*cmd)
        rule = ufw_cmd.data.get('rule', self.EMPTY)
        ip_type = ufw_cmd.data.get('iptype', self.EMPTY)
        return self.do_action(ufw_cmd.action, rule, ip_type, force)

    def reset(self, default_policies=True, force=True):
        self.execute('reset', force=force)
        if default_policies:
            self.execute("default", "deny", "incoming", force=force)
            self.execute("default", "allow", "outgoing", force=force)

    def enable(self):
        self.set_enabled(True)

    def disable(self):
        self.set_enabled(False)

    def delete_by_port(self, *ports):
        """
        Remove the rules connected with specifiec port. Counter keep numbering for the rule. 
        When the rule is removed from ufw other rules are lifted and rules' indexes are changed.

        @return list of removed rules.
        """
        removed_rules = []
        selected_ports = [max(0, int(port)) for port in ports]
 
        counter = 1
        for rule in self.rules():
            rule_port = -1 if rule.dport is None else int(rule.dport)
            if rule_port in selected_ports:
                removed_rules.append(rule)
                self.execute("delete", counter, force=True)
            else:
                counter += 1

        return removed_irules

    def delete_by_ip(self, *ip_address):
        """
        Remove the rules connected to specific ip_address.
        """
        removed_rules = []
        counter = 1
        for rule in self.rules():
            if rule.src in ip_address:
                removed_rules.append(rule)
                self.execute("delete", counter, force=True)
            else:
                counter += 1

        return removed_rules

    def deny(self, port=None, protocol=None):
        values = []
        if port is not None:
            values.append(port)
            if protocol is not None:
                values.append("/")
                values.append(protocol)
        return self.denyA(None if not values else "".join(map(str, values)))

    def denyA(self, port_and_protocol=None):
        cmd = ('default', 'deny') if port_and_protocol is None else ("deny", port_and_protocol)
        return self.execute(*cmd)

    def deny_from(self, ip_address, *ports):
        if ports:
            for port in ports:
                self.execute("deny", "from", ip_address, "to", "any", "port", port)
        else:
            self.execute("deny", "from", ip_address)

    def allow_from(self, ip_address, *ports):
        if ports:
            for port in ports:
                self.execute("allow", "from", ip_address, "to", "any", "port", port)
        else:
            self.execute("allow", "from", ip_address)

    def insert(self, ip_address, index=1, comment=""):
        """
        UFW (iptables) rules are applied in order of insertion. When the rule is matched other rules are skipped.
        In case when given IP should be banned, the rule must be on top. 
        """
        cmd = ["insert", index, "deny", "from", ip_address]
        if comment:
            cmd.extend(["comment", comment])
        return self.execute(*cmd)

    def status(self, verbose=True):
        cmd = ("status", "verbose") if verbose else ("status",)
        return self.execute(*cmd)

