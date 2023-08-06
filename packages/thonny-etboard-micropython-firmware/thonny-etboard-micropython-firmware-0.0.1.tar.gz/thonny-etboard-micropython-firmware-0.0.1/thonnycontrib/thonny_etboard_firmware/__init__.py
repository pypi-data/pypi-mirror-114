import tkinter as tk
import os
import time
from glob import glob
from thonny import get_workbench, workbench
from tkinter.messagebox import showinfo
from thonny import ui_utils

class ETBoardMenu:
    def __init__(self):
        self.workbench = get_workbench()
        
    def __del__(self):
        pass

    def hello(self):
        #핸들러 테스트 함수
        showinfo("Hello!", "Thonny rules!")

    def _get_esptool_command(self):
        try:
            import esptool
            from thonny.running import get_interpreter_for_subprocess

            return [get_interpreter_for_subprocess(), "-u", "-m", "esptool"]
        except ImportError:
            import shutil

            result = shutil.which("esptool")
            if result:
                return [result]
            else:
                result = shutil.which("esptool.py")
                if result:
                    return [result]
                else:
                    return None


    def firmware_upload(self):
        from thonny.plugins import esp

        esptool_command = self._get_esptool_command()
        if not esptool_command:
            return

        dlg = esp.ESPFlashingDialog(
            self.workbench, "esp32", "0x1000", esptool_command
        )

        dir = os.path.dirname(__file__)
        dir = os.path.abspath(dir)
        firmware_path = glob(os.path.join(dir, "etboard", "firmware", "*.*"))
        if not firmware_path:
            showinfo("에러", "펌웨어를 찾을 수 없습니다")
            return

        dlg._firmware_entry.delete(0, "end")
        dlg._firmware_entry.insert(0, firmware_path[-1])
        ui_utils.show_dialog(dlg)

    def interpreter_select(self):
        from thonny import get_runner
        from thonny.plugins.micropython import list_serial_ports

        def get_port_list():
            port_info_list = {port.description : port.device for port in list_serial_ports()}

            return port_info_list

        def get_ch340_port():
            port_info_list = get_port_list()
            if not port_info_list:
                return ""

            for desc, device in port_info_list.items():
                if not desc or not device:
                    continue

                desc = desc.upper()
                if "CH340" in desc:
                    return device

            
            return ""


        self.workbench.set_option("run.backend_name", "ESP32")
        
        port_name = get_ch340_port()
        self.workbench.set_option("ESP32.port", port_name)
        get_runner().restart_backend(False)
        self.workbench.show_options("interpreter")
        
    def load_plugin(self):
        self.workbench.add_command(command_id="et-firmware",
                                menu_name="file",
                                command_label="ET-board 펌웨어 업로드",
                                handler=self.firmware_upload,
                                group=10)

        self.workbench.add_command(command_id="et-interpreter",
                                menu_name="file",
                                command_label="ET-board 인터프리터 설정",
                                handler=self.interpreter_select,
                                group=10)


        


if get_workbench() is not None:
    run = ETBoardMenu().load_plugin()
