#!/bin/bash
xhost +

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

CCACHE_DIR="${HOME}/.ccache"
mkdir -p "$CCACHE_DIR"
ROBOT_VERSION=45
DIR_HASH=$(echo "$PARENT_DIR" | md5sum | cut -c1-8)
echo "Directory $PARENT_DIR hash: $DIR_HASH"
# 使用用户名区分容器，避免多用户冲突
CURRENT_USER=$(whoami)
CONTAINER_NAME="kuavo_container_GPU_${CURRENT_USER}_${DIR_HASH}"
# 自动使用最新的镜像版本
IMAGE_NAME=$(docker images kuavo_opensource_mpc_wbc_img --format "{{.Repository}}:{{.Tag}}" | sort -V | tail -n1)

if [[ -z "$IMAGE_NAME" ]]; then
    echo -e "\033[33mWarning: No 'kuavo_opensource_mpc_wbc_img' Docker image found.\033[0m"
    read -r -p "The script can attempt to automatically download and import the image. Would you like to proceed? (yes/no): " response
    if [[ "$response" =~ ^([yY][eE][sS])$ ]]; then
        echo "Attempting to download/import 'kuavo_opensource_mpc_wbc_img'..."
        IMAGE_TARBALL_URL="https://kuavo.lejurobot.com/docker_images/kuavo_opensource_mpc_wbc_img_latest.tar.gz"
        IMAGE_TARBALL_NAME="kuavo_opensource_mpc_wbc_img_latest.tar.gz"
        DOWNLOAD_PATH="${SCRIPT_DIR}/${IMAGE_TARBALL_NAME}"

        echo "Downloading Docker image from ${IMAGE_TARBALL_URL}..."
        if wget -O "${DOWNLOAD_PATH}" "${IMAGE_TARBALL_URL}"; then
            echo "Download successful. Loading image into Docker..."
            if sudo docker load -i "${DOWNLOAD_PATH}"; then
                echo "Docker image loaded successfully."
                # Clean up the downloaded tarball
                rm -f "${DOWNLOAD_PATH}"
                # Re-evaluate IMAGE_NAME
                IMAGE_NAME=$(docker images kuavo_opensource_mpc_wbc_img --format "{{.Repository}}:{{.Tag}}" | sort -V | tail -n1)
                if [[ -z "$IMAGE_NAME" ]]; then
                    echo -e "\033[31mError: Failed to find the image name even after loading. Please check the image details.\033[0m"
                    exit 1
                else
                    echo -e "\033[32mSuccessfully loaded image: ${IMAGE_NAME}\033[0m"
                fi
            else
                echo -e "\033[31mError: Failed to load Docker image from ${DOWNLOAD_PATH}.\033[0m"
                rm -f "${DOWNLOAD_PATH}" # Clean up even on failure
                exit 1
            fi
        else
            echo -e "\033[31mError: Failed to download Docker image from ${IMAGE_TARBALL_URL}.\033[0m"
            exit 1
        fi
    else
        echo "Okay. Please build or pull the 'kuavo_opensource_mpc_wbc_img' image manually."
        echo "You can typically do this by navigating to the docker directory and running a build script (e.g., './build.sh'), or by pulling it from a registry."
        exit 1
    fi
fi

show_container_info() {
    local div_line="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "\n$div_line"
    echo -e " \033[34mContainer Info\033[0m: $CONTAINER_NAME"
    echo -e " \033[32mWorking Directory\033[0m:"
    echo -e "   $PARENT_DIR"
    echo -e " \033[33mMounted Volumes\033[0m:"
    # docker inspect -f '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}' $CONTAINER_NAME

    docker inspect -f '{{range .Mounts}}   {{.Source}} → {{.Destination}}{{println}}{{end}}' $CONTAINER_NAME
    echo -e "$div_line\n"
}

# 检测 PulseAudio socket 路径
USER_ID=$(id -u)
PULSE_SOCKET="/run/user/${USER_ID}/pulse/native"

# 检查主机 PulseAudio 状态
if ! pgrep -x pulseaudio > /dev/null; then
    echo -e "\033[33m⚠️  Warning: PulseAudio is not running on host.\033[0m"
    echo "Starting PulseAudio..."
    pulseaudio --start 2>/dev/null
    sleep 2
fi

if [[ ! -S "$PULSE_SOCKET" ]]; then
    echo -e "\033[33m⚠️  Warning: PulseAudio socket not found at $PULSE_SOCKET\033[0m"
    # 尝试查找备用 socket 路径
    PULSE_SOCKET=$(find /run/user/${USER_ID}/pulse -name "native" 2>/dev/null | head -1)
    if [[ -z "$PULSE_SOCKET" ]]; then
        echo -e "\033[31mError: Cannot find PulseAudio socket. Audio may not work.\033[0m"
        echo "Please ensure PulseAudio is running: pulseaudio --start"
    else
        echo -e "\033[32mFound PulseAudio socket at: $PULSE_SOCKET\033[0m"
    fi
fi

# 获取 audio 组 GID
AUDIO_GID=$(getent group audio | cut -d: -f3)
if [[ -z "$AUDIO_GID" ]]; then
    echo -e "\033[33mWarning: audio group not found. Audio permissions may be limited.\033[0m"
    AUDIO_GID=29  # 默认值
fi

# 检查是否存在同名容器
EXISTING_CONTAINER=$(docker ps -aq -f name=^/${CONTAINER_NAME}$)

if [[ -n "$EXISTING_CONTAINER" ]]; then
    echo "Container '${CONTAINER_NAME}' already exists."
    
    # 检查容器是否已挂载音频
    PULSE_MOUNTED=$(docker inspect $CONTAINER_NAME | grep -o "/run/user/${USER_ID}/pulse" | head -1)
    AUDIO_DEVICE=$(docker inspect $CONTAINER_NAME | grep -o '"/dev/snd"' | head -1)
    
    if [[ -z "$PULSE_MOUNTED" ]] || [[ -z "$AUDIO_DEVICE" ]]; then
        echo -e "\033[33m⚠️  Warning: Audio devices are not properly mounted in this container.\033[0m"
        echo -e "\033[33m   The container was created without audio support.\033[0m"
        echo ""
        read -r -p "Do you want to recreate the container with audio support? (yes/no): " recreate_response
        
        if [[ "$recreate_response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            echo "Stopping and removing container '$CONTAINER_NAME' ..."
            docker stop $CONTAINER_NAME >/dev/null 2>&1
            docker rm $CONTAINER_NAME >/dev/null 2>&1
            echo "Container removed. Will create new container with audio support..."
            EXISTING_CONTAINER=""  # 清空标记,继续执行创建逻辑
        else
            echo "Continuing with existing container (without audio support)..."
        fi
    else
        echo -e "\033[32m✓ Audio devices are properly mounted.\033[0m"
    fi
    
    # 如果容器仍然存在(用户选择不重建),则进入容器
    if [[ -n "$EXISTING_CONTAINER" ]]; then
        # 检查容器是否正在运行
        CONTAINER_STATUS=$(docker inspect -f '{{.State.Status}}' $CONTAINER_NAME 2>/dev/null)
        
        if [[ "$CONTAINER_STATUS" == "exited" ]] || [[ "$CONTAINER_STATUS" == "created" ]]; then
            echo "Starting container '$CONTAINER_NAME' ..."
            docker start $CONTAINER_NAME
            # 等待容器完全启动
            sleep 1
        elif [[ "$CONTAINER_STATUS" == "running" ]]; then
            echo "Container '$CONTAINER_NAME' is already running."
        else
            echo -e "\033[31mError: Container status is '$CONTAINER_STATUS'. Please check container manually.\033[0m"
            exit 1
        fi
        
        # 自动修改容器内的 ROBOT_VERSION 环境变量
        echo "Updating ROBOT_VERSION to 45 in container..."
        docker exec $CONTAINER_NAME bash -c "
            if grep -q '^export ROBOT_VERSION=' /root/.zshrc; then
                sed -i 's/^export ROBOT_VERSION=.*/export ROBOT_VERSION=45/' /root/.zshrc
            elif grep -q 'export ROBOT_VERSION=' /root/.zshrc; then
                sed -i 's/export ROBOT_VERSION=.*/export ROBOT_VERSION=45/' /root/.zshrc
            else
                echo '' >> /root/.zshrc
                echo '# Auto-configured by docker script' >> /root/.zshrc
                echo 'export ROBOT_VERSION=45' >> /root/.zshrc
            fi
        "
        
        show_container_info
        echo "Exec into container '$CONTAINER_NAME' ..."
        docker exec -it $CONTAINER_NAME zsh
        exit 0
    fi
fi

# 创建新容器
if [[ -z "$EXISTING_CONTAINER" ]]; then
    echo "Creating a new container '${CONTAINER_NAME}' based on image '${IMAGE_NAME}' ..."
    
    # 为每个容器分配独立的 ROS Master 端口（将十六进制哈希转换为十进制）
    DIR_HASH_DEC=$((16#${DIR_HASH}))
    USER_HASH=$(echo "$CURRENT_USER" | md5sum | cut -c1-4)
    USER_HASH_DEC=$((16#${USER_HASH}))
    PORT_OFFSET=$(( (DIR_HASH_DEC + USER_HASH_DEC) % 1000 ))
    ROS_MASTER_PORT=$((11311 + PORT_OFFSET))
    GAZEBO_MASTER_PORT=$((11345 + PORT_OFFSET))
    echo "Using ROS_MASTER_URI: http://localhost:${ROS_MASTER_PORT}"
    echo "Using GAZEBO_MASTER_URI: http://localhost:${GAZEBO_MASTER_PORT}"
    
	docker run -it --net host --gpus all \
		--runtime nvidia \
        --name $CONTAINER_NAME \
		--privileged \
		-v /dev:/dev \
		-v "$CCACHE_DIR:/root/.ccache" \
		-v "$PARENT_DIR:/root/kuavo_ws" \
		-v "${HOME}/.config/lejuconfig:/root/.config/lejuconfig" \
		-v "/run/user/${USER_ID}/pulse:/run/user/${USER_ID}/pulse:rw" \
		-v "${HOME}/.config/pulse:/root/.config/pulse:ro" \
        -e NVIDIA_VISIBLE_DEVICES=all \
        -e NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics,display \
        -e __NV_PRIME_RENDER_OFFLOAD=1 \
        -e __GLX_VENDOR_LIBRARY_NAME=nvidia \
        -e CARB_GRAPHICS_API=vulkan \
        -e GDK_SYNCHRONIZE=1 \
		-e PULSE_SERVER=unix:/run/user/${USER_ID}/pulse/native \
		-e PULSE_COOKIE=/run/user/${USER_ID}/pulse/cookie \
		-e XDG_RUNTIME_DIR=/run/user/${USER_ID} \
		-e HOME=/root \
		-e ROS_MASTER_URI=http://localhost:${ROS_MASTER_PORT} \
		-e GAZEBO_MASTER_URI=http://localhost:${GAZEBO_MASTER_PORT} \
		-e GAZEBO_IP=127.0.0.1 \
		-e GAZEBO_MASTER_IP=127.0.0.1 \
		-e IGN_PARTITION=${CONTAINER_NAME} \
		--device /dev/snd \
		--group-add=${AUDIO_GID} \
		--group-add=dialout \
		--group-add=video \
		--ulimit rtprio=99 \
		--cap-add=sys_nice \
		--ipc=private \
		-e DISPLAY=$DISPLAY \
		-e ROBOT_VERSION=45 \
		--volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
		${IMAGE_NAME} \
		bash -c "
			chmod -R 777 /run/user/${USER_ID}/pulse 2>/dev/null || true
			# 修改 .zshrc 中的 ROBOT_VERSION 和 ROS/Gazebo 端口
			if grep -q '^export ROBOT_VERSION=' /root/.zshrc; then
				sed -i 's/^export ROBOT_VERSION=.*/export ROBOT_VERSION=45/' /root/.zshrc
			elif grep -q 'export ROBOT_VERSION=' /root/.zshrc; then
				sed -i 's/export ROBOT_VERSION=.*/export ROBOT_VERSION=45/' /root/.zshrc
			else
				echo '' >> /root/.zshrc
				echo '# Auto-configured by docker script' >> /root/.zshrc
				echo 'export ROBOT_VERSION=45' >> /root/.zshrc
			fi
			
			# 设置独立的 ROS/Gazebo Master URI
			sed -i '/ROS_MASTER_URI/d' /root/.zshrc 2>/dev/null || true
			sed -i '/GAZEBO_MASTER_URI/d' /root/.zshrc 2>/dev/null || true
			echo \"export ROS_MASTER_URI=http://localhost:${ROS_MASTER_PORT}\" >> /root/.zshrc
			echo \"export GAZEBO_MASTER_URI=http://localhost:${GAZEBO_MASTER_PORT}\" >> /root/.zshrc
			
			exec zsh
		"
fi
