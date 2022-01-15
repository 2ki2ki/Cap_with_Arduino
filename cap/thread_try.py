from random import shuffle
from time import perf_counter
from typing import Callable, List, Tuple
import numpy as np
import sounddevice as sd
from amas.agent import OBSERVER, Agent, NotWorkingError, Observer
from pino.ino import HIGH, LOW, Arduino
import cv2

STIMULATOR = "STIMULATOR"
READER = "READER"
RECORDER = "RECORDER"


def packing(event: int) -> Tuple[float, int]:
    return (perf_counter(), event)


def init_iti(var: dict) -> List[float]:
    mean = var.get("mean-iti")
    _range = var.get("range-iti")
    trial = var.get("trial", 0)
    if mean < _range or trial < 1:
        raise ValueError
    d = 2 * _range
    e = _range / trial
    _min = mean - _range
    itis = [(_min + (step * d / trial)) + e for step in range(trial)]
    shuffle(itis)
    return itis


def make_pure_tone(amp: float, freq: int, samplerate: int,
                   t: float) -> np.ndarray:
    return amp * np.sin(2.0 * np.pi * freq * np.arange(samplerate * t) /
                        samplerate).astype(np.float32)


def set_speaker(tone: np.ndarray, samplerate: int) -> Callable:
    def sound():
        sd.play(tone, samplerate=samplerate)
        return None

    return sound


async def stimulate(agent: Agent, ino: Arduino, beep: Callable,
                    var: dict) -> None:
    cs = 100
    us = var.get("us", 12)
    air = var.get("air", 11)
    us_duration = var.get("us-duration")
    air_duration = 0.02
    # air_duration = var.get("air-duration")
    cs_duration = expvars.get("cs-duration")
    intervals = init_iti(var)
    agent.send_to(RECORDER, (perf_counter(), 0))
    try:
        count = 0
        for interval in intervals:
            count += 1
            await agent.sleep(interval)
            if count%3 == 0:
                ino.digital_write(us, HIGH)
                agent.send_to("CAP","peak")
                await agent.sleep(us_duration)
                ino.digital_write(us, LOW)
                agent.send_to("CAP",False)
                agent.send_to(RECORDER, packing(us))
                print("peak")
            else:
                ino.digital_write(us, HIGH)
                agent.send_to("CAP","FT")
                await agent.sleep(us_duration)
                ino.digital_write(us, LOW)
                agent.send_to("CAP",False)
                agent.send_to(RECORDER, packing(us))
                print("US")
            print(count)
        agent.send_to(RECORDER, packing(1))
    except NotWorkingError:
        agent.send_to(RECORDER, packing(-1))
    agent.send_to(OBSERVER, "done")

    return None


async def camera(agent):
    cap = cv2.VideoCapture(1)
    led_on =False
    fps = int(cap.get(cv2.CAP_PROP_FPS))                    # カメラのFPSを取得
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))              # カメラの横幅を取得
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))             # カメラの縦幅を取得
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # 動画保存時のfourcc設定（mp4用）
    video = cv2.VideoWriter('video.mp4', fourcc, fps, (w, h))

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        re_color_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
        if not ret:
            continue

        mess = await agent.try_recv(0.001)

        if mess is not None:
            led_on = mess[1]

        if led_on == "type01":
            cv2.circle(re_color_frame, (550, 20), 15, (255, 255, 255), thickness=-1)
        elif led_on == "type02":
            cv2.circle(re_color_frame, (600, 20), 15, (255, 255, 255), thickness=-1)
        elif led_on == "end":
            break

        cv2.imshow('frame',re_color_frame)
        video.write(re_color_frame)
        await agent.sleep(0.00001)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    video.release
    cv2.destroyAllWindows()



async def read(agent: Agent, ino: Arduino) -> None:
    try:
        while agent.working():
            v = await agent.call_async(ino.read_until_eol)
            if v is None:
                continue
            s = v.rstrip().decode("utf-8")
            agent.send_to(RECORDER, packing(s))
    except NotWorkingError:
        ino.cancel_read()
        pass
    return None


async def record(agent: Agent, filename: str) -> None:
    packs: List[Tuple[float, int]] = []
    try:
        while agent.working():
            _, mess = await agent.recv()
            print(mess)
            packs.append(mess)
    except NotWorkingError or KeyboardInterrupt:
        pass
    with open(filename, "w") as f:
        f.write("time, event\n")
        for pack in packs:
            t, e = pack
            f.write(f"{t}, {e}\n")
    return None


async def observe(agent: Observer) -> None:
    while agent.working():
        _, mess = await agent.recv(t=2.0)
        if mess == "done":
            agent.send_all(mess)
            agent.finish()
            break
    return None


async def watch(agent: Agent) -> None:
    while agent.working():
        _, mess = await agent.recv_from_observer()
        if mess == "done":
            agent.finish()
            break
    return None


if __name__ == '__main__':
    from pino.ino import Comport, OUTPUT, SSINPUT_PULLUP
    from pino.ui import clap
    from amas.env import Environment
    from amas.connection import Register
    from datetime import datetime

    config = clap.PinoCli().get_config()
    expvars = config.get_experimental()
    meta = config.get_metadata()

    SAMPLERATE = expvars.get("samplerate")
    cs_duration = expvars.get("cs-duration")
    freq = expvars.get("Hz")
    amp = expvars.get("amplifer", 10.0)
    cs = make_pure_tone(amp, freq, SAMPLERATE, cs_duration)
    sd.default.device = expvars.get("speaker")
    sound = set_speaker(cs, samplerate=SAMPLERATE)

    us = expvars.get("us")
    us_duration = expvars.get("us_duration")
    lick = expvars.get("lick")

    now = datetime.now().strftime("%y-%m-%d-%H-%M")
    sub = meta.get("subject")
    cond = meta.get("condition")
    filename = f"{now}_{sub}_{cond}.csv"

    com = Comport() \
        .apply_settings(config.get_comport()) \
        .set_timeout(2.0) \
        .deploy() \
        .connect()

    ino = Arduino(com)
    ino.set_pinmode(us, OUTPUT)
    ino.set_pinmode(11, OUTPUT)
    ino.set_pinmode(lick, SSINPUT_PULLUP)

    stimulator = Agent(STIMULATOR)
    stimulator.assign_task(stimulate, ino=ino, beep=sound, var=expvars) \
        .assign_task(watch)

    reader = Agent(READER)
    reader.assign_task(read, ino=ino) \
        .assign_task(watch)

    recorder = Agent(RECORDER)
    recorder.assign_task(record, filename=filename) \
        .assign_task(watch)

    videocap = Agent("CAP").assign_task(camera)

    observer = Observer()
    observer.assign_task(observe)

    rgist = Register([stimulator, reader, recorder, observer,videocap])

    env = Environment([stimulator, reader, recorder, observer,videocap])
    env.run()


