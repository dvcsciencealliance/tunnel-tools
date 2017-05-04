import logging
import json
import bot_handler
import subprocess
Popen = subprocess.Popen

logger = logging.getLogger(__name__)

class Tunnel(bot_handler.TelegramHandler):
    def __init__(self, bot=None, config=None):
        bot_handler.TelegramHandler.__init__(self, bot, config)
        self.process = None
        
        try:
            self.auth = self.config['admins']
        except KeyError:
            self.auth = ()
        
        with open("tunnel_config.json", 'r') as f:
            self._cfg = json.loads(f.read())
            
        try:
            self._cfg['local_addr']
        except KeyError:
            self._cfg['local_addr'] = "localhost"
        try:
            self._cfg['user']
            self._cfg['addr']
            self._cfg['port']
            self._cfg['remote_port']
            self._cfg['local_port']
            #ssh -R *:<remote_port>:<local_addr>:<local_port> -p <port> <user>@<addr>
        except KeyError:
            self._cfg_valid = False
            logger.error("tunnel_config.json not valid")
        else:
            self._cfg_valid = True
            
    def update(self, update):
        try:
            message = update['message']
            chat_id = message['chat']['id']
            from_id = message['from']['id']
            text = message['text']
        except KeyError:
            pass
        else:
            if from_id in self.auth and self._cfg_valid:
                if text.startswith("/tunnel "):
                    cmd = text.split(" ")[1:]
                elif from_id == chat_id:
                    cmd = text.split(" ")
                else:
                    return
                
                if cmd[0] == "start" and self.process == None:
                    cfg = self._cfg
                    if len(cmd) > 1:
                        if cmd[1].find(":") != -1:
                            tun_arg = "*:{0}:{1}".format(cfg['remote_port'], cmd[1])
                        else:
                            tun_arg = "*:{0}:{1}:{2}".format(cfg['remote_port'], cfg['local_addr'], cmd[1])
                    else:
                        tun_arg = "*:{0}:{1}:{2}".format(cfg['remote_port'], cfg['local_addr'], cfg['local_port'])
                    dest_arg = "{0}@{1}".format(cfg['user'], cfg['addr'])
                    args = ["ssh", "-NT", "-R", tun_arg, "-p", cfg['port'], dest_arg]
                    try:
                        args += ["-i", cfg['key']]
                    except KeyError:
                        pass
                    logger.debug(" ".join(args))
                    
                    self.process = Popen(args)
                    self.bot.sendMessage(chat_id, "Tunnel started.")
                elif cmd[0] == "start":
                    self.bot.sendMessage(chat_id, "Process already running.")
                elif cmd[0] == "stop" and self.process == None:
                    self.bot.sendMessage(chat_id, "Process not running.")
                elif cmd[0] == "stop":
                    try:
                        self.process.kill()
                    except ProcessLookupError:
                        self.bot.sendMessage(chat_id, "Process not running.")
                    self.process = None
                    self.bot.sendMessage(chat_id, "Tunnel stopped.")
                elif cmd[0] == "ssh" and self.process == None:
                    cmd.append("-NT")
                    cmd.append(self._cfg['user'])
                    cmd.append("-i")
                    cmd.append(self._cfg['key'])
                    self.process = Popen(cmd)
                elif cmd[0] == "ssh":
                    self.bot.sendMessage(chat_id, "Process already running.")
                elif cmd[0] == "kill":
                    args = ["killall", "ssh"]
                    Popen(args)
                    self.process = None
                elif cmd[0] == "status":
                    reply = "Stopped" if self.process is None else "Running"
                    self.bot.sendMessage(chat_id, "{}".format(reply))
