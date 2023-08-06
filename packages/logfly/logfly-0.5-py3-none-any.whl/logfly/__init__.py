import time
import os


def create_log_folder():
    dirs = '.\\logs\\'
    dirs2 = '.\\logs\\' + get_time('date')
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    else:
        pass
    if not os.path.exists(dirs2):
        os.makedirs(dirs2)
    else:
        pass


def get_time(flag):
    if flag == 'datetime':
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if flag == 'date':
        return time.strftime("%Y-%m-%d", time.localtime())
    if flag == 'times':
        return time.strftime("%H:%M:%S", time.localtime())
    if flag == 'datetimefile':
        return time.strftime("%Y%m%d%H%M%S", time.localtime())


def write_log(name, position, level, message, mode='add'):
    global logfile
    logfolder = '.\\logs\\' + get_time('date') + '\\'
    if mode == 'add':
        logfile = logfolder + name + '-' + get_time('date') + '.log'
    elif mode == 'new':
        logfile = logfolder + name + '-' + get_time('datetimefile') + '.log'
    create_log_folder()
    if position == 'CLI':
        print(name + ' ' + get_time('datetime') + ' ' + '[' + str.upper(level) + ']' + ' ' + message + '\r\n')
    if position == 'file':
        if mode == 'add':
            File = open(logfile, 'a', newline='')
            File.write(get_time('datetime') + ' ' + '[' + str.upper(level) + ']' + ' ' + message + '\r\n')
            File.close()
        elif mode == 'new':
            File = open(logfile, 'w', newline='')
            File.write(get_time('datetime') + ' ' + '[' + str.upper(level) + ']' + ' ' + message + '\r\n')
            File.close()
    if position == 'fileCLI':
        print(name + ' ' + get_time('datetime') + ' ' + '[' + str.upper(level) + ']' + ' ' + message + '\r\n')
        if mode == 'add':
            File = open(logfile, 'a', newline='')
            File.write(get_time('datetime') + ' ' + '[' + str.upper(level) + ']' + ' ' + message + '\r\n')
            File.close()
        elif mode == 'new':
            File = open(logfile, 'w', newline='')
            File.write(get_time('datetime') + ' ' + '[' + str.upper(level) + ']' + ' ' + message + '\r\n')
            File.close()


if __name__ == '__main__':
    write_log('Doctor Who', 'CLI', 'info', "this is Doctor's log, only in CLI.")
    write_log('Doctor Who', 'fileCLI', 'info', "this is Doctor's log, in file and CLI.", mode='add')
    write_log('Doctor Who', 'file', 'info', "this is Doctor's log, only in file.")
    write_log('Tardis', 'CLI', 'info', "this is Tardis's log, only in CLI.")
    write_log('Tardis', 'fileCLI', 'info', "this is Tardis's log, in file and CLI.")
    write_log('Tardis', 'file', 'info', "this is Tardis's log, only in file.")
