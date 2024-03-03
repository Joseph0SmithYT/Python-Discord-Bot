from terminal import CustomTerminal
import main
import subprocess
terminal = CustomTerminal()

@terminal.register_command(
    command_name="start",
    description="Starts the discord bot"
)
def start_bot():
    subprocess.Popen(['python', 'main.py'], stdout=subprocess.PIPE, shell=True)
@terminal.register_command(
    command_name="quit",
    description="Quits the discord bot"
)    
def quit():
    # Find the process ID
    process = subprocess.Popen(["pgrep", "-f", "python main.py"], stdout=subprocess.PIPE)
    pid = int(process.communicate()[0])
    subprocess.run(["kill", str(pid)])

terminal.start()