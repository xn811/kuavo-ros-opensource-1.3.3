#!/bin/bash

set -e

# 日志函数
log() {
    echo "[`date '+%F %T'`] $1"
}

log "🔍 检查网卡信息..."

# 自动查找网段为 192.168.26.X 的网卡
INTERFACE=$(ifconfig | grep -B1 "192.168.26" | head -n1 | awk -F: '{print $1}' | xargs)

if [ -z "$INTERFACE" ]; then
    log "❌ 没有找到匹配 192.168.26.X 网段的网卡，退出。"
    exit 1
fi

log "检测到目标网卡：$INTERFACE"

# 固定配置
SUBNET="192.168.26.0"
NETMASK="255.255.255.0"
ROUTER="192.168.26.1"
POOL_START="192.168.26.12"
POOL_END="192.168.26.12"
LEASE_TIME="600"

log "安装 isc-dhcp-server..."
sudo apt update
sudo apt install -y isc-dhcp-server

log "配置绑定网卡..."
sudo sed -i "s/^INTERFACESv4=\".*\"/INTERFACESv4=\"$INTERFACE\"/" /etc/default/isc-dhcp-server

# 检查 dhcpd.conf 文件是否存在
if [ -f "/etc/dhcp/dhcpd.conf" ]; then
    log "配置文件已存在，正在检查是否需要添加或修改配置..."

    # 检查是否已经包含相同的配置（通过匹配某些关键字）
    if grep -q "subnet $SUBNET netmask $NETMASK" /etc/dhcp/dhcpd.conf; then
        log "配置已存在，检查 range 配置..."

        # 检查是否包含正确的 range 配置
        if ! grep -q "range $POOL_START $POOL_END" /etc/dhcp/dhcpd.conf; then
            log "❌ 找到不匹配的 range 配置，正在修改为正确的 range：$POOL_START $POOL_END"
            # 使用 sed 修改 range 配置
            sudo sed -i "s/range .*/range $POOL_START $POOL_END;/g" /etc/dhcp/dhcpd.conf
            log "range 配置已更新为：$POOL_START $POOL_END"
        else
            log "range 配置正确，无需修改"
        fi
    else
        log "配置文件没有找到目标网段配置，正在追加新的配置..."
        # 如果没有配置，追加新配置
        sudo tee -a /etc/dhcp/dhcpd.conf > /dev/null <<EOF

subnet $SUBNET netmask $NETMASK {
  range $POOL_START $POOL_END;
  option routers $ROUTER;
  option subnet-mask $NETMASK;
}
EOF
        log "新的 DHCP 配置已添加到 /etc/dhcp/dhcpd.conf"
    fi
else
    log "配置文件不存在，正在创建新的 /etc/dhcp/dhcpd.conf..."

    # 创建并写入新的配置
    sudo tee /etc/dhcp/dhcpd.conf > /dev/null <<EOF
default-lease-time $LEASE_TIME;
max-lease-time $((LEASE_TIME * 2));
authoritative;

subnet $SUBNET netmask $NETMASK {
  range $POOL_START $POOL_END;
  option routers $ROUTER;
  option subnet-mask $NETMASK;
}
EOF
    log "新的 DHCP 配置已生成并写入 /etc/dhcp/dhcpd.conf"
fi

log "设置网卡 $INTERFACE 静态 IP 为 $ROUTER..."
sudo ip addr flush dev $INTERFACE
sudo ip addr add $ROUTER/24 dev $INTERFACE
sudo ip link set $INTERFACE up

log "启动 DHCP 服务..."
sudo systemctl restart isc-dhcp-server
sudo systemctl enable isc-dhcp-server

log "DHCP 服务部署完成，监听网卡：$INTERFACE，分配地址：$POOL_START"
