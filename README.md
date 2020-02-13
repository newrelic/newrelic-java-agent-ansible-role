# New Relic Java agent Ansible role

## Description

This role installs and configures the [New Relic Java agent][3]. It should work with minimal configuration for applications running under Tomcat. Our aim is to support many of the most popular Java web servers over time.

## Requirements

Requires unzip to be available on the target hosts.

## Role Variables

### Agent configuration

Configuration specific to the agent goes in the `nr_agent_config` dictionary.

#### license_key (REQUIRED)

Your New Relic license key.

#### app_name (REQUIRED)

The name of the application being instrumented. See the [documentation on app naming][1] for more details.

#### proxy_host, proxy_port, proxy_user, proxy_password, proxy_scheme (OPTIONAL)

If you connect to the New Relic collector via a proxy, you can configure that with these values. See [the documentation on configuring the Java agent][2] for more details.

### Role configuration

Other variables are used to control the installation of the agent.

#### server_type (REQUIRED)

The web server used by your application. Tomcat is supported out of the box; Jetty support is present but not yet tested.

#### app_root (REQUIRED)

The location of the web server on the host; the agent's jar, configuration, and log files will live in a subdirectory of this directory.

#### jvm_conf_file (REQUIRED)

The path to the file with which the web server will be configured to use the New Relic Java agent. For Tomcat, for instance, this is the `setenv.sh` file. The file will be created if necessary.

#### server_user, server_group (REQUIRED)

The user and group under which the web server runs; will be used to set the ownership of the `newrelic.jar` and `newrelic.yml` files.

#### restart_web_server (OPTIONAL, default true)

If defined to false, the role will _not_ restart the web server after installing the agent. NOTE: the agent will not be activated until the web server is restarted.

#### service_name (REQUIRED, unless restart_web_server is set to false)

The service name under which the web server runs; used by ansible to restart the web server after the agent is installed.

#### staging (NEW RELIC INTERNAL USE ONLY)

If staging is set to true, the agent will use New Relic's internal staging collector. This option is only available for use at New Relic.

## Example usage

The `examples/install_agent.yml` file, along with `examples/inventory.yml`, provide an example of how to use the role.

[1]: https://docs.newrelic.com/docs/agents/manage-apm-agents/app-naming/name-your-application
[2]: https://docs.newrelic.com/docs/agents/java-agent/configuration/java-agent-configuration-config-file#cfg-proxy_host
[3]: https://docs.newrelic.com/docs/agents/java-agent
