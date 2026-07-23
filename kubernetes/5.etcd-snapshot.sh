export ETCDCTL_API=3
BACKUP_DIR="$HOME/etcd-backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
mkdir -p "$BACKUP_DIR"
sudo etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save "$BACKUP_DIR/etcd-snapshot-$TIMESTAMP.db"

echo "Snapshot saved under $BACKUP_DIR"
sudo etcdctl snapshot status "$BACKUP_DIR/etcd-snapshot-$TIMESTAMP.db" -w table