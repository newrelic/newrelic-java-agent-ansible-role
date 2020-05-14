# Ansible role: New Relic Java agent

[![Molecule Test](https://github.com/newrelic/newrelic-java-agent-ansible-role/workflows/Molecule%20Test/badge.svg)](https://github.com/newrelic/newrelic-java-agent-ansible-role/actions?query=workflow%3A%22Molecule+Test%22)

This role installs and configures the [New Relic Java agent][3]. It should work with minimal configuration for applications running under Tomcat, Jetty, or Wildfly. We aim to support the most popular Java web servers over time.

* [Requirements](#Requirements)
* [Installation](#Installation)
* [Configuration](#Configuration)
	* [Role configuration variables](#Roleconfigurationvariables)
	* [Agent configuration variables](#Agentconfigurationvariables)
	* [Other agent-specific configuration](#Otheragent-specificconfiguration)
	* [Using your own agent config file](#Usingyourownagentconfigfile)
* [Example usage](#Exampleusage)
* [Community](#Community)
* [Issues / Enhancement Requests](#IssuesEnhancementRequests)
* [License](#License)

## <a name='Requirements'></a>Requirements

The `unzip` command must be available on the target hosts.

## <a name='Installation'></a>Installation

The recommended way to install the role is to use Ansible Galaxy:
```Shell
$ ansible-galaxy install newrelic.new_relic_java_agent
```

If you want to contribute to the role, you can clone this repo and make changes to it, then install it locally by running:

```Shell
sh examples/install_role.sh
```
Depending on how Ansible is installed on your system, you may need to preface the above command with `sudo`.

## <a name='Configuration'></a>Configuration

This role uses variables for two purposes: role configuration and agent configuration.

**Role configuration variables** describe how your hosts are set up so that the role can install the agent files to the right location and set up your Java environment to run the agent.

**Agent configuration variables** can be set up globally in your playbook or per host or group in your inventory file. They are used to create the `newrelic.yml` file that the Java agent uses to determine its configuration.

### <a name='Roleconfigurationvariables'></a>Role configuration variables

#### <a name='server_type'></a>`server_type`
**Required**
Web server used by your application. Possible values are: `tomcat`, `jetty`, and `wildfly` (standalone mode only).

#### <a name='server_root'></a>`server_root`
**Required**
Location of the web server on the host. The agent's JAR, configuration, and log files will live in a subdirectory of this directory.

#### <a name='jvm_conf_file'></a>`jvm_conf_file`
**Required**
Path of the web server configuration file to reference the New Relic Java agent. For Tomcat, for instance, it's `setenv.sh`. If it doesn't exist, the file will be created.

#### <a name='server_userserver_group'></a>`server_user` /  `server_group`
**Required**
User and group under which the web server runs. Used to set the ownership of the `newrelic.jar` and `newrelic.yml` files.

#### <a name='restart_web_server'></a>`restart_web_server`
**Optional** - **Default:** `true`
If set to false, the role does _not_ restart the web server after installing the agent. 

> Note that the agent is not activated until the web server is restarted.

#### <a name='service_name'></a>`service_name`
**Required** (unless `restart_web_server` is set to `false`)
Service name under which the web server runs. Used by Ansible to restart the web server after the agent is installed.

#### <a name='custom_instrumentation_files'></a>`custom_instrumentation_files`
**Optional**
List of XML files to enable custom instrumentation by the Java agent. See the [Custom instrumentation section](#Custominstrumentation) for more details.

### <a name='Agentconfigurationvariables'></a>Agent configuration variables

Agent configuration goes in the `nr_java_agent_config` dictionary and is added to the Java agent's config file - `newrelic.yml`. The most common settings can be specified through this role. Examples can be found in [examples/agent_install.yml](/examples/agent_install.yml).

To specify **settings for specific hosts** in your inventory use the `nr_java_agent_host_config` dictionary. For examples, see [examples/inventory.yml](/examples/inventory.yml). Host values override those in `nr_java_agent_config`.

If you need to configure settings that aren't listed below, you must provide your own, preconfigured `newrelic.yml` file (see [Using your own agent config file](#Using-your-own-agent-config-file)).

#### <a name='license_key'></a>`license_key`
**Required**
Your [New Relic license key](https://docs.newrelic.com/docs/accounts/install-new-relic/account-setup/license-key).

#### <a name='app_name'></a>`app_name`
**Required**
Name of the application being instrumented. For more details, see the [New Relic documentation on app naming][1].

#### <a name='proxy_hostproxy_portproxy_userproxy_passwordproxy_scheme'></a>`proxy_host` / `proxy_port` / `proxy_user` / `proxy_password`, / `proxy_scheme`
**Optional**
If you connect to the New Relic collector via a proxy, you can configure your proxy settings with these values. For more details, see [the New Relic documentation on configuring the Java agent][2].

#### <a name='labels'></a>`labels`
**Optional**
User-configurable custom labels for the agent. Labels are name-value pairs. Names and values are limited to 255 characters and cannot contain colons (`:`) nor semicolons (`;`). Value should be a semicolon-separated list of key-value pairs. For example:

```yaml
nr_java_agent_config:
  ...
  labels: Server:One;Data Center:Primary
```

### <a name='Otheragent-specificconfiguration'></a>Other agent-specific configuration

Besides those listed above, you can configure the following settings through this Ansible role:

* `agent_enabled`
* `high_security`
* `enable_auto_app_naming`
* `log_level`
* `audit_mode`
* `log_file_count`
* `log_limit_in_kbytes`
* `log_daily`
* `log_file_name`
* `log_file_path`
* `max_stack_trace_lines`
* `attributes`: `enabled`, `include`, `exclude`
* `transaction_tracer`: `enabled`, `transaction_threshold`, `record_sql`, `log_sql`, `stack_trace_threshold`, `explain_enabled`, `explain_threshold`, `top_n`
* `error_collector`: `enabled`, `ignore_errors`, `ignore_status_codes`
* `transaction_events`: `enabled`, `max_samples_stored`
* `distributed_tracing`: `enabled`
* `cross_application_tracer`: `enabled`
* `thread_profiler`: `enabled`
* `browser_monitoring`: `auto_instrument`
* `labels`

See the [Java agent configuration documentation][4] for more details on these settings and others. If you need to configure settings besides these, you'll need to provide a fully-specified `newrelic.yml`. For details, see the [Using your own agent config file](#Using-your-own-agent-config-file) section.

### <a name='Usingyourownagentconfigfile'></a>Using your own agent config file

If you need to specify agent configuration settings beyond those listed above, you'll need to provide your own `newrelic.yml` file. Any settings in the `nr_java_agent_config` dictionary will then be ignored. Set the variable `nr_java_agent_config_file` to the path to your file, for example:

```yaml
nr_java_agent_config_file: /path/to/your/newrelic.yml
```

If this file is on the target hosts instead of on the system running Ansible, set `nr_java_agent_config_file_is_remote` to true:

```yaml
nr_java_agent_config_file_is_remote: true
```

## <a name='Exampleusage'></a>Example usage

The [examples/agent_install.yml](/examples/agent_install.yml) and [examples/inventory.yml](/examples/inventory.yml) files provide an example of how to use the role. 

After setting up your variables in `examples/agent_install.yml` and your inventory in `examples/inventory.yml` you can try the role by running Ansible:

```Shell
ansible-playbook -i examples/inventory.yml examples/agent_install.yml
```
## <a name='Custominstrumentation'>Custom instrumentation

If you want to enable [custom instrumentation with XML](https://docs.newrelic.com/docs/agents/java-agent/custom-instrumentation/java-instrumentation-xml), you can provide a list of XML files in the `custom_instrumentation_files` variable. These files will be copied to each host that the Java agent is being installed on, if you specify the variable in your playbook. You can also install different files to different hosts by specifying the variable at the host level in your inventory, or different files for different host groups by specifying the variable at the group level, either through your inventory or through files in the `group_vars` directory.

See the [Ansible documentation on inventory and variables](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html) for more details on managing host and group variables. You can see some examples in this repo of how to specify custom instrumentation in the [custom_instrumentation_playbook.yml](examples/custom_instrumentation_playbook.yml) and [custom_instrumentation_inventory.yml](examples/custom_instrumentation_inventory.yml) files.

## <a name='Development'></a>Development

### Testing

This role uses [molecule](https://molecule.readthedocs.io/en/latest/) for testing. You'll need [Docker](https://www.docker.com/) and [Python](https://www.python.org) 3.6 or later. Install molecule with the docker module, if you haven't already:

```shell
$ pip install molecule[docker]
```

This will also install ansible, if necessary. To run the tests, call `molecule test` from the top level directory.

```shell
$ git clone https://github.com/newrelic/newrelic-java-agent-ansible-role
$ cd newrelic-java-agent-ansible-role
$ molecule test
--> Test matrix

└── default
    ├── dependency
    ├── lint
    ├── cleanup
...
```

## <a name='Community'></a>Community

New Relic hosts and moderates an online forum where customers can interact with New Relic employees as well as other customers to get help and share best practices. Like all official New Relic open source projects, there's a related Community topic in the New Relic Explorers Hub. You can find the project's topic/threads here:

https://discuss.newrelic.com/t/ansible-role-for-new-relic-java-agent/99654

## <a name='IssuesEnhancementRequests'></a>Issues / Enhancement Requests

Issues and enhancement requests can be submitted in the [Issues tab of this repository](../../issues). Please search for and review the existing open issues before submitting a new issue.

## <a name='License'></a>License

The project is released under version 2.0 of the [Apache license](http://www.apache.org/licenses/LICENSE-2.0).

[1]: https://docs.newrelic.com/docs/agents/manage-apm-agents/app-naming/name-your-application
[2]: https://docs.newrelic.com/docs/agents/java-agent/configuration/java-agent-configuration-config-file#cfg-proxy_host
[3]: https://docs.newrelic.com/docs/agents/java-agent
[4]: https://docs.newrelic.com/docs/agents/java-agent/configuration/java-agent-configuration-config-file
