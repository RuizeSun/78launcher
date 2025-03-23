import os, settings, requests, logging, json, shutil, _thread, webbrowser
from tkinter.messagebox import *

# 初始化
directory = os.getcwd()+"\\78launcher\\"
logger = logging.getLogger("LauncherOperationCore")
version = [2,"1.0.0-beta.2"]

# 启动器版本检测
def launcherVersionCheck():
    global version
    logger.info("现在将检查启动器版本。")
    launcherConfig = json.loads(requests.get("http://www.78go.work/resources/launcher/launcherConfig.json").text)
    if launcherConfig["launcher"]["version"] > version[0]:
        logger.warning("有新的启动器版本。")
        if askyesno("更新提示",f"有新的启动器版本，是否更新？\n{version[1]} → {launcherConfig["launcher"]["displayName"]}\n更新内容：\n{"\n".join(launcherConfig["launcher"]["changelog"])}"):
            webbrowser.open(launcherConfig["launcher"]["downloadPage"])

# 下载
def checkMinecraft(ignore=False):
    try:
        if ignore:
            temp = settings.getSettings()
            temp["currentModpackVersion"] = 0
            settings.writeSettings(temp)
        launcherConfig = json.loads(requests.get("http://www.78go.work/resources/launcher/launcherConfig.json").text)
        if launcherConfig["modpack"]["version"] > settings.getSettings()["currentModpackVersion"]:
            logger.info("本地 Minecraft 模组包版本低于现行版本，即将开始安装/更新本地模组包。")
            if os.path.exists(os.getcwd()+"\\.minecraft\\versions\\"):
                shutil.rmtree(os.getcwd()+"\\.minecraft\\versions\\")
            if os.path.exists(directory+".cmcl\\modpacks\\"):
                shutil.rmtree(directory+".cmcl\\modpacks\\")
            logger.info("已经打开安装程序。")
            os.system(f"@echo 正在安装/更新本地 Minecraft 模组包，请勿关闭本窗口！&& @echo {settings.getSettings()["currentModpackVersionDisplay"]} → {launcherConfig["modpack"]["displayName"]} && @echo {" && @echo ".join(launcherConfig["modpack"]["changelog"])} && {directory}cmcl.exe modpack --url={launcherConfig["modpack"]["downloadUrl"]} --storage=78787878")
            settingsconfig = settings.getSettings()
            settingsconfig["currentModpackVersion"] = launcherConfig["modpack"]["version"]
            settingsconfig["currentModpackVersionDisplay"] = launcherConfig["modpack"]["displayName"]
            settings.writeSettings(settingsconfig)
        else:
            logger.info("本地 Minecraft 模组包不必更新。")
    except:
        logger.error("检查 Minecraft 版本时出现错误。",exc_info=True)

# 启动
def launch(playerName, serverip):
    with open(f"{directory}cmcl.json","w") as f:
        f.write(json.dumps({ "exitWithMinecraft": True, "windowSizeWidth": 854, "windowSizeHeight": 480, "language": "zh", "downloadSource": 0, "accounts": [{ "playerName": playerName, "loginMethod": 0, "selected": True }], "checkAccountBeforeStart": False, "printStartupInfo": True, "qpServerAddress":serverip }))
    os.system(f"{directory}cmcl.exe 78787878")

_thread.start_new_thread(launcherVersionCheck, ())
logger.info("启动器操作核心加载完毕。")
