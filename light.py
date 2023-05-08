from machine import Pin,PWM
import time

pin4 = Pin(4, Pin.OUT)
pin4.value(0)
pwm1 = PWM(Pin(5), freq=50)
pwm2 = PWM(Pin(0), freq=50)
yled = PWM(Pin(4), freq=50, duty=0)
wled = PWM(Pin(13), freq=50, duty=0)
p15 =Pin(15, Pin.OUT)
p15.off()
button = Pin(14, Pin.IN)
file = open('data.txt', 'r')
data = file.read().split(',')
status = int(data[0])
mode = int(data[1])
brightness = int(data[2])
file.close()


def closing(status):
    global pwm1,pwm2 
    if status:
        for x in range(1,91):
            pwm1.duty(int((0.5+x/90)/20*1023))
            pwm2.duty(int((1.5-x/90)/20*1023))
            time.sleep(0.01)
    else:
        for x in range(1, 91):
            pwm1.duty(int((1.5-x/90)/20*1023))
            pwm2.duty(int((0.5+x/90)/20*1023))
            time.sleep(0.01)
def modeswitch():
    global mode
    if mode >= 2:
        mode = 0
    else:
        mode += 1

def lightswitch():
    global status
    status = not status
    closing(status)
    pwm1.duty(0)
    pwm2.duty(0)

def sync():
    global brightness
    if status:
        if brightness > 100:
            brightness = 100
        if mode == 0:
            yled.duty(0)
            wled.duty(int(brightness*10.24-1))
        if mode == 1:
            wled.duty(0)
            yled.duty(int(brightness*10.24-1))
        if mode == 2:
            wled.duty(int(brightness*10.24-1))
            yled.duty(int(brightness*10.24-1))
    else:
        wled.duty(0)
        yled.duty(0)
    file1 = open('data.txt', 'w')
    file1.write(str(int(status))+','+str(mode)+','+str(brightness))
    file1.close()
    print(status,mode,brightness)

sync()

while True:
    if button.value():
        start = time.ticks_ms()
        while button.value():
            delta1 = time.ticks_diff(time.ticks_ms(), start)
            if delta1 > 500:
                if status == 1:
                    if brightness < 100:
                        while button.value():
                            if brightness < 100:
                                brightness = brightness + 1
                                sync()
                                time.sleep(0.01)
                    if brightness == 100: 
                        while button.value():
                            if brightness >70:
                                brightness = brightness - 1
                                sync()
                                time.sleep(0.01)

        if delta1 > 500:
            pass
        else:
            start = time.ticks_ms()
            if not status:
                lightswitch()
                sync()
                time.sleep(1)
            else:
                while not button.value():
                    delta2 = time.ticks_diff(time.ticks_ms(), start)
                    if delta2 >= 500:
                        break
                if delta2 < 500:
                    modeswitch()
                    sync()
                    time.sleep(0.5)
                else:
                    lightswitch()
                    sync()
                    time.sleep(0.5)





