import sys
from PySide6.QtWidgets import QApplication, QStackedWidget, QFileDialog
from PySide6 import QtWidgets, QtCore
from PySide6.QtUiTools import QUiLoader
import platform
import os, datetime
import subprocess
import sqlite3
import json
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
import database

def bitlocker_status():
    if platform.system() == "Windows":
        new_audit_page.bitlocker_btn.setEnabled(True)
    else:
        new_audit_page.bitlocker_btn.setEnabled(False)

def check_os():
    # Check if the system is Linux
    if platform.system() == "Linux":
        # Try to determine if it's Ubuntu or rhel_9
            with open("/etc/os-release", "r") as f:
                os_info = f.read()
            if "Ubuntu" in os_info:
                return "Ubuntu"
            elif "Red Hat" in os_info or "rhel_9" in os_info or "fedora" in os_info:
                return "rhel_9"
            else:
                return "Windows"
    else:
        return "Windows"

def open_cis_website():
    QDesktopServices.openUrl(QUrl("https://www.cisecurity.org/"))

###START PAGE INFORMATION###

def get_clean_linux_version():
    try:
        with open("/etc/os-release", "r") as file:
            for line in file:
                if line.startswith("PRETTY_NAME="):
                    return line.split("=")[1].strip().replace('"', '')
    except FileNotFoundError:
        return platform.system()

def get_system_info():
    os_name = platform.system()
    hostname = os.uname()[1] if hasattr(os, 'uname') else platform.node()
    os_version = None
    kernel_version = None
    machine_arch = None
    processor = None

    if os_name == "Linux":
        os_version = get_clean_linux_version()
        kernel_version = platform.release()
        machine_arch = platform.machine()
        try:
            processor = subprocess.check_output("lscpu | grep 'Model name:'", shell=True).decode('utf-8').strip().split(":")[1].strip()
        except (subprocess.CalledProcessError, IndexError):
            processor = "Unknown"

    elif os_name == "Windows":
        os_version = '.'.join(platform.win32_ver()[1].split('.')[:2])
        kernel_version = platform.release()
        machine_arch = platform.machine()
        processor = platform.processor()

    elif os_name == "Darwin":
        os_version = platform.mac_ver()[0]
        kernel_version = platform.release()
        machine_arch = platform.machine()
        processor = platform.processor()

    else:
        os_version = "Unknown"
        kernel_version = "Unknown"
        machine_arch = "Unknown"
        processor = "Unknown"

    return {
        "hostname": hostname,
        "os_name": os_name,
        "os_version": os_version,
        "kernel_version": kernel_version,
        "machine_arch": machine_arch,
        "processor": processor
    }

###-----------------###

### LOADS MODULE TO NAME DICTIONARY ###

def load_module_to_name():
    with open('tests/ubuntu_moduleToName.json', 'r') as file:
        return json.load(file)

### ADDS SCRIPTS TO THE AUDIT SELECT PAGE DISPLAY SECTION ###
def display_script_info(script_name):
    print(f"Script Info Clicked: {script_name}")
'''
def audit_select_page_populate_script_list():
    audit_select_page.script_select_display.clear()
    os_name = check_os()
    script_dir = None
    if os_name == "Ubuntu":
        script_dir = 'scripts/audits/ubuntu'
    if os_name == "rhel_9":
        script_dir = 'scripts/audits/rhel_9'
    if os_name == "Windows":
        script_dir = 'scripts/audits/windows'
    if os.path.isdir(script_dir):
        for script in sorted(os.listdir(script_dir)):
            script_name = os.path.splitext(script)[0]
            module_name = audit_select_page.module_to_name.get(script_name, script_name)

            # Create a layout for each list item
            widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(widget)
            layout.setContentsMargins(0, 0, 0, 0)

            # Add a checkbox
            checkbox = QtWidgets.QCheckBox(module_name)
            checkbox.setObjectName(script_name)  # Optional: set an object name
            layout.addWidget(checkbox)

            # Add an info button
            info_button = QtWidgets.QPushButton("Info")
            info_button.clicked.connect(lambda _, name=script_name: display_script_info(name))
            layout.addWidget(info_button)

            # Wrap the widget into a QListWidgetItem
            list_item = QtWidgets.QListWidgetItem(audit_select_page.script_select_display)
            list_item.setSizeHint(widget.sizeHint())
            audit_select_page.script_select_display.addItem(list_item)
            audit_select_page.script_select_display.setItemWidget(list_item, widget)
'''
def audit_select_page_populate_script_list(sl1, sl2, l1 , l2, bl, searcphrase = None):

    if(isworkstation and islevel1):
        l1 = True
    if(isworkstation and islevel2):
        l2 = True
    if(isserver and islevel1):
        sl1 = True
    if(isserver and islevel2):
        sl2 = True
    

    print("HEre", sl1 , sl2 , l1, l2, bl)
    audit_select_page.script_select_display.clear()
    os_name = check_os()
    script_dir = None
    if os_name == "Ubuntu":
        script_dir = 'scripts/audits/ubuntu'
        filtered_list = database.search(ops = os_name, sl1_value =  sl1, sl2_value = sl2, l1_value = l1, l2_value = l2, bl_value = bl, search_phrase=searcphrase)
        filtered_list = [i + ".sh" for i in filtered_list]
    if os_name == "rhel_9":
        script_dir = 'scripts/audits/rhel_9'
        filtered_list = database.search(ops = os_name, sl1_value =  sl1, sl2_value = sl2, l1_value = l1, l2_value = l2, bl_value = bl, search_phrase=searcphrase)
        filtered_list = [i + ".sh" for i in filtered_list]
    if os_name == "Windows":
        script_dir = 'scripts/audits/windows'
        filtered_list = database.search(ops = os_name, sl1_value =  sl1, sl2_value = sl2, l1_value = l1, l2_value = l2, bl_value = bl, search_phrase=searcphrase)
        filtered_list = [i + ".ps1" for i in filtered_list]
        # print("helo")
        print(filtered_list)
    if os.path.isdir(script_dir):
        

        # for script in sorted(os.listdir(script_dir)):

        for script in filtered_list:
            script_name = os.path.splitext(script)[0]

            module_name = audit_select_page.module_to_name.get(script_name, script_name)

            # Create a layout for each list item
            widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(widget)
            layout.setContentsMargins(0, 0, 0, 0)

            # Add a checkbox
            checkbox = QtWidgets.QCheckBox(module_name)
            checkbox.setObjectName(script_name)  # Optional: set an object name
            layout.addWidget(checkbox)

            # Add an info button and make it smaller
            info_button = QtWidgets.QPushButton("Info")
            info_button.setFixedSize(50, 20)  # Set the size to be smaller (width, height)
            info_button.clicked.connect(lambda _, name=script_name: display_script_info(name))
            layout.addWidget(info_button)

            # Wrap the widget into a QListWidgetItem
            list_item = QtWidgets.QListWidgetItem(audit_select_page.script_select_display)
            list_item.setSizeHint(widget.sizeHint())
            audit_select_page.script_select_display.addItem(list_item)
            audit_select_page.script_select_display.setItemWidget(list_item, widget)



# def audit_select_page_populate_script_list():
#     audit_select_page.script_select_display.clear()
#     os_name = check_os()
#     script_dir = None
#     if os_name == "Ubuntu":
#         script_dir = 'scripts/audits/ubuntu'
#     if os_name == "rhel_9":
#         script_dir = 'scripts/audits/rhel_9'
#     if os_name == "Windows":
#         script_dir = 'scripts/audits/windows' 
#     if os.path.isdir(script_dir):
#         for script in sorted(os.listdir(script_dir)):
#             script_name = os.path.splitext(script)[0]
#             module_name = audit_select_page.module_to_name.get(script_name, script_name)

#             # Create a layout for each list item
#             widget = QtWidgets.QWidget()
#             layout = QtWidgets.QHBoxLayout(widget)
#             layout.setContentsMargins(0, 0, 0, 0)

#             # Add a label for the script name
#             label = QtWidgets.QLabel(module_name)
#             layout.addWidget(label)

#             # Add an info button
#             info_button = QtWidgets.QPushButton("Info")
#             info_button.clicked.connect(lambda _, name=script_name: display_script_info(name))
#             layout.addWidget(info_button)

#             # Wrap the widget into a QListWidgetItem
#             list_item = QtWidgets.QListWidgetItem(audit_select_page.script_select_display)
#             list_item.setSizeHint(widget.sizeHint())
#             audit_select_page.script_select_display.addItem(list_item)
#             audit_select_page.script_select_display.setItemWidget(list_item, widget)


# def audit_select_page_populate_script_list():
#     audit_select_page.script_select_display.clear()
#     os_name = check_os()
#     script_dir = None
#     if os_name == "Ubuntu":
#         script_dir = 'scripts/audits/ubuntu'
#     if os_name == "rhel_9":
#         script_dir = 'scripts/audits/rhel_9'
#     if os_name == "Windows":
#         script_dir = 'scripts/audits/windows' 
#     if os.path.isdir(script_dir):
#         for script in sorted(os.listdir(script_dir)):
#             script_name = os.path.splitext(script)[0]
#             module_name = audit_select_page.module_to_name.get(script_name, script_name)
#             list_item = QtWidgets.QListWidgetItem(module_name)
#             list_item.setFlags(list_item.flags() | QtCore.Qt.ItemIsUserCheckable)
#             list_item.setCheckState(QtCore.Qt.Unchecked)
#             list_item.setData(QtCore.Qt.UserRole, script)
#             audit_select_page.script_select_display.addItem(list_item)

### SELECTS ALL SCRIPTS ON AUDIT SELECT PAGE (SELECT ALL BUTTON SLOT) ###

# def audit_select_page_select_all_scripts():
#     if audit_select_page.select_all_btn.isChecked():
#         loader_select_all_warning = QUiLoader()
#         select_all_warning = loader_select_all_warning.load('select_all_warning.ui', audit_select_page)
#         select_all_warning.show()
#         for index in range(audit_select_page.script_select_display.count()):
#             item = audit_select_page.script_select_display.item(index)
#             item.setCheckState(QtCore.Qt.Checked)
#     else:
#         for index in range(audit_select_page.script_select_display.count()):
#             item = audit_select_page.script_select_display.item(index)
#             item.setCheckState(QtCore.Qt.Unchecked)

def audit_select_page_select_all_scripts():
    is_checked = audit_select_page.select_all_btn.isChecked()

    for index in range(audit_select_page.script_select_display.count()):
        item = audit_select_page.script_select_display.item(index)
        widget = audit_select_page.script_select_display.itemWidget(item)
        if widget:
            checkbox = widget.findChild(QtWidgets.QCheckBox)
            if checkbox:
                checkbox.setChecked(is_checked)

    


def audit_select_page_add_new_script():
    file_path, _ = QFileDialog.getOpenFileName(None, "Select Script", "/home", "Bash Files (*.sh)")
    if file_path:
        script_name = os.path.basename(file_path)
        audit_select_page.script_select_display.addItem(script_name)

### CREATES THE DATABASE FOR AUDIT RESULTS ### 

def create_tables():
    cursor = audit_select_page.database.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            script_name TEXT,
            output TEXT,
            error TEXT,
            return_code INTEGER,
            execution_time TEXT,
            session_id INTEGER
        )
    ''')
    audit_select_page.database.commit()


### 

def run_script(script_path):
    try:
        os_name = check_os()
        if os_name == "Ubuntu":
            os.chmod(script_path, 0o755)
            result = subprocess.run(["bash", script_path], capture_output=True, text=True)
        if os_name == "rhel_9":
            os.chmod(script_path, 0o755)
            result = subprocess.run(["bash", script_path], capture_output=True, text=True)
        if os_name == "Windows":
            result = subprocess.run(
                ["powershell.exe", 
                "-ExecutionPolicy", "Bypass", 
                "-File", script_path],
                capture_output=True, text=True
            )
        return result.stdout, result.stderr, result.returncode
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, e.returncode

def add_audit_result(result):
    cursor = audit_select_page.database.cursor()
    cursor.execute('''
        INSERT INTO audit_results (script_name, output, error, return_code, execution_time, session_id)
        VALUES (?, ?, ?, ?, datetime('now'), ?)
    ''', (result['script_name'], result['output'], result['error'], result['return_code'], result['session_id']))
    audit_select_page.database.commit()

###
def audit_selected_scripts():
    global logfile_name
    logfile_name = f'/tmp/audit_log_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.txt'
    logfile = open(f'{logfile_name}', 'w')
    selected_scripts = []  # List to hold the selected script names

    for index in range(audit_select_page.script_select_display.count()):
        item = audit_select_page.script_select_display.item(index)
        widget = audit_select_page.script_select_display.itemWidget(item)

        if widget:
            checkbox = widget.findChild(QtWidgets.QCheckBox)
            if checkbox and checkbox.isChecked():
                script_name = checkbox.objectName()  # Use the object name set for the checkbox
                selected_scripts.append(script_name)

    global session_id
    session_id += 1
    item_count = len(selected_scripts)

    main_window.setCurrentIndex(3)

    for idx, script_name in enumerate(selected_scripts, start=1):
        QCoreApplication.processEvents()
        audit_progress_page.current_script_lbl.setText(str(script_name))

        script_path = None
        os_name = check_os()
        if os_name == "Ubuntu":
            script_name += ".sh" 
            script_path = os.path.join('scripts/audits/ubuntu', script_name)
        if os_name == "rhel_9":
            script_name += ".sh" 
            script_path = os.path.join('scripts/audits/rhel_9', script_name)
        if os_name == "Windows":
            script_name += ".ps1"
            script_path = os.path.join('scripts\\audits\\windows', script_name)

        if not os.path.exists(script_path):
            print(f"Script not found: {script_path}")
            continue
        stdout, stderr, return_code = run_script(script_path)
        result = {
            'script_name': script_name,
            'output': stdout,
            'error': stderr,
            'return_code': return_code,
            'session_id': session_id
        }

        logfile.write(f"Script: {script_name}\n")
        logfile.write(f"Output:{stdout}\n")
        logfile.write(f"Error:{stderr}\n")
        logfile.write(f"Return Code: {return_code}\n\n")
        
        add_audit_result(result)
        QCoreApplication.processEvents()
        progress = int(idx / item_count * 100)
        audit_progress_page.script_progess_bar.setValue(progress)
    print("Audit completed")

    logfile.close()

    main_window.setCurrentIndex(4)
    audit_result_page_display_result()

# def audit_selected_scripts():
#     selected_items = [audit_select_page.script_select_display.item(i) for i in range(audit_select_page.script_select_display.count()) if audit_select_page.script_select_display.item(i).checkState() == QtCore.Qt.Checked]
#     global session_id
#     session_id += 1
#     item_count = len(selected_items)

#     main_window.setCurrentIndex(3)

#     for idx, item in enumerate(selected_items, start=1):
#         QCoreApplication.processEvents()
#         script_name = item.data(QtCore.Qt.UserRole)
#         audit_progress_page.current_script_lbl.setText(str(script_name))

#         script_path = None
#         os_name = check_os()
#         if os_name == "Ubuntu":
#             script_path = os.path.join('scripts/audits/ubuntu', script_name)
#         if os_name == "rhel_9":
#             script_path = os.path.join('scripts/audits/rhel_9', script_name) 
#         if os_name == "Windows":
#             script_path = os.path.join('scripts/audits/windows', script_name)

#         if not os.path.exists(script_path):
#             print(f"Script not found: {script_path}")
#             continue
#         stdout, stderr, return_code = run_script(script_path)
#         result = { 'script_name': script_name, 'output': stdout, 'error': stderr, 'return_code': return_code, 'session_id': session_id}
#         add_audit_result(result)
#         QCoreApplication.processEvents()
#         progress = int(idx / item_count * 100)
#         audit_progress_page.script_progess_bar.setValue(progress)
#     print("Audit completed")

#     main_window.setCurrentIndex(4)
#     audit_result_page_display_result()
    
###

def audit_result_page_display_result():
    newdatabase = sqlite3.connect("audit_results.db")
    cursor = newdatabase.cursor()
    cursor.execute("""
            SELECT script_name, return_code, output, error
            FROM audit_results
            WHERE session_id = ?
        """, (session_id,))
    
    rows = cursor.fetchall()
    audit_result_page.module_to_name = load_module_to_name()
    audit_result_page.script_result_display.clear()  # Clear previous results
    for row_idx, (script_name, return_code, output, error) in enumerate(rows):
        module_name = audit_result_page.module_to_name.get(script_name, script_name)

        audit_result_page.script_result_display.setWordWrap(True)
        
        # Create parent item for the script
        parent_item = QtWidgets.QTreeWidgetItem(audit_result_page.script_result_display)
        if return_code == 0:  # Pass
            parent_item.setText(0, f"PASS: {module_name}")
            parent_item.setStyleSheet(f'color: QtCore.Qt.green;')
        else:
            parent_item.setText(0, f"FAIL: {module_name}")
            parent_item.setStyleSheet(f'color: QtCore.Qt.red;')
        
        # Add placeholder details as child items
        
        # Truncate if output is too long

        if output != "":
            child_output = QtWidgets.QTreeWidgetItem(parent_item)
            child_output.setText(0, f"{output}")
            # child_output.setwordWrap(True)
        # Truncate if error is too long
        
        if error != "" :
            child_error = QtWidgets.QTreeWidgetItem(parent_item)
            child_error.setText(0, f"{error}")
            # child_error.setwordWrap(True)
        # Truncate if error is too long
        
        # Expand all items by default (optional)
        parent_item.setExpanded(False)


def new_audit_filters():
    global isworkstation
    global islevel2
    global isserver
    global islevel1
    global isbitlocker

    isworkstation = new_audit_page.workstation_btn.isChecked()
    isserver = new_audit_page.server_btn.isChecked()
    islevel1 = new_audit_page.level1_btn.isChecked()
    islevel2 = new_audit_page.level2_btn.isChecked()
    isbitlocker = new_audit_page.bitlocker_btn.isChecked()
    print(isworkstation, isserver, islevel1, islevel2, isbitlocker)
    main_window.setCurrentIndex(2)

if __name__ == "__main__":
    session_id = 0
    app = QApplication(sys.argv)
    main_window = QStackedWidget()

    # Load the start page UI file
    loader_start_page = QUiLoader()
    start_page = loader_start_page.load("start_page.ui", main_window)
    main_window.addWidget(start_page)

    # Get system information
    system_info = get_system_info()

    # Set label text for each system information entry
    start_page.hostname_lbl_entry.setText(system_info["hostname"])
    start_page.os_name_entry.setText(system_info["os_name"])
    start_page.os_version_lbl_entry.setText(system_info["os_version"])
    start_page.kernel_lbl_entry.setText(system_info["kernel_version"])
    start_page.mach_arch_lbl_entry.setText(system_info["machine_arch"])
    start_page.processor_lbl_entry.setText(system_info["processor"])

    # Connect buttons to methods
    loader_new_audit_page = QUiLoader()
    new_audit_page = loader_new_audit_page.load("new_audit_page.ui", main_window)
    main_window.addWidget(new_audit_page)

    bitlocker_status()

    start_page.new_audit_btn.clicked.connect(lambda: main_window.setCurrentIndex(1))

    loader_audit_select_page = QUiLoader()
    audit_select_page = loader_audit_select_page.load("audit_select_page.ui", main_window)
    main_window.addWidget(audit_select_page)

    loader_audit_progess_page = QUiLoader()
    audit_progress_page = loader_audit_progess_page.load("audit_progress_page.ui", None)
    main_window.addWidget(audit_progress_page)

    isworkstation = None
    isserver = None
    islevel1 = None
    islevel2 = None
    isbitlocker = None

    new_audit_page.continue_btn.clicked.connect(new_audit_filters)
    print(isworkstation , islevel2)

    audit_select_page.module_to_name = load_module_to_name()
    audit_select_page.database = sqlite3.connect('audit_results.db')
    create_tables()
    sl1 = False
    sl2 = False
    l1 = False
    l2 = False
    bl = isbitlocker

    if(isworkstation and islevel1):
        l1 = True
    if(isworkstation and islevel2):
        l2 = True
    if(isserver and islevel1):
        sl1 = True
    if(isserver and islevel2):
        sl2 = True
    audit_select_page_populate_script_list(sl1 =  sl1, sl2= sl2, l1 = l1, l2 = l2, bl = bl)
    new_audit_page.continue_btn.clicked.connect(lambda: [
    new_audit_filters(),  # This sets the global filter variables
    audit_select_page_populate_script_list(
        sl1=sl1 , 
        sl2=sl2 , 
        l1=l1 , 
        l2=l2 , 
        bl=isbitlocker
    )
    ])
    audit_select_page.select_all_btn.clicked.connect(audit_select_page_select_all_scripts)
    if os.path.exists("audit_results.db"):
        cursor = audit_select_page.database.cursor()
        cursor.execute('''select max(session_id) from audit_results''')
        result = cursor.fetchone()
        cursor.close()
        session_id = result[0] if result[0] else 0
    audit_select_page.back_btn.clicked.connect(lambda: main_window.setCurrentIndex(0))
    # audit_select_page.add_script_btn.clicked.connect(audit_select_page_add_new_script)

    loader_audit_result_page = QUiLoader()
    audit_result_page = loader_audit_result_page.load("audit_result_page.ui", main_window)
    main_window.addWidget(audit_result_page)

    audit_select_page.audit_btn.clicked.connect(audit_selected_scripts)
    audit_result_page.home_btn.clicked.connect(lambda: main_window.setCurrentIndex(0))

    start_page.cis_benchmark_btn.clicked.connect(open_cis_website)
    new_audit_page.cis_benchmark_btn.clicked.connect(open_cis_website)

    logfile_name = None

    def view_logs():
        loader_log_page = QUiLoader()
        log_page = loader_log_page.load("log_page.ui", None)
        log_data = open(f'{logfile_name}', 'r').read()
        log_page.textEdit.setText(log_data)

        log_page.show()

    def save_logs():
        log_data = open(f'{logfile_name}', 'r').read()
        filename = QFileDialog.getSaveFileName(audit_result_page, "Save Log", "", "Text Files (*.txt)")
        if filename[0]:
            with open(filename[0], 'w') as f:
                f.write(log_data)

    audit_result_page.view_logs_btn.clicked.connect(view_logs)
    audit_result_page.export_btn.clicked.connect(save_logs)


    main_window.show()
    sys.exit(app.exec())
