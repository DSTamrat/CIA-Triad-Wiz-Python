import shutil
import time

def backup_file(src, dst):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    shutil.copy(src, f"{dst}/backup_{timestamp}.bak")

backup_file("database.db", "./backups")
