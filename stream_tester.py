import m3u8
from urllib.request import urlopen
from multiprocessing import Process

import threading
import time
import sys

class StreamTester:
    def __init__(self, playlist_url):
        self.known_segments = []
        self.playlist_uri = playlist_url
        self.segment_base_url = playlist_url[:playlist_url.rfind("/")+1]

    def run(self):
        print("RUN STREAM TEST WORKER AGAINST" + self.playlist_uri)
        playlist = m3u8.load(self.playlist_uri)  # this could also be an absolute filename

        #print("segments:")
        #print(playlist.segments.uri)

        print("target_duration:")
        print(playlist.target_duration)

        while True:
            start = time.time()
            self.tick()
            tick_duration = time.time()-start
            if tick_duration < playlist.target_duration:
                time.sleep(playlist.target_duration - tick_duration)
            
    def tick(self):
        playlist = m3u8.load(self.playlist_uri)  # this could also be an absolute filename
        #print("segments:")
        #print(playlist.segments.uri)

        for one_segment_uri in playlist.segments.uri:
            if one_segment_uri not in self.known_segments:
                self.known_segments.append(one_segment_uri)
                self.load_segment(one_segment_uri)
                        
    def load_segment(self, uri: str):
        #just load and discard
        url = self.segment_base_url + uri
        print("load: " + url)

        with urlopen("https://www.example.com") as response:
            body = response.read()

            print("segment size: " + str(len(body)))


def run_worker(playlist_url):
    streamTester = StreamTester(playlist_url)
    streamTester.run()

def main(args):
    if len(args) != 3:
        print("USAGE: python3.x stream_tester.py <WORKERS> <PLAYLIST_URL>")
        return

    processes = []
    for i in range(int(args[1])):
        print("START WORKER " + str(i))

        p = Process(target=run_worker, args=(args[2],))
        p.start()
        processes.append(p)

    while True:
        time.sleep(1)



if __name__ == '__main__':
    main(sys.argv)