import pyaudio
import struct
import math
import pyautogui
INITIAL_TAP_THRESHOLD = 0.18
FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
RATE = 44100   
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
OVERSENSITIVE = 15.0/INPUT_BLOCK_TIME                    
UNDERSENSITIVE = 120.0/INPUT_BLOCK_TIME 
MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME
global amplitude

global c
def get_rms( block ):

    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    sum_squares = 0.0
    for sample in shorts:
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

class TapTester(object):
    def _init_(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.tap_threshold = INITIAL_TAP_THRESHOLD
        self.noisycount = MAX_TAP_BLOCKS+1 
        self.quietcount = 0 
        self.errorcount = 0

    def stop(self):
        self.stream.close()

    def find_input_device(self):
        device_index = None            
        for i in range( self.pa.get_device_count() ):     
            devinfo = self.pa.get_device_info_by_index(i)   

            for keyword in ["mic","input"]:
                if keyword in devinfo["name"].lower():
                    device_index = i
                    return device_index

        if device_index == None:
            print( "No input device" )

        return device_index

    def open_mic_stream( self ):
        device_index = self.find_input_device()

        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = device_index,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return stream

    def tapDetected(self):
        global c

        c=c+1
        
        

    def listen(self):
        global amplitude
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        except e:
            self.errorcount += 1
            print( "(%d) Error recording: %s"%(self.errorcount,e) )
            self.noisycount = 1
            return

        amplitude = get_rms( block )
        if amplitude > self.tap_threshold:
            self.quietcount = 0
            self.noisycount += 1
        else:            
            if 1 <= self.noisycount <= MAX_TAP_BLOCKS:
                self.tapDetected()
            self.noisycount = 0
            self.quietcount += 1

def auto(c):
        if(selection==1):
            if c==1:
                pyautogui.press('right')
            if c==2:
                pyautogui.press('left')
            if c==3:
                pyautogui.press('esc')    
        if(selection==2):
            if c==1:
                pyautogui.press('playpause')
            if c==2:
                pyautogui.press('nexttrack')
            if c==3:
                pyautogui.press('prevtrack')              
        if(selection==3):
            pyautogui.press('space',interval=0.25)
        print (c)
        print(amplitude)

if _name_ == "_main_":
    c=0
    print("Welcome, What would you like to automate today?")
    print("~~~~~~~~~~~~~~~~~")
    print("Press Number Followed by Enter")
    print("SlideShow-1, Music-2, Video-3")
    selection=int(input());
    if selection==1:
      print("open a PPT presentation")
    elif selection ==2:
      print("Open music player")
    elif selection==3:
      print("Open a video")
    else:
     print("Invalid choice")
    tt = TapTester()
   
    
    for i in range(10000):
        if(i%30==0):
            if(c>0):
                auto(c)
            c=0
        tt.listen()
