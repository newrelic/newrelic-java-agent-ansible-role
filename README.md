# New Relic Java agent Ansible role

## Description

This role installs and configures the [New Relic Java agent][3]. It should work with minimal configuration for applications running under Tomcat, Jetty or Wildfly. Our aim is to support the most popular Java web servers over time.

## Requirements

This role requires the `unzip` command to be available on the target hosts.

## Installation and example usage

### Installation

NOTE: this role is not yet available on Ansible Galaxy. To install the role locally run this command:

```Shell
$ sh examples/install_role.sh
```

Depending on how Ansible is installed on your system, you may need to preface the above command with `sudo`.

### Example usage

The `examples/agent_install.yml` file, along with `examples/inventory.yml`, provide an example of how to use the role. After setting up your variables in `examples/agent_install.yml` and your inventory in `examples/inventory.yml` you can try the role out like this:

```Shell
$ ansible-playbook -i examples/inventory.yml examples/agent_install.yml
```

## Configuration

This role uses variables for two purposes: agent configuration and role configuration.

Agent configuration variables can be set up globally in your playbook or per host or group in your inventory file. They will be used to create the `newrelic.yml` file that the Java agent uses to determine its configuration.

Role configuration variables describe how your hosts are set up so that the role can install the agent files to the right location and set up your Java environment to run the agent.

### Role configuration variables

#### server_type (REQUIRED)

The web server used by your application. `tomcat`, `jetty`, and `wildfly` (standalone mode only) are supported out of the box.

#### server_root (REQUIRED)

The location of the web server on the host; the agent's jar, configuration, and log files will live in a subdirectory of this directory.

#### jvm_conf_file (REQUIRED)

The path to the file with which the web server will be configured to use the New Relic Java agent. For Tomcat, for instance, this is the `setenv.sh` file. The file will be created if necessary.

#### server_user, server_group (REQUIRED)

The user and group under which the web server runs; will be used to set the ownership of the `newrelic.jar` and `newrelic.yml` files.

#### restart_web_server (OPTIONAL, default true)

If defined to false, the role will _not_ restart the web server after installing the agent. NOTE: the agent will not be activated until the web server is restarted.

#### service_name (REQUIRED, unless restart_web_server is set to false)

The service name under which the web server runs; used by ansible to restart the web server after the agent is installed.

### Agent configuration variables

Configuration specific to the agent goes in the `nr_java_agent_config` dictionary and will be added to the Java agent's config file - `newrelic.yml` - by template. The most commonly-used settings can be specified through this role - some examples can be found in `examples/agent_config.yml`. If you need to configure settings that aren't listed below, you'll need to provide your own, preconfigured `newrelic.yml` file - see [Using your own agent config file](#Using-your-own-agent-config-file) for details.

You can specify agent configuration settings for specific hosts in your inventory using the `nr_java_agent_host_config` dictionary. See `examples/inventory.yml` for some examples. Values here will override those in `nr_java_agent_config`.

#### license_key (REQUIRED)

Your New Relic license key.

#### app_name (REQUIRED)

The name of the application being instrumented. See the [documentation on app naming][1] for more details.

#### proxy_host, proxy_port, proxy_user, proxy_password, proxy_scheme (OPTIONAL)

If you connect to the New Relic collector via a proxy, you can configure your proxy settings with these values. See [the documentation on configuring the Java agent][2] for more details.

#### labels
User-configurable custom labels for this agent. Labels are name-value pairs. Names and values are limited to 255 characters and may not contain colons (:) or semicolons (;). The value of this setting should be a semicolon-separated list of key:value pairs, eg:

```yaml
nr_java_agent_config:
  ...
  labels: Server:One;Data Center:Primary
```

#### Other agent-specific configuration

Besides those listed above, you can configure the following settings through this Ansible role:

* agent_enabled
* high_security
* enable_auto_app_naming
* log_level
* audit_mode
* log_file_count
* log_limit_in_kbytes
* log_daily
* log_file_name
* log_file_path
* max_stack_trace_lines
* attributes: enabled, include, exclude
* transaction_tracer: enabled, transaction_threshold, record_sql, log_sql, stack_trace_threshold, explain_enabled, explain_threshold, top_n
* error_collector: enabled, ignore_errors, ignore_status_codes
* transaction_events: enabled, max_samples_stored
* distributed_tracing: enabled
* cross_application_tracer: enabled
* thread_profiler: enabled
* browser_monitoring: auto_instrument
* labels

See the [Java agent configuration documentation][4] for more details on these settings and others. If you need to configure settings besides these, you'll need to provide a fully-specified `newrelic.yml`. See the [Using your own agent config file](#Using-your-own-agent-config-file) section for details.

### Using your own agent config file

If you need to specify agent configuration settings beyond those listed above, you'll need to provide your own `newrelic.yml` file. Any settings in the `nr_java_agent_config` dictionary will then be ignored. Set the variable `nr_java_agent_config_file` to the path to your file, for example:

```yaml
nr_java_agent_config_file: /path/to/your/newrelic.yml
```

If this file is on the target hosts instead of on the system running Ansible, set `nr_java_agent_config_file_is_remote` to true:

```yaml
nr_java_agent_config_file_is_remote: true
```

[1]: https://docs.newrelic.com/docs/agents/manage-apm-agents/app-naming/name-your-application
[2]: https://docs.newrelic.com/docs/agents/java-agent/configuration/java-agent-configuration-config-file#cfg-proxy_host
[3]: https://docs.newrelic.com/docs/agents/java-agent
[4]: https://docs.newrelic.com/docs/agents/java-agent/configuration/java-agent-configuration-config-file
