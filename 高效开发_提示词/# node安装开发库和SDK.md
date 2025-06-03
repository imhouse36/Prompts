# 安装 pkg-config 和相关开发库
sudo apt update

# 安装必要的系统依赖
sudo apt install -y pkg-config libsecret-1-dev build-essential

#安装 CLI
npm install @lark-opdev/cli@latest -g -f

#安装 NodeJS SDK
npm install @larksuiteoapi/node-sdk

#初始化项目
npm install