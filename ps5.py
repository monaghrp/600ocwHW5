# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, subject, summary, link):
        self.guid=guid
        self.title=title
        self.subject=subject
        self.summary=summary
        self.link=link
    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link
        
#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger
class WordTrigger(Trigger):
    def __init__(self,Trigger):
        Trigger.__init__(self)
        self.trigger=Trigger.lower()
        ##print "'"+ str(self.trigger)+"'"
    def is_word_in(self,text):
        temp=text.lower()
        ##print str(temp)
        for i in xrange(0,len(string.punctuation)):
            temp=temp.replace(string.punctuation[i],' ')
        split_words=temp.split()
        if self.trigger in split_words:
            return True
        else:
            return False
# TODO: TitleTrigger
class TitleTrigger(WordTrigger):
    def evaluate(self,story):
        return self.is_word_in(story.get_title())
# TODO: SubjectTrigger

class SubjectTrigger(WordTrigger):
    def evaluate(self,story):
        return self.is_word_in(story.get_subject())
    
# TODO: SummaryTrigger
class SummaryTrigger(WordTrigger):
    def evaluate(self,story):
        return self.is_word_in(story.get_summary())

# Composite Triggers
# Problems 6-8

# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self,Trigger):
        self.trigger=Trigger
    def evaluate(self, story):
        return not self.trigger.evaluate(story)
    
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self,Trigger1, Trigger2):
        self.trigger1=Trigger1
        self.trigger2=Trigger2
    def evaluate(self, story):
        return (self.trigger1.evaluate(story) and self.trigger2.evaluate(story))
                
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self,Trigger1, Trigger2):
        self.trigger1=Trigger1
        self.trigger2=Trigger2
    def evaluate(self, story):
        return (self.trigger1.evaluate(story) or self.trigger2.evaluate(story))

# Phrase Trigger
# Question 9

# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self,Trigger):
        self.trigger=Trigger
    def evaluate(self, story):
        temp1=self.trigger in story.get_subject()
        temp2=self.trigger in story.get_title()
        temp3=self.trigger in story.get_summary()
        
        return (temp1 or temp2 or temp3)

#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    result=[]
    trigger_count=0
    for i in xrange(0,len(stories)):
        for j in xrange(0,len(triggerlist)):
            ##print str(triggerlist[j].evaluate(stories[i]))
            if triggerlist[j].evaluate(stories[i]):
                trigger_count+=1
        if trigger_count>=1:
            ##print 'found at least 1 trigger'
            result.append(stories[i])
        trigger_count=0
    # TODO: Problem 10
    # This is a placeholder (we're just returning all the stories, with no filtering) 
    # Feel free to change this line!
    ##print str(result)
    return result

#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    # TODO: Problem 11
    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    trigger_list=[]
    trigger_return=[]
    for i in xrange(len(lines)):
        if lines[i][0]=='t':
            temp=lines[i].split()
            if temp[1]=='TITLE':
                ##print 'found TITLE'
                ##print "'" + str(lines[i][9:len(lines[i])]) + "'"
                trigger_list.append(TitleTrigger(lines[i][9:len(lines[i])]))
            elif temp[1]=='SUBJECT':
                ##print 'found SUBJECT'
                ##print "'" + str(lines[i][11:len(lines[i])]) + "'"
                trigger_list.append(SubjectTrigger(lines[i][11:len(lines[i])]))
            elif temp[1]=='SUMMARY':
                ##print 'found SUMMARY'
                ##print "'" + str(lines[i][11:len(lines[i])]) + "'"
                trigger_list.append(SummaryTrigger(lines[i][11:len(lines[i])]))
            elif temp[1]=='NOT':
                ##print 'found NOT'
                ##print str(temp[2][1])
                ##print str(trigger_list[int(temp[2][1])-1]) + "'"
                trigger_list.append(NotTrigger(trigger_list[int(temp[2][1])-1]))
            elif temp[1]=='AND':
                ##print 'found AND'
                ##print 'trigger1: ' +str(temp[2][1])
                ##print 'trigger1: ' +str(temp[3][1])
                t1=trigger_list[int(temp[2][1])-1]
                t2=trigger_list[int(temp[3][1])-1]
                trigger_list.append(AndTrigger(t1,t2))
            elif temp[1]=='OR':
                ##print 'found OR'
                ##print 'trigger1: ' +str(temp[2][1])
                ##print 'trigger1: ' +str(temp[3][1])
                t1=trigger_list[int(temp[2][1])-1]
                t2=trigger_list[int(temp[3][1])-1]
                trigger_list.append(OrTrigger(t1,t2))
            elif temp[1]=='PHRASE':
                ##print 'found PHRASE'
                ##print "'" + str(lines[i][10:len(lines[i])]) + "'"
                trigger_list.append(PhraseTrigger(lines[i][10:len(lines[i])]))
        if lines[i][0:3]=='ADD':
            ##print 'found ADD'
            temp=lines[i].split()
            for j in xrange(1,len(temp)):
                ##print str(trigger_list[int(temp[j][1])-1])
                trigger_return.append(trigger_list[int(temp[j][1])-1])
    return trigger_return
    
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    ##t1 = SubjectTrigger("Chong")
    ##t2 = SummaryTrigger("NSA")
    ##t3 = PhraseTrigger("Snowden")
    ##t4 = OrTrigger(t2, t3)
    ##triggerlist = [t1, t4]
    
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))
        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
        
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

