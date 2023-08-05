#!/bin/bash

set -x
set -e

# Req
apt update
apt install -y --no-install-recommends wget gnupg hwloc


# Kwollect
# echo 'deb [trusted=yes] http://packages.grid5000.fr/deb/kwollect /' > /etc/apt/sources.list.d/kwollect.list
# apt update
# apt install -y kwollect
apt install -y --no-install-recommends python3-pip python3-setuptools python3-yarl
pip3 install -e /vagrant

# Database
echo "deb https://packagecloud.io/timescale/timescaledb/debian/ `lsb_release -c -s` main" > /etc/apt/sources.list.d/timescaledb.list
wget --quiet -O - https://packagecloud.io/timescale/timescaledb/gpgkey | apt-key add -
apt update
apt-get install -y postgresql postgresql-client libpq-dev timescaledb-2-postgresql-11 postgresql-plpython3-11

## TimescaleDB comes with a script to tune Postgres configuration that you might want to use:
cp /etc/postgresql/11/main/postgresql.conf /etc/postgresql/11/main/postgresql.conf-timescaledb_tune.backup
timescaledb-tune -yes -quiet
echo 'timescaledb.telemetry_level=off' >> /etc/postgresql/11/main/postgresql.conf

sed -i 's/max_connections.*/max_connections = 1000/g' /etc/postgresql/11/main/postgresql.conf

systemctl restart postgresql

# API
#wget -q https://github.com/PostgREST/postgrest/releases/download/v6.0.2/postgrest-v6.0.2-linux-x64-static.tar.xz -O /tmp/postgrest.txz
cd /tmp
tar xf postgrest.txz
chmod +x ./postgrest
mv ./postgrest /usr/local/bin/

cat > /etc/postgrest.conf << EOF
db-uri = "postgres://kwuser:changeme@localhost/kwdb"
db-schema = "api"
db-anon-role = "kwuser_ro"
jwt-secret = "changemechangemechangemechangemechangeme"
EOF

cat > /etc/systemd/system/postgrest.service << EOF
[Unit]
Description=Postgrest service
After=network.target

[Service]
ExecStart=/usr/local/bin/postgrest /etc/postgrest.conf

[Install]
WantedBy=multi-user.target
EOF

systemctl enable postgrest

# Kwollector
mkdir -p /etc/kwollect/metrics.d
cat > /etc/kwollect/kwollector.conf << EOF
# Path to directory containing metrics description
metrics_dir: /etc/kwollect/metrics.d/

# Hostname of postgresql server
db_host: localhost

# Database name
db_name: kwdb

# Database user
db_user: kwuser

# Database password
db_password: changeme

# Log level
log_level: warning
EOF


# Grafana
apt-get install -y apt-transport-https software-properties-common wget
echo "deb https://packages.grafana.com/oss/deb stable main" > /etc/apt/sources.list.d/grafana.list
wget -q -O - https://packages.grafana.com/gpg.key | apt-key add -
apt-get update
apt-get install grafana

sed -i 's/.*http_port.*/http_port = 3003/g' /etc/grafana/grafana.ini
cp /vagrant/grafana/postgres_datasource.yaml /etc/grafana/provisioning/datasources/postgres.yaml
cp /vagrant/grafana/kwollect_dashboardsource.yaml /etc/grafana/provisioning/dashboards/kwollect.yaml
mkdir -p /etc/grafana/kwollect_dashboard
ln -sf /vagrant/grafana/kwollect_dashboard.json /etc/grafana/kwollect_dashboard/

systemctl start grafana-server
systemctl enable grafana-server
