#!/usr/bin/env python3
import io
import jinja2
import threading
import paramiko
from . import queue

'''
a host consists of the following components.
    ssh - the paramiko.SSHClient()
    ssh_lock - a thread lock to prevent multiple tasks at once per connection
    facts - a dict to store host related info
    facts['address'] - default fact that provides the address of the host
'''

# tool to help coordinate bulk tasks over ssh
class Client():
    facts = {} # shared facts
    hosts = {}
    _queue = queue.queued()
    _skip = None
    _select = None

    def __init__(self):
        pass

    # connect to an ssh server
    # host[options] become kwargs for paramiko.client.SSHClient.connect
    # see http://docs.paramiko.org/en/stable/api/client.html#paramiko.client.SSHClient.connect
    def connect(self, host):
        if isinstance(host, list):
            for h in host:
                self.connect(h)
            return

        # address is required field
        if 'address' not in host:
            raise Exception("connect() address is required attribute")

        # make sure we don't already have an open connection
        if host['address'] in self.hosts:
            raise Exception(str(host['address']) + " already has a connection")
        
        # default host[options] value
        if 'options' not in host:
            host['options'] = {}

        # add the SSHClient to the host
        host['ssh'] = paramiko.SSHClient()
        host['ssh_lock'] = threading.Lock()
        host['ssh'].load_system_host_keys()
        host['ssh'].set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # If we want to use a key from a string, add pkey=pkey to ssh.connect()
        if 'ssh_key' in host and isinstance(host['ssh_key'], str):
            host['options']['pkey'] = paramiko.RSAKey.from_private_key(io.StringIO.StringIO(host['ssh_key']))
        else:
            host['ssh'].load_system_host_keys()

        # Attempt to make contact
        host['ssh'].connect(host['address'], username=host['username'], **host['options'])

        # ensure facts is defined
        if 'facts' not in host or not isinstance(host['facts'], dict):
            host['facts'] = {}
        
        # guaranteed facts!
        host['facts']['address'] = host['address']

        # ensure groups are set to an array
        if 'groups' not in host['facts']:
            host['facts']['groups'] = []
        

        # add the host to the list of hosts
        self.hosts[host['address']] = host
    
    # closes all ssh connections
    def close_all(self):
        for _, host in self.hosts.items():
            host['ssh'].close()

    # runs a command on a specific server
    def run_cmd_on_host(self, host, cmd_template):
        host['ssh_lock'].acquire()
        parsed_cmd = jinja2.Template(cmd_template).render(self.facts, facts=host['facts'])
        _, _stdout, _stderr = host['ssh'].exec_command(parsed_cmd)
        _status = _stdout.channel.recv_exit_status()
        self._queue.append({
                'host': host,
                'command': parsed_cmd,
                'status': _status,
                'stdout': _stdout.read().decode('utf-8'),
                'stderr': _stderr.read().decode('utf-8')
            })
        host['ssh_lock'].release()

    # run commands against connected servers
    def cmd(self, cmd_template, clear_filters=True, threaded=True):
        threads = []
        
        for address, host in self.hosts.items():
            if self.allowed_by_filters(address):
                if threaded:
                    t = threading.Thread(target=self.run_cmd_on_host, args=[host, cmd_template])
                    t.start()
                    threads.append(t)
                else:
                    self.run_cmd_on_host(host, cmd_template)

        for x in threads:
            x.join()
        
        if clear_filters:
            self.clear_filters()
        return self._queue.get()

    # downloads a file from a server
    def download_from_host(self, host, remote_src, local_dest):
        host['ssh_lock'].acquire()
        parsed_local_dest = jinja2.Template(local_dest).render(self.facts, facts=host['facts'])
        ftp_client = host['ssh'].open_sftp()
        ftp_client.get(remote_src, parsed_local_dest)
        ftp_client.close()
        host['ssh_lock'].release()

    # run commands against connected servers
    def get(self, remote_src, local_dest, clear_filters=True, threaded=True):
        threads = []
        
        for address, host in self.hosts.items():
            if self.allowed_by_filters(address):
                if threaded:
                    t = threading.Thread(target=self.download_from_host, args=[host, remote_src, local_dest])
                    t.start()
                    threads.append(t)
                else:
                    self.download_from_host(host, remote_src, local_dest)

        for x in threads:
            x.join()
        
        if clear_filters:
            self.clear_filters()
        return self._queue.get()

    # uploads a file to a server
    def upload_to_host(self, host, local_src, remote_dest, parse_tpl):
        host['ssh_lock'].acquire()
        ftp_client = host['ssh'].open_sftp()

        if parse_tpl:
            parsed_tpl = jinja2.Template(open(local_src).read()).render(self.facts, facts=host['facts'])
            file=ftp_client.file(remote_dest, "w", -1)
            file.write(parsed_tpl)
            file.flush()
        else:
            ftp_client.put(local_src, remote_dest)

        ftp_client.close()
        host['ssh_lock'].release()

    # run upload_to_host against connected servers
    def put(self, local_src, remote_dest, parse_tpl=False, clear_filters=True, threaded=True):
        threads = []
        
        for address, host in self.hosts.items():
            if self.allowed_by_filters(address):
                if threaded:
                    t = threading.Thread(target=self.upload_to_host, args=[host, local_src, remote_dest, parse_tpl])
                    t.start()
                    threads.append(t)
                else:
                    self.upload_to_host(host, local_src, remote_dest, parse_tpl)

        for x in threads:
            x.join()
        
        if clear_filters:
            self.clear_filters()
        return self._queue.get()

    # check filters and return true if the task can be ran on this host
    def allowed_by_filters(self, address):
        if self._skip is not None and address in self._skip:
            return False
        
        if len(self._select) is not None and address not in self._select:
            return False
        
        return True

    # lazy function to just determine if there was a non-zero status
    def check_all_statuses(self, n):
        for x in n:
            if n['status'] != 0:
                return False
        return True

    # filter to skip hosts when cmd runs again
    def skip(self, hosts):
        if self._skip is None:
            self._skip = []

        if isinstance(hosts, list):
            self._skip.extend(hosts)
        elif isinstance(hosts, str):
            self._skip.append(hosts)
        else:
            raise Exception("skip(): hosts provided must be a list or string")
        return self

    # filter to select what hosts cmd runs again
    def select(self, hosts):
        if self._select is None:
            self._select = []

        if isinstance(hosts, list):
            self._select.extend(hosts)
        elif isinstance(hosts, str):
            self._select.append(hosts)
        else:
            raise Exception("select(): hosts provided must be a list or string")
        return self

    # search for hosts in a group
    def find_by_group(self, groups):
        hosts_out = []
        if isinstance(groups, list):
            for address, host in self.hosts.items():
                for group in host['facts']['groups']:
                    if group in groups:
                        hosts_out.append(address)
        elif isinstance(groups, str):
            for address, host in self.hosts.items():
                if groups in host['facts']['groups']:
                    hosts_out.append(address)
        else:
            raise Exception("find_by_group(): groups provided must be a list or string")

        return hosts_out


    # filter to skip hosts by group when cmd runs again
    def skip_groups(self, groups):
        if self._skip is None:
            self._skip = []

        hosts = self.find_by_group(groups)
        self._skip.extend(hosts)
        return self

    # filter to select hosts by group when cmd runs again
    def select_groups(self, groups):
        if self._select is None:
            self._select = []

        hosts = self.find_by_group(groups)
        self._select.extend(hosts)
        return self

    # clears all filters
    def clear_filters(self):
        self._skip = None
        self._select = None

    # utility function to get list of filtered hosts
    def get_hosts(self, clear_filters=True):
        hosts = []

        for address, host in self.hosts.items():
            if self.allowed_by_filters(address):
                hosts.append(host)

        if clear_filters:
            self.clear_filters()
        
        return hosts