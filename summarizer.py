from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_videoclips

from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_videoclips

import urllib.request
import json
import urllib


from pytube import YouTube

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import pandas as pd

from youtube_transcript_api.formatters import JSONFormatter
from youtube_transcript_api import YouTubeTranscriptApi

# get video id, get transcripts, store and format the data
def initializeFiles(link):
    video_id = link.split("=")[1][:11]
    YouTube(link).streams.first().download()
    print("video ",video_id)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    formatter = JSONFormatter()
    json_formatted = formatter.format_transcript(transcript)
    with open('sanjana1.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_formatted)

    read1= pd.read_json('sanjana1.json')
    read1['text'] = read1['text'].str.replace('\n',' ')
    read1['text'] = read1['text'].str.replace('”','')
    read1['text'] = read1['text'].str.replace('"','')
    read1['text'] = read1['text'].str.replace('-','')
    read1['text'] = read1['text'].str.replace('.','')
    read1['text'] = read1['text'].str.replace('$','')
    strr = read1['text'].tolist()

    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_id}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        title = (data['title'])
    title = title.replace('|','')
    title+='.mp4'
    #_______________________________________________
    return read1,strr,title

#Function to return start and end time of that subtitle
def giveTime(string,read1):
    k = read1[read1['text'].str.match(string)]
    start=k["start"]
    start=float(start)
    dur=k["duration"]
    dur = float(dur)
    end=start+dur
    print(start)
    return start,end


def formatText(strr):
    with open('srt_filet1.txt','w',encoding='utf-8') as f:
        count=0
        for i in strr:
            count+=1
            f.write('%s.\n\n' %i) 
    LANGUAGE = "english"
    parser = PlaintextParser.from_file("srt_filet1.txt", Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    return summarizer,count,parser

#Summarization and summarized video formation
def summarize(link,time1):
    k=0
    read1,strr,title = initializeFiles(link)
    summarizer,count,parser = formatText(strr)
    
    my_clip = VideoFileClip(title)
    clip1 = my_clip.subclip(0,0)
    print('Video duration : ',my_clip.duration)
    minn=int(time1)
    req=minn*60
    dur = (count/float(my_clip.duration))*req
    SENTENCES_COUNT = int(dur)
    time=0
    cj=0
    diff=0
    #print("subtitle count is ",SENTENCES_COUNT)
    while not ((req+5 >= (time)) and (req-5 <= time)):
        k=0
        cj+=1
        #print("sentence count is",SENTENCES_COUNT)
        time=0
        prdiff=diff
        prev=SENTENCES_COUNT
        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            
            sentence=str(sentence)
            strr = sentence.replace(".", " ")
            strr = strr.strip()            
            try:
                strr = strr.split("  ")
                for i in strr:
                    i=i.strip() 
                    start,end=giveTime(i,read1)       
                    start=max(k,start)
                    time+=(end-start)
                    print("Start and end time is ",start,end)
                    k=max(k,end)
                    
                    print("sentence count ",SENTENCES_COUNT)

            except:
                print("Sentence has some spl characters handle it")
        if(time<(req-6)):
            if time*2<req:
                SENTENCES_COUNT*=2
            else:
                SENTENCES_COUNT+=4
        elif(time>(req+6)):
            if time>2*req:
                SENTENCES_COUNT/=2
            else:
                SENTENCES_COUNT-=4
        diff=prev-SENTENCES_COUNT
        if(diff+prdiff == 0):
            break
        print("sentence count ",SENTENCES_COUNT)
        
    print("total iterations ",cj)
    print("_________________________________________________________________________________")
    print("total time outloop ",time)


    print("sentence count outloop",SENTENCES_COUNT)
    k=0
    time=0
    #--------------------------------------------------------------------------------------------------
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
            print(sentence)
            sentence=str(sentence)
            strr = sentence.replace(".", " ")
            strr = strr.strip()#removed rstrip
            try:
                strr = strr.split("  ")
                for i in strr:
                    i=i.strip() #added new
            #call function  to merge video
                    print("Array of sentence",i)
                    start,end=giveTime(i,read1)
                    start=max(k,start)
                    time+=(end-start)
                    print("Start and end time is loop ",start,end)
                    k=max(k,end)
                    
                    
                    clip2 = my_clip.subclip(start,end)
                    clip1 = concatenate_videoclips([clip1, clip2])

            except Exception as e:
                print("not array of sentence",strr)
                print("Strr[0] is ",i)
                print("Exception  ",e)
                break
    print("total time ",time)

    clip1.write_videofile("static/new_clip8.mov", codec = "libx264", fps=25)# new clip formed
    clip1.close()

summarize("https://www.youtube.com/watch?v=BFZtNN6eNvQ",3)

