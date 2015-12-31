set -eux

DIR="$(dirname `readlink -f $0`)"
TARGET="/opt"
onos_home="/opt/onos"
onos=http://205.177.226.235:9999/onosfw/onos-1.3.0.tar.gz
jdk=http://205.177.226.235:9999/onosfw/jdk-8u51-linux-x64.tar.gz
repo=http://205.177.226.235:9999/onosfw/repository.tar
karaf_dist="apache-karaf-3.0.3"
onos_pkg_name="onos-1.3.0.tar.gz"
jdk8_pkg_name="jdk-8u51-linux-x64.tar.gz"
onos_boot_features="config,standard,region,package,kar,ssh,management,webconsole,onos-api,onos-core,onos-incubator,onos-cli,onos-rest,onos-gui,onos-openflow-base,onos-openflow"
HOME="/root"

cd $TARGET
if [ ! -f "onos_pack.tar" ]
then
  wget  $onos -P $TARGET
  wget  $jdk -P $TARGET
  wget  $repo -P $TARGET
else
  tar xf onos_pack.tar
fi

groupadd onos -r
adduser --system --home $onos_home --group onos


mkdir $HOME/.m2
mv $TARGET/repository.tar $HOME/.m2/

tar -zvxf /opt/$onos_pkg_name -C $onos_home  --strip-components 1 --no-overwrite-dir -k;
tar xf $HOME/.m2/repository.tar -C $HOME/.m2/


echo 'export ONOS_OPTS=debug' > /opt/onos/options;
echo 'export ONOS_USER=root' >> /opt/onos/options;
mkdir /opt/onos/var;
mkdir /opt/onos/config;

#jdk config

mkdir /usr/lib/jvm/
tar -xzf /opt/jdk-8u*-linux-x64.tar.gz -C /usr/lib/jvm/
mv /usr/lib/jvm/jdk1.8.0_* /usr/lib/jvm/java-8-oracle

touch /etc/profile.d/jdk.csh
cat <<EOT>> /etc/profile.d/jdk.csh
setenv J2SDKDIR /usr/lib/jvm/java-8-oracle
setenv J2REDIR /usr/lib/jvm/java-8-oracle/jre
setenv PATH ${PATH}:/usr/lib/jvm/java-8-oracle/bin:/usr/lib/jvm/java-8-oracle/db/bin:/usr/lib/jvm/java-8-oracle/jre/bin
setenv JAVA_HOME /usr/lib/jvm/java-8-oracle
setenv DERBY_HOME /usr/lib/jvm/java-8-oracle/db
EOT

touch /etc/profile.d/jdk.sh
cat <<EOT>> /etc/profile.d/jdk.sh
export J2SDKDIR=/usr/lib/jvm/java-8-oracle
export J2REDIR=/usr/lib/jvm/java-8-oracle/jre
export PATH=$PATH:/usr/lib/jvm/java-8-oracle/bin:/usr/lib/jvm/java-8-oracle/db/bin:/usr/lib/jvm/java-8-oracle/jre/bin
export JAVA_HOME=/usr/lib/jvm/java-8-oracle
export DERBY_HOME=/usr/lib/jvm/java-8-oracle/db
EOT

chmod +x /etc/profile.d/jdk*



service onos start 
sleep 100
#service onos restart
#sleep 60
service onos stop

