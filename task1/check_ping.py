import subprocess


def get_rtt_os(url):
    result = subprocess.run(['ping', '-c', '1', url], stdout=subprocess.PIPE)
    if (result.returncode != 0): 
        return None
    return str(result.stdout).split(',')

hostnames = ["google.com", "wikipedia.org", "amazon.com", "microsoft.com", \
             "github.com", "mail.ru", "yandex.ru", "vk.com", "youtube.com", "roblox.com"]


with open("pings.csv", "w") as f:
    for hostname in hostnames:

        stats = get_rtt_os(hostname) 
        if stats:
            avg_rtt = stats[3].split('=')[1].split('/')[1]
            f.write(f"{hostname}, {avg_rtt}  ms\n")
        else:
            f.write(f"unable to ping host {hostname}\n")
