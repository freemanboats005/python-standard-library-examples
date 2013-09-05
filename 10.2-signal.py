## 10.2 signal - Asynchronous System Events
# Signals provide a means of notifying a program of an event and having it handled asynchronously.
# They can be generated by the system itself, or sent from one process to another.
# Since signals interrupt the regular flow of the program, it is possible that some operations produce errors,
# especially I/O operations, when they are interrupted in the middle of happening
# Signals are identified by integers and are defined as in the operating system C headers.
# Python exposes the signals appropriate for the platform as sumbols in the signal module.
# These examples use SIDINT and SIGUSR1, both usually found on all UNIX-like systems

## Note: Programming UNIX signal handlers is not trivial.  This is merely an overview for specific cases

import signal, os, time

## 10.2.1 Receiving Signals
# Signals are received by callabck function, called a signal handler that is invoked when the signal occurs
# The arguments to the handler are the signal number and the stack frame at the point the signal originated

def receive_signal(signum, stack):
    print "Received:", signum

# register signal handlers
signal.signal( signal.SIGUSR1, receive_signal )
signal.signal( signal.SIGUSR2, receive_signal )

# Print the process ID so it can be used with kill to send this program signals
print 'My PID is:', os.getpid()

   
## 10.2.2 Retreiving Registered Handlers
# To see which signal handlers are registered for a signal, use getsignal()
# Pass the signal number as an argument.
# THe return value is the registered handler or one of the special values:
    # SIG_IGN - ignore, 
    # SIG_DFL - default behaviour, or
    # None - Existing handler registered from C, not Python

## 10.2.4 Alarms
# Alarms are a special sort of signal, where the program asks the OS to notify it after some period of time has elapsed.
# os points out this is useful for avoiding blocking indefinitely on an i/o operation or other system call
    
def receive_alarm(n, stack):
    print "Alarm :", time.ctime()
    return
    
signal.signal( signal.SIGALRM, receive_alarm)
signal.alarm(2)

# in this case, the alarm breaks the sleep in less than the 4 seconds
print "Before: ", time.ctime()
time.sleep(4)
print "After: ", time.ctime()

signals_to_names = dict(
    ( getattr(signal, n), n)
    for n in dir(signal)
    if n.startswith('SIG') and '_' not in n
)
for s, name in sorted(signals_to_names.items()):
    handler = signal.getsignal(s)
    if handler is signal.SIG_DFL:
        handler = "SIG_DFL"
    elif handler is signal.SIG_IGN:
        handler = "SIG_IGN"
    print "%-10s (%2d)" % (name, s), handler

## 10.2.3 Sending Signals
# The function for sending signals from within Pytohn is os.kill().  Its use is covered in 17.3-os.

## 10.2.5 Ignoring Signals
# To ignore a signal, register IGN_SIG as the handler.
# This script replaces the default handler for SIGINT with SIG_IGN, and registers a handler for SIGUSR1
# Then it uses signal.pause() to wait for a signal to be received
def do_exit( sig, stack ):
    raise SystemExit('Exiting')
    
signal.signal( signal.SIGINT, signal.SIG_IGN )
signal.signal( signal.SIGUSR1, do_exit )

## 10.2.6 Signals and Threads
#signals and threads do not generally mix well because the main thread of a process is the only one which will receive signals
# There is an example in the book where a thread is used to send a message back to the main process
# And an example of using an alarm that a subthread will never receive, if you want more details.


## Runcode
while True:
    print "Waiting...:"
    time.sleep(3)
    