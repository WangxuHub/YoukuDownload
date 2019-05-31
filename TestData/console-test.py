import sys
import  time
import progressbar as pb


def dosomework():
    time.sleep(0.01)

print(111)
print(111)
print(111)

def startProcess():
    total = 1000
    widgets = ['Progress: ', pb.Percentage(), ' ', pb.Bar('#'), ' ', pb.Timer(),
            ' ', pb.ETA(), ' ', pb.FileTransferSpeed()]
    pbar = pb.ProgressBar(widgets=widgets, maxval=10*total).start()
    for i in range(total):
        # do something
        pbar.update(10 * i + 1)
        dosomework()
    pbar.finish()

startProcess()

print(111)
print(111)
print(111)
# sys.stdin.
