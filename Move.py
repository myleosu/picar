import RPi.GPIO as GPIO
import time

class Move:
    def __init__(self):
        self.PWMA = 18
        self.AIN1 = 22# 左侧前轮引脚编号
        self.AIN2 = 27# 左侧后轮引脚编号

        self.PWMB = 23
        self.BIN1 = 25# 右侧前轮引脚编号
        self.BIN2 = 24# 右侧后轮引脚编号
        self.speed = 10# 初始速度
        self.set_up_All()# 初始化所有引脚

    def __del__(self):
        GPIO.cleanup()# 释放资源

    def set_up_All(self):
        # 取消警告
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # 设置为BCM编码
        # 启动输入输出IO口
        GPIO.setup(self.AIN2, GPIO.OUT)
        GPIO.setup(self.AIN1, GPIO.OUT)
        GPIO.setup(self.PWMA, GPIO.OUT)

        GPIO.setup(self.BIN1, GPIO.OUT)
        GPIO.setup(self.BIN2, GPIO.OUT)
        GPIO.setup(self.PWMB, GPIO.OUT)

        # PWM我理解为是一个信号强度，通过控制这个强度大小，我们可以控制小车的速度，初始化为100
        self.L_Motor = GPIO.PWM(self.PWMA, self.speed)
        self.L_Motor.start(0)# 初始化时速度为0

        self.R_Motor = GPIO.PWM(self.PWMB, self.speed)
        self.R_Motor.start(0)# 初始化时速度为0
    
    def reset(self):
        self.L_Motor.ChangeDutyCycle(0)
        GPIO.output(self.AIN2, False)  # AIN2
        GPIO.output(self.AIN1, False)  # AIN1

        self.R_Motor.ChangeDutyCycle(0)
        GPIO.output(self.BIN2, False)  # BIN2
        GPIO.output(self.BIN1, False)  # BIN1

    def turn_up(self, run_speed=-1, run_time=-1):
        self.reset()
        if run_speed == -1:
            run_speed = self.speed
        
        self.L_Motor.ChangeDutyCycle(run_speed)
        GPIO.output(self.AIN2, False)  # AIN2
        GPIO.output(self.AIN1, True)  # AIN1

        self.R_Motor.ChangeDutyCycle(run_speed)
        GPIO.output(self.BIN2, False)  # BIN2
        GPIO.output(self.BIN1, True)  # BIN1
        if run_time != -1:
            time.sleep(run_time)

    def turn_back(self, run_speed=-1, run_time=-1):
        self.reset()
        if run_speed == -1:
            run_speed = self.speed
        
        self.L_Motor.ChangeDutyCycle(run_speed)
        GPIO.output(self.AIN2, True)  # AIN2
        GPIO.output(self.AIN1, False)  # AIN1

        self.R_Motor.ChangeDutyCycle(run_speed)
        GPIO.output(self.BIN2, True)  # BIN2
        GPIO.output(self.BIN1, False)  # BIN1

        if run_time != -1:
            time.sleep(run_time)

    def turn_left(self, run_speed=-1, run_time=-1):
        self.reset()
        if run_speed == -1:
            run_speed = self.speed
        
        self.L_Motor.ChangeDutyCycle(run_speed)
        # 小车左转弯的第一种方式
        GPIO.output(self.AIN2, True)  # AIN2
        # 小车左转弯的第二种方式
        # GPIO.output(self.AIN2,False)  # AIN2
        GPIO.output(self.AIN1, False)  # AIN1

        self.R_Motor.ChangeDutyCycle(run_speed)
        GPIO.output(self.BIN2, False)  # BIN2
        GPIO.output(self.BIN1, True)  # BIN1
        if run_time != -1:
            time.sleep(run_time)
    
    def turn_right(self, run_speed=-1, run_time=-1):
        self.reset()
        if run_speed == -1:
            run_speed = self.speed
        
        self.L_Motor.ChangeDutyCycle(run_speed)
        GPIO.output(self.AIN2, False)  # AIN2
        # 小车右转弯的第一种方式
        GPIO.output(self.AIN1, True)  # AIN2
        # 小车右转弯的第二种方式
        # GPIO.output(self.AIN1, False)  # AIN1

        self.R_Motor.ChangeDutyCycle(run_speed)
        GPIO.output(self.BIN2, True)  # BIN2
        GPIO.output(self.BIN1, False)  # BIN1
        if run_time != -1:
            time.sleep(run_time)

    def turn_stop(self, run_time=-1):
        self.reset()
        if run_time != -1:
            time.sleep(run_time)


    # def turn_up_left(self, run_speed=-1, run_time=-1):
    #     self.reset()
    #     if run_speed == -1:
    #         run_speed = self.speed
        
    #     self.L_Motor.ChangeDutyCycle(run_speed)
    #     # 小车左转弯的第一种方式
    #     # GPIO.output(self.AIN2, True)  # AIN2
    #     # 小车左转弯的第二种方式
    #     GPIO.output(self.AIN2,False)  # AIN2
    #     GPIO.output(self.AIN1, False)  # AIN1

    #     self.R_Motor.ChangeDutyCycle(run_speed)
    #     GPIO.output(self.BIN2, False)  # BIN2
    #     GPIO.output(self.BIN1, True)  # BIN1
    #     if run_time != -1:
    #         time.sleep(run_time)

    # # 向左掉头
    # def t_left_down(self):
    #     self.t_left(50,1.0)
    #     self.t_stop(0.5)
    #     self.t_up(20,1.0)
    #     self.t_stop(0.5)
    #     self.t_left(50,1.0)

    # # 向右掉头
    # def t_right_down(self):
    #     self.t_right(50,1.0)
    #     self.t_stop(0.5)
    #     self.t_up(20,1.0)
    #     self.t_stop(0.5)
    #     self.t_right(50,1.0)

if __name__ == '__main__':
    car = Move()
    car.turn_up(run_speed=20, run_time=0.5)
    car.turn_back(run_speed=20, run_time=0.5)
    car.turn_left(run_speed=30, run_time=0.5)
    car.turn_right(run_speed=30, run_time=0.5)
    # car.turn_up_left(run_speed=30, run_time=2)
    # GPIO.cleanup()# 释放资源