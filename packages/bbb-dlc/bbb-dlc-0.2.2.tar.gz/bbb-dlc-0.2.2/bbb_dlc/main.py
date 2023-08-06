import argparse
import os
from posixpath import dirname

from bbb_dlc.version import __version__
from bbb_dlc.bigbluebutton_api_python import BigBlueButton
from re import match
import subprocess
from datetime import datetime
import traceback

class BBBDLC:
    def run(args):
        bbb = BigBlueButton(args.server, args.secret)
        recordingParams = {
            "recordID": args.recordId,
        }

        try:
            serverDir = args.serverDir

            os.chdir(serverDir)

            occCommand = "/opt/plesk/php/7.3/bin/php " + serverDir + "/occ "
            os.system(occCommand + "config:system:get datadirectory > ncPath.txt")

            ncPathFile = open(serverDir + "/ncPath.txt", "r")
            ncPath = ncPathFile.readline().strip()
            ncPathFile.close()
            os.system("rm " + serverDir + "/ncPath.txt")

            if ncPath == "": raise NameError('Could not find nextcloud config!')
            
            recordingUrl = bbb.get_recordings(recordingParams)
            recordingUrl = recordingUrl["xml"]["recordings"]["recording"]["playback"]["format"]["url"]
            passthroughArgs = ""

            for arg in vars(args):
                if arg == "recordId" or arg == "server" or arg == "secret" or arg == "serverName" or arg == "serverDir": continue
                if getattr(args, arg) == None or getattr(args, arg) == False: continue

                arg = arg.replace("_", "-")
                if arg == "encoder" or arg == "audiocodec": arg += " " +  str(getattr(args, arg))
                passthroughArgs += "--" + arg + " "

            passthroughArgs += recordingUrl
            os.chdir(ncPath + "/admin/files")
            os.system("ianes-bbb-dl " + passthroughArgs)
            os.system(occCommand + "files:scan admin")
        except Exception as e:
            now = datetime.now()
            error = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "] " + str(traceback.format_exc()) + "\n"
            print(traceback.format_exc())
            errorLog = open("/var/www/vhosts/sapienslab.com.mx/logs/bbb_error_log", "a")
            errorLog.write(error)
            errorLog.close()

def change(user_uid, user_gid):
    def result():
        report_ids('starting demotion')
        os.setgid(user_gid)
        os.setuid(user_uid)
        report_ids('finished demotion')
    return result

def report_ids(msg):
    print('uid, gid = %d, %d; %s' % (os.getuid(), os.getgid(), msg))

def get_parent(dirName, dirUp):
    for i in range(dirUp):
        dirName = os.path.dirname(dirname)

def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser(
        description=('Big Blue Button Converter and Downloader')
    )

    parser.add_argument('serverName', type=str, help='Server name')

    parser.add_argument('serverDir', type=str, help='Server install directory')

    parser.add_argument('recordId', type=str, help='Recording ID of a lesson')

    parser.add_argument('server', type=str, help='BBB API Server')

    parser.add_argument('secret', type=str, help='BBB API Secret')

    parser.add_argument(
        '-aw',
        '--add-webcam',
        action='store_true',
        help='add the webcam video as an overlay to the final video',
    )

    parser.add_argument(
        '-aa',
        '--add-annotations',
        action='store_true',
        help='add the annotations of the professor to the final video',
    )

    parser.add_argument(
        '-kt',
        '--keep-tmp-files',
        action='store_true',
        help=('keep the temporary files after finish'),
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help=('print more verbose debug informations'),
    )
    parser.add_argument(
        '-ncc',
        '--no-check-certificate',
        action='store_true',
        help=('Suppress HTTPS certificate validation'),
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='bbb-dlc ' + __version__,
        help='Print program version and exit'
    )
    
    parser.add_argument(
        '--encoder',
        dest='encoder',
        type=str,
        default='libx264',
        help='Optional encoder to pass to ffmpeg (default libx264)',
    )

    parser.add_argument(
        '--audiocodec',
        dest='audiocodec',
        type=str,
        default='copy',
        help='Optional audiocodec to pass to ffmpeg (default copy the codec from the original source)',
    )

    parser.add_argument(
        '-f',
        '--filename',
        type=str,
        help='Optional output filename',
    )

    return parser


# --- called at the program invocation: -------------------------------------
def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    BBBDLC.run(args)