import sys

# This should be invoked by an Ansible handler and only on the wsadmin_primary node

# Get cell name
def getCellName():
    cell = AdminConfig.list("Cell")
    cellName = AdminConfig.showAttribute(cell,"name")
    return str(cellName)

# Find server
def findServer(name):
    servers = AdminTask.listServers("[-serverType APPLICATION_SERVER]").splitlines()
    for server in servers:
        serverName = AdminConfig.showAttribute(server,"name")
        if (serverName == name):
            return str(server)

# Get cluster name
def getClusterName(server):
    clusterName = AdminConfig.showAttribute(server,"clusterName")
    return str(clusterName)

# Get cluster mbean
def getClusterMbean(cell, clusterName):
    mbean = AdminControl.completeObjectName("cell="+cell+",type=Cluster,name="+clusterName+",*")
    return str(mbean)

# Ripple start cluster
# This command completes quickly, but the actual ripple start can take several minutes to complete.
def rippleStart(cluster):
    print AdminControl.invoke(cluster, "rippleStart")

# JVM name must be passed in as an argument
serverName = sys.argv[0]

# Get the cell name. This will be used later to find the cluster mbean
cell = getCellName()
if cell is None:
    print("Error - Unable to find cell name. Is server clustered?")
    sys.exit(1)
print("Cell name: " + cell)
# Find the server, which will be used to find the cluster
server = findServer(serverName)
if server is None:
    print("Error - Unable to find matching JVM!")
    sys.exit(2)
print("Server: " + server)
clusterName = getClusterName(server)
if clusterName is None:
    print("Error - Unable to find cluster name for JVM. Is server clustered?")
    sys.exit(3)
print("Cluster name: " + clusterName)
cluster = getClusterMbean(cell, clusterName)
print("Cluster mbean: "+ cluster)
if cluster is None:
    print("Error - Unable to find cluster mbean for cluster: " + clusterName)
    sys.exit(4)
# Ripple start the cluster
rippleStart(cluster)