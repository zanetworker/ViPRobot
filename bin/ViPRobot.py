import argparse
import getpass

from utils.CommunicationUtils import CommunicationUtils
from utils.ViPRobotExceptions import ViPRobotException
from utils.CommandUtils import CommandUtils
from utils.CommonUtils import *

class PasswordPromptAction(argparse.Action):
    def __init__(self,
             option_strings,
             dest=None,
             nargs=0,
             default=None,
             required=False,
             type=None,
             metavar=None,
             help=None):

        super(PasswordPromptAction, self).__init__(
             option_strings=option_strings,
             dest=dest,
             nargs=nargs,
             default=default,
             required=required,
             metavar=metavar,
             type=type,
             help=help)

    def __call__(self, parser, args, values, option_string=None):
        password = getpass.getpass()
        setattr(args, self.dest, password)


if __name__ == "__main__":
        text ='Welcome to ViPRobot, the app store for ViPR implementations'
        parser = argparse.ArgumentParser(description=text)

        parser.add_argument('-u', '--user',
                            help='The username that will be used to log into ViPR',
                            dest='user',
                            type=str,
                            required=True)

        parser.add_argument('-p', '--password',
                            help='The password that will be used to log into ViPR',
                            dest='password',
                            action=PasswordPromptAction,
                            type=str,
                            required=True)

        try:
            args = parser.parse_args()
            communicationUtils = CommunicationUtils(username=args.user,
                                                    password=args.password,
                                                    token=None,
                                                    request_timeout=15.0)

            commandUtils = CommandUtils(communicationUtils)

            log_this(__name__, commandUtils.get_tenant(),"")
            log_this(__name__, commandUtils.create_storage_provider(), "")
            log_this(__name__, commandUtils.create_smis_provider(), "")
            log_this(__name__, commandUtils.create_hosts(),"")

        except ViPRobotException as viprobot:
            print('Message: {0}'.format(viprobot.message))
            print('Status Code Returned: {0}\n'.format(viprobot.http_status_code))
            print('ViPR API Message: {0}'.format(viprobot.vipr_message))
        # except Exception as ex:
        #     print(ex.message)

        #list_storage_systems()
        #create_smis_provider()


