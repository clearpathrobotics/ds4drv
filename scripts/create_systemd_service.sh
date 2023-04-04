#!/bin/bash
SYSTEMD_SCRIPT_DIR=$( cd  $(dirname "${BASH_SOURCE:=$0}") && pwd)
cp -f "$SYSTEMD_SCRIPT_DIR/super-project.service" /lib/systemd/system
chown root:root /lib/systemd/system/super-project.service

systemctl daemon-reload
systemctl enable super-project.service