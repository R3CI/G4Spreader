from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Log, ProgressBar
from datetime import datetime as dt

class Logger:
    def __init__(self):
        self.logwidget = None
    
    def timestamp(self):
        return dt.now().strftime('%H:%M:%S')
    
    def write(self, text, level_color='white', level_name=''):
        logstr = f'[{self.timestamp()}] '
        if level_name:
            logstr += f'{level_name} '
        logstr += f'» {text}'
        if self.logwidget:
            self.logwidget.write_line(logstr)
        else:
            print(logstr)
    
    def info(self, text):
        self.write(text, level_color='blue', level_name='INFO')
    
    def success(self, text):
        self.write(text, level_color='green', level_name='SUCCESS')
    
    def error(self, text):
        self.write(text, level_color='red', level_name='ERROR')
    
    def warning(self, text):
        self.write(text, level_color='yellow', level_name='WARNING')
    
    def locked(self, text):
        self.write(text, level_color='magenta', level_name='LOCKED')
    
    def ratelimit(self, text):
        self.write(text, level_color='cyan', level_name='RATELIMIT')
    
    def cloudflare(self, text):
        self.write(text, level_color='blue', level_name='CLOUDFLARE')
    
    def solver(self, text):
        self.write(text, level_color='magenta', level_name='SOLVER')
    
    def captcha(self, text):
        self.write(text, level_color='red', level_name='CAPTCHA')
    
    def debug(self, text):
        pass

logger = Logger()

class dashboard(App):
    CSS = '''
    Screen {
        layout: vertical;
        background: #0a0a0f;
    }
    #top { height: 50%; }
    #bottom { height: 50%; border-top: solid rgb(80,5,255); }
    #stats, #threads, #config {
        border: solid rgb(80,5,255);
        padding: 1;
        background: #0a0a0f;
        color: white;
    }
    #stats { width: 25%; }
    #threads { width: 50%; }
    #config { width: 25%; }
    Log {
        border: solid rgb(80,5,255);
        background: #05050a;
        color: white;
    }
    ProgressBar { height: 1; }
    '''
   
    def compose(self) -> ComposeResult:
        with Container(id='top'):
            with Horizontal():
                with Vertical(id='stats'):
                    self.statsdisplay = Static('')
                    yield self.statsdisplay
                    self.progress = ProgressBar(total=100, show_eta=False)
                    yield self.progress
                with Vertical(id='threads'):
                    self.threadsdisplay = Static('')
                    yield self.threadsdisplay
                with Vertical(id='config'):
                    self.configdisplay = Static('')
                    yield self.configdisplay
        with Container(id='bottom'):
            self.logwidget = Log()
            yield self.logwidget
   
    def on_mount(self):
        self.sentdms = 0
        self.sentchannels = 0
        self.total = 0
        self.percent = 0
        self.configdata = {}
        self.threads = []
   
    def setstats(self, sentdms=None, sentchannels=None, percent=None):
        if sentdms is not None:
            self.sentdms = sentdms
        if sentchannels is not None:
            self.sentchannels = sentchannels
        self.total = self.sentdms + self.sentchannels
        if percent is not None:
            self.percent = max(0, min(100, percent))
        self.refreshstats()
        self.updateprogressbar()
   
    def setconfig(self, key, value):
        self.configdata[key] = value
        self.refreshconfig()
   
    def setthreads(self, threads):
        self.threads = threads
        self.refreshthreads()
   
    def addlog(self, message):
        if hasattr(self, 'logwidget') and self.logwidget:
            self.logwidget.write_line(str(message))
   
    def refreshstats(self):
        text = f'Sent to open DMS: {self.sentdms}\nSent to server channels: {self.sentchannels}\nTotal sent: {self.total}'
        self.statsdisplay.update(text)
   
    def refreshconfig(self):
        lines = []
        for k, v in self.configdata.items():
            if isinstance(v, bool):
                color = 'green' if v else 'red'
                val = '✓' if v else '✗'
                lines.append(f'{k}: [bold {color}]{val}[/bold {color}]')
            else:
                val = str(v)
                lines.append(f'{k}: {val}')
        self.configdisplay.update('\n'.join(lines))
   
    def refreshthreads(self):
        lines = []
        for th in self.threads:
            msg = th.get('status','')[:20].replace('\n', ' ')
            progress = th.get('progress', 0)
            lines.append(f'[dim]tid=[/dim]{th.get("id","")} [dim]token=[/dim]{th.get("token","")[:6]} [dim]sent=[/dim]{th.get("success",0)} [dim]progress=[/dim]{progress}% [dim]msg=[/dim]{msg}')
        self.threadsdisplay.update('\n'.join(lines))
   
    def updateprogressbar(self):
        if self.percent <= 50:
            r = 255
            g = int(255 * self.percent / 50)
        else:
            g = 255
            r = int(255 * (100 - self.percent) / 50)
        color = f'rgb({r},{g},0)'
        self.progress.styles.bar_color = color
        self.progress.update(progress=self.percent)