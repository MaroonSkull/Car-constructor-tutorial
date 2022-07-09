try:
    import RPi.GPIO as GPIO
    import psutil
    import json
    from flask import Flask, render_template
    from time import sleep
except ModuleNotFoundError:
    pass

# Глобальные переменные
Ain1 = 16   # Мотор A
Ain2 = 18
PWMA = 22
Bin1 = 13   # Мотор B
Bin2 = 15
PWMB = 11
servo = 29  # Сервопривод

# Вспомогательные функции
def cpu_temperature():
    return psutil.sensors_temperatures()['cpu_thermal'][0].current

def disk_space():
    st = psutil.disk_usage(".")
    return st.free, st.total

def cpu_load() -> int:
    return int(psutil.cpu_percent())

def ram_usage() -> int:
    return int(psutil.virtual_memory().percent)

# Моторы и серво
def moto(direction, speed):
    A = GPIO.PWM(PWMA, 100) # общаемся на рандомно выбранной частоте с драйвером моторов - 100Hz
    B = GPIO.PWM(PWMB, 100)

    if direction > 0:
        GPIO.output(Ain1,GPIO.HIGH) # Пара high/low отвечает за направление вращения
        GPIO.output(Ain2,GPIO.LOW)
        GPIO.output(Bin1,GPIO.HIGH)
        GPIO.output(Bin2,GPIO.LOW)
    else:
        GPIO.output(Ain1,GPIO.LOW)  # реверсим направление
        GPIO.output(Ain2,GPIO.HIGH)
        GPIO.output(Bin1,GPIO.LOW)
        GPIO.output(Bin2,GPIO.HIGH)

    A.start(speed)  # Отвечает за скорость вращения [0, 100]
    B.start(speed)

def setServoAngle(angle):
    pwm = GPIO.PWM(servo, 50)
    dutyCycle = angle / 18. + 8./5.
    pwm.start(dutyCycle)
    sleep(0.02)
    pwm.stop()

# Страницы сервера
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/status')
def status():
    health = {'CPUTemp': cpu_temperature(), 'CPULoad': cpu_load(), "DiskFree": disk_space()[0], "DiskTotal": disk_space()[1], "RAMUse": ram_usage()}
    return json.dumps(health).encode('utf-8')
@app.route('/control', methods=['POST'])
def control():
    res = jsonify(request.get_json(force=True));
    return res;

# init
if __name__ == '__main__':

    # Настройка GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    # Настройка моторов
    GPIO.setup(Ain1,GPIO.OUT)
    GPIO.setup(Ain2,GPIO.OUT)
    GPIO.setup(PWMA,GPIO.OUT)
    GPIO.setup(Bin1,GPIO.OUT)
    GPIO.setup(Bin2,GPIO.OUT)
    GPIO.setup(PWMB,GPIO.OUT)

    # Настройка серво
    GPIO.setup(servo, GPIO.OUT)
    setServoAngle(90)

    # Запуск flask-сервера в режиме debug
    app.run(debug=True, port=80, host='0.0.0.0')