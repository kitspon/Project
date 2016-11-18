#!/usr/bin/python

from bluepy import btle
import threading
import time
import BB8_driver
import sys
import cmd

mutex = threading.Lock()

class Logger(object):
    # src: http://stackoverflow.com/a/14906787

    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("logfile.log", "a")
        self.write("\nLog start: " + repr(time.time()) + "\n")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

class uhsh(cmd.Cmd):
    TIMER_DELAY = 0.1

    def __init__(self):
        cmd.Cmd.__init__(self)

        self.sp = None
        self.logging = False

    def timer_cb(self):
        if not self.sp:
            return

        self.poll(self.TIMER_DELAY/10.0, False)

        # restart timer
        threading.Timer(self.TIMER_DELAY, self.timer_cb).start()

    def default(self, line):
        if not self.sp:
            print "Not connected!"
            return False

        print 'Sending Command(%s)' % line

        mutex.acquire()
        try:
            self.sp.bt.userhack_cmd(line)
        except btle.BTLEException, e:
            print "BT FAIL:", e

            if self.sp:
                self.do_disconnect("")
        finally:
            mutex.release()

    def do_quote(self, line):
        return self.default(line)

    def do_flash(self, line):
        if not self.sp:
            print "Not connected!"
            return False

        mutex.acquire()
        try:
            self.sp.set_rgb_led(255,0,0,0,False)
            time.sleep(.2)
            self.sp.set_rgb_led(0,255,0,0,False)
            time.sleep(.2)
            self.sp.set_rgb_led(0,0,255,0,False)
            time.sleep(.2)
            self.sp.set_rgb_led(0,0,0,0,False)
        except btle.BTLEException, e:
            print "BT FAIL:", e

            if self.sp:
                self.do_disconnect("")
        finally:
            mutex.release()

    def do_connect(self, line):
        if self.sp:
            print "Already connected!"
            return False

        print "Connecting ..."
        self.sp = BB8_driver.Sphero()

        try:
            self.sp.connect()
        except btle.BTLEException, e:
            print "BT FAIL:", e
            self.sp = None
            return

        self.sp.start()
        self.sp.join()

        # activate outputs
        self.sp.bt.show_shell = True
        self.sp.bt.show_notifications = True
        print "OK"

        # start shell printout timer
        self.timer_cb()

    def do_disconnect(self, line):
        if not self.sp:
            print "Not connected!"
            return False

        print "Disconnecting ..."
        self.sp.disconnect()
        self.sp = None

    def do_quit(self, line):
        if self.sp:
            self.do_disconnect("")
        return True

    def do_log(self, line):
        if not self.logging:
            print "Logging everything to file ..."
            sys.stdout = Logger()
            self.logging = True
        else:
            print "Already active!"

    def postcmd(self, stop, line):
        """handle Async RX queue after processing command"""
        self.poll()

        return cmd.Cmd.postcmd(self, stop, line)

    def emptyline(self):
        self.poll()

    def poll(self, timeout=0.05, blocking=True):
        if self.sp:
            # don't poll concurrently
            locked = mutex.acquire(blocking)

            if not locked:
                return

            try:
                self.sp.bt.waitForNotifications(timeout)
            except btle.BTLEException, e:
                print "BT FAIL:", e

                if self.sp:
                    self.do_disconnect("")
            finally:
                mutex.release()

if __name__ == '__main__':
    u = uhsh()
    u.cmdloop("Orbotix User Hack Shell")
