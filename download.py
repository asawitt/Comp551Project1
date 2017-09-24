import urllib.request
sample = "http://www.fanfr.com/scripts/saison4vf/friendsgeneration2.php?nav=script&version=vf&episodescript=412"

seasons = [
    24,
    24,
    25,
    24,
    24,
    25,
    24,
    24,
    24,
    18
] # num of episodes in each season

def get_episodes():
    for i in range(len(seasons)):
        for j in range(1, seasons[i]+1):
            episode_str = "{:02d}".format(j)
            tag = int(str(i + 1) + episode_str)
            sample_format = "http://www.fanfr.com/scripts/saison{:d}vf/friendsgeneration2.php?nav=script&version=vf&episodescript={:d}"
            url = sample_format.format(i + 1, tag)
            print(url)
            response = urllib.request.urlopen(url)
            data = response.read()      # a `bytes` object
            text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
            filename_format = "raw_scripts/friends_{:d}_{:d}.htm"
            with open(filename_format.format(i + 1, j), "w") as episode_file:
                episode_file.write(text)

if __name__ == "__main__":
    get_episodes()

