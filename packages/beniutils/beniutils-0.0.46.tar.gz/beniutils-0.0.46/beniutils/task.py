import sys
import time

import beniutils as b

projectPath = None
workspacePath = None


def init(pPath, wPath):
    global projectPath
    global workspacePath
    projectPath = pPath
    workspacePath = wPath


def getPathByProject(*parList):
    return b.getPath(projectPath, *parList)


def getPathByWorkspace(*parList):
    return b.getPath(workspacePath, *parList)


isAllowRunMain = True


def runMain(moduleName=None, **parDict):
    global isAllowRunMain
    if isAllowRunMain:
        isAllowRunMain = False
        isError = False
        lockFile = b.getPath(workspacePath, "tool.lock")
        b.checkLockFile(lockFile)
        isDebug = not not moduleName
        try:
            logFolder = b.getPath(workspacePath, "log")
            b.makeFolder(logFolder)
            for logFile in sorted(b.getAllFileList(logFolder), reverse=True)[100:]:
                b.remove(logFile)
            logFile = b.getPath(logFolder, f"{time.strftime('%Y%m%d_%H%M%S')}.log")
            b.initLogger(logFile=logFile)
            if not moduleName:
                moduleName, parDict = initParDict()
            run(moduleName, **parDict)
        except Exception:
            isError = True
            import traceback
            traceback.print_exc()
            b.error("执行失败")
        finally:
            b.remove(lockFile)
        if not isDebug and isError:
            sys.exit(1)
    else:
        raise Exception("不允许重复执行 runMain")


def run(moduleName, **parDict):
    exec(f"import {moduleName}")
    module = eval(moduleName)
    try:
        for k, v in parDict.items():
            if hasattr(module, k):
                setattr(module, k, v)
            else:
                b.warning(f"模块缺少属性定义 module={moduleName} k={k} v={v}")
        module.run()
    except Exception as e:
        raise e
    finally:
        if hasattr(module, "clean"):
            module.clean()


def initParDict():
    ary = sys.argv
    if len(ary) < 2:
        raise Exception("执行异常，参数长度小于2")
    moduleName = ary[1]
    parList = ary[2:]
    parDict = {}
    index = 0
    while index < len(parList):
        par = parList[index]
        if par.startswith("--"):
            index += 1
            try:
                parValue = parList[index]
            except:
                parValue = None
            parName = par[2:]
            if parName in parDict:
                raise Exception("发现有重复参数名")
            parDict[parName] = parValue
        index += 1
    return moduleName, parDict
