import sys

# Return matching servers, which will be restarted later in the script.
def findServers(name):
    mbeans = []
    servers = AdminConfig.list("Server").splitlines()
    for server in servers:
        serverType = AdminConfig.showAttribute(server,"serverType")
        if serverType == "APPLICATION_SERVER":
            if name.lower() == 'all':
                objectName = AdminConfig.getObjectName(server)
                # Object name may return a 0 length string if the server is restarting.
                if len(objectName) > 0:
                    mbeans.append(objectName)
                continue
            clusterName = AdminConfig.showAttribute(server,"clusterName")
            if clusterName != None:
                if (clusterName.lower() == name.lower()):
                    objectName = AdminConfig.getObjectName(server)
                    if len(objectName) > 0:
                        mbeans.append(objectName)
                    continue
            serverName = AdminConfig.showAttribute(server,"name")
            if (serverName.lower() == name.lower()):
                objectName = AdminConfig.getObjectName(server)
                if len(objectName) > 0: 
                    mbeans.append(objectName)
    return mbeans

# Restart the application server (JVM)
def restartAppServer(server):
    print AdminControl.invoke(server, 'restart')

# JVM name must be passed in as an argument. If all is used we will attempt to restart all application servers (JVMs) returned by wsadmin.
serverName = sys.argv[0]

# Find the server, which will be used to find the node
servers = findServers(serverName)
if (len(servers) == 0):
    print("Unable to find matching JVM! Nothing will be restarted")
print("Servers: " + str(servers))

# Restart servers using AdminControl
for server in servers:
    print("Restarting server: " + str(server))
    restartAppServer(server)