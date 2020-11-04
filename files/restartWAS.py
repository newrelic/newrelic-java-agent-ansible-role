import sys

# Return matching servers, which will be restarted later in the script.
def findServers(name):
    mbeans = []
    servers = AdminControl.queryNames('type=Server,*').splitlines()
    for server in servers:
        # Confirming this is an application server, not a dmgr, nodeagent, etc.
        if (server.find('processType=UnManagedProcess') > -1) or (server.find('processType=ManagedProcess') > -1):
            if (name.lower() == 'all'):
                mbeans.append(server)
            else:
                serverName = AdminControl.getAttribute(server,"name")
                if (serverName.lower() == name.lower()):
                    mbeans.append(server)
    return mbeans

# Restart the application server (JVM)
def restartAppServer(server):
    print AdminControl.invoke(server, 'restart')

# JVM name must be passed in as an argument. If all is used we will attempt to restart all application servers (JVMs) returned by wsadmin.
serverName = sys.argv[0]

# Find the server, which will be used to find the node
servers = findServers(serverName)
if (len(servers) == 0):
    print("Error - Unable to find matching JVM!")
    sys.exit(2)
print("Servers: " + str(servers))

# Restart servers using AdminControl
for server in servers:
    restartAppServer(server)