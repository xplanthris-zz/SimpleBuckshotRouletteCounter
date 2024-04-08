import os, platform, ctypes


def check_admin_privileges():
    """A function that checks if the program is being run as an administrator

    Returns:
        Boolean: Returns True if the program is being run as an administrator
    """

    # If the OS is Windows
    if platform.system() == "Windows":
        # Wrap it in a try-except loop as the command might fail due to lack of privileges
        try:
            # This should return 1 if your an admin
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            # Looks like we are not an admin
            return False
    else:
        # So we are running Unix, this is easy, just get the current EUID and check if it is 0
        return os.geteuid() == 0
