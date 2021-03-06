import m3u8
from urllib.request import urlopen
from multiprocessing import Process

import threading
import time
import sys
import random
import traceback

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
            try:
                self.tick()
            except:
                print("ERROR")
                traceback.print_exc()
            tick_duration = time.time()-start
            if tick_duration < playlist.target_duration:
                time.sleep(playlist.target_duration - tick_duration)
            else:
                print("SEGEMENT DELAY TICK DURATION: " + str(tick_duration))
            
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
        #print("load: " + url)

        with urlopen(url) as response:
            body = response.read()

            print("segment loaded - size: " + str(len(body)))


def run_worker(playlist_url):
    streamTester = StreamTester(playlist_url)
    streamTester.run()


def get_workers() -> int:
    try:
        with open("/home/ubuntu/workers.txt") as f:
            return int(str(f.read()))
    except:
        return 0

def get_playlist_url() -> int:
    try:
        with open("/home/ubuntu/playlist_url.txt") as f:
            return str(f.read())
    except:
        return 0

def main(args):
    workers = get_workers()
    playlist_url = get_playlist_url()
    
    if (workers == 0 or not playlist_url) and len(args) != 3:
        print("USAGE: python3.x stream_tester.py <WORKERS> <PLAYLIST_URL>")
        return

    if len(args) == 3:
        workers = args[1]
        playlist_url = args[2]


    processes = []
    for i in range(int(workers)):
        print("START WORKER " + str(i))
        time.sleep(random.random())

        p = Process(target=run_worker, args=(playlist_url,))
        p.start()
        processes.append(p)

    while True:
        time.sleep(1)



if __name__ == '__main__':
    main(sys.argv)