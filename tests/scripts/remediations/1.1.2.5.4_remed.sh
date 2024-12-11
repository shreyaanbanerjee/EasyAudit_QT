#!/usr/bin/env bash

# Check if /var/tmp is a separate partition
var_tmp_partition=$(findmnt -kn /var/tmp)

if [[ -n "$var_tmp_partition" ]]; then
    # Add noexec to the fourth field in /etc/fstab for /var/tmp partition
    echo "Editing /etc/fstab to add noexec option for /var/tmp partition..."
    sudo sed -i 's|\(/var/tmp.*defaults.*\)|\1,noexec|' /etc/fstab

    # Remount /var/tmp with the configured options
    echo "Remounting /var/tmp with the configured options..."
    sudo mount -o remount /var/tmp

    echo "The /var/tmp partition has been remounted with the noexec option."
else
    echo "No separate partition found for /var/tmp."
fi
