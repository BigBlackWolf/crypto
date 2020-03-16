import pyautogui
import time
import json
import os


def listen_movement() -> list:
    scenario = []
    try:
        while True:
            x, y = pyautogui.position()
            if x == y == 0:
                break
            print(x, y)
            scenario.append((x, y))
            time.sleep(0.5)
    except KeyboardInterrupt:
        return scenario


def clean_result(inputs: list) -> list:
    last = inputs[0]
    result = []
    for i in inputs:
        if i == last and i not in result:
            result.append(i)
        last = i
    return result


def run_scenario(scenario: list, duration: int=1):
    for i in scenario:
        pyautogui.moveTo(*i, duration=duration)
        pyautogui.click()


def save_scenario(scenario: list):
    name = 'scenario.txt'
    if os.path.exists(name):
        counter = 0
        while True:
            counter += 1
            name = 'scenario{}.txt'.format(counter)
            if not os.path.exists(name):
                break

    with open(name, 'w') as file:
        jsoned = json.dumps({'data': scenario})
        file.write(jsoned)


def main(scenario: str=''):
    if not scenario:
        input('When you will be ready just press ENTER and I will record script')
        dirty = listen_movement()
        scenario = clean_result(dirty)
        save_scenario(scenario)
    with open(scenario, 'r') as file:
        data = file.read()
        scenario = json.loads(data)['data']
    run_scenario(scenario)


if __name__ == '__main__':
    main()
