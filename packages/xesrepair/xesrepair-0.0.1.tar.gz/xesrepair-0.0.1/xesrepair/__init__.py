import subprocess
import sys
PACKAGE_NAME = 'xesrepair'
name = PACKAGE_NAME
from xesrepair.common import PYTHONW_EXE, USER_LIB_PATH, create_python_process

SHOW_BUTTON = False # 是否在学而思编程助手的托盘处进行清理
class RepairHandler:
    def __init__(self):
        self._modules = ['numpy', 'imageio'] # 待检查的库

    def check_common (self, name):
        try:
            import importlib
            check_module = importlib.import_module(name)

            importlib.reload(sys.modules[name])
            # except Exception as e:
            #     print(e)
            print(check_module.__version__)
            return {"state": True}
        except Exception as e:
            print("check error:"+str(e))
            return {"state": False, "reason": str(e)}
    
    def repair_common (self, name):
        res = self.check_common(name)
        print("通用修复的检查结果是", res)
        if  res['state']:
            return
        # 先卸载
        uninstall_args = [PYTHONW_EXE, "-m", "pip", "uninstall", "-y", name]
        create_python_process(uninstall_args)
        # 再安装
        install_args = [PYTHONW_EXE, "-m", "pip", "install",'--target', USER_LIB_PATH, name, '--no-cache-dir', '--no-warn-script-location', "--index-url", 'https://mirrors.aliyun.com/pypi/simple/', "--upgrade" ]
        create_python_process(install_args)
         


    def run (self):
        for module in self._modules:
            print("开始检测", module)
            try:
                import importlib
                check_module = importlib.import_module(PACKAGE_NAME+".repair_"+module)
                check_module.repair()
                # return {"state": True}
            except Exception as e:
                print(module + ".run() error:"+str(e))
                self.repair_common(module)
            print("检测结束", module)