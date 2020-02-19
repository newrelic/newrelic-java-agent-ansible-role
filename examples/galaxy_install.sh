BUILD_DIR=build
ROLE_FILE=$BUILD_DIR/newrelic_java_agent_role.tar.gz
ROLE_INSTALL_FILE=$BUILD_DIR/local_role_install.yml

mkdir -p $BUILD_DIR
tar --exclude=build -zcf $ROLE_FILE .
cat << EOF > $ROLE_INSTALL_FILE
- src: $ROLE_FILE
  name: newrelic_java_agent
EOF
ansible-galaxy install -f -r $ROLE_INSTALL_FILE
