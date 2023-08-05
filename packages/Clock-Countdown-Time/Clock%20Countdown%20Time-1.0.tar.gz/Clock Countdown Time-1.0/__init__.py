from time import sleep
#This module was created by JohanCoder
#If you want you can add me in the description of your creation, but this isn't nessecary

class time:
    
    #Making a function called "time"
    def time(sec, min, hr):
        hr = hr
        min = min
        sec = sec
        done = False

        #Making counter
        hrs = 0
        mins = 0
        secs = 0

        #Counting seconds
        while secs != sec:
            secs += 1
            sleep(1)
            print(secs)
        
        if secs == sec:
            print("Seconds Done")

        #Counting minutes
        while mins != min:
            mins += 1
            sleep(60)
            print(mins)

        if mins == min:
            print("Minutes Done")

        #Counting hours
        while hrs != hr:
            hrs += 1
            sleep(3600)
            print(hrs)

        #Checking if time is up
        if secs == sec:
            if mins == min:
                if hrs == hr:
                    print("Fully Done!")
                    done = True

#Usage: when you have downloaded and installed the module, you have to write "import johan_time" and then you can call it using time.time(secs, mins, hrs)