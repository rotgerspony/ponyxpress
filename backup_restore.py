
import shutil

def backup_db(src="ponyxpress.db", dest="ponyxpress_backup.db"):
    shutil.copy(src, dest)

def restore_db(backup="ponyxpress_backup.db", dest="ponyxpress.db"):
    shutil.copy(backup, dest)
