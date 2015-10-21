import time
import sys
import math
class wln:
    """Program to display the remaining time of a program execution
       Usage:
    
    a=wln.wln(nitter,name='name',modulo=1)
    for i in xrange(nitter):
        # do something slow and often
        time.sleep(ttt)
        a.event()
       
    
    
    """
    def __init__(self,nitter,name="",modulo=1):
        self.start=time.time()
        self.last=self.start
        self.mean=0.0
        self.var=0.0
        self.count=0L
        self.modulo=modulo
        self.nitter=nitter
        self.name=name
        #anzahl der stellen 
        ndigits=math.floor(math.log10(self.nitter))+1
        #output format code
        self.frmt="%0"+str(ndigits)+"i"



    def event(self):
        """Increases internal counter and 
           prints some information if modulo"""
        self.zz=time.time()-self.last
        self.last=time.time()
        self.mean=self.mean*self.count+self.zz
        self.mean=self.mean/(self.count+1L)
        self.var=self.var*self.count+(self.zz-self.mean)**2
        self.var=self.var/(self.count+1L)
        self.count=self.count+1L
        
        if self.count % self.modulo  == 0: self.print_it()
        
    def print_it(self):
        
        # 012 / 100
        out = self.frmt % self.count + "/"+str(self.nitter) + "   "
        
        # 0063/1000   1.67 s (1.28 s +- 0.29 s)
        out = out + "%.4f s (%.4f s +- %.4f s)" % (self.zz,self.mean,math.sqrt(self.var))
        
        # Remaining seconds [s]:
        rem = (self.nitter-self.count)*self.mean
        
        # check if more than a day
        days = int(rem)/86400
        if days >= 1: days=str(days)+"d "
        else: days=""
        
        # Convert to nice string
        rem = "     Remaining: " +days+time.strftime("%H:%M:%S",time.gmtime(rem))
        
        #test 0057/1000   1.12 s (1.31 s +- 0.25 s)   Remaining: 00:20:39        
        out = out + rem
        
        print self.name, out ,'                 \r',
        sys.stdout.flush()

        
if __name__ == '__main__':
    import wln
    import time
    import random
    nitter = 40
    tt = 2
    a=wln.wln(nitter,name='name',modulo=1)
    for i in xrange(nitter):
        # do something slow and often
        ttt=tt*random.random()
        time.sleep(ttt)
        a.event()



        
