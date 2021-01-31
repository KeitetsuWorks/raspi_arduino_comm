#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
## @file        arduino_comm.py
## @brief       Get A/D conversion value from Arduino
## @author      Keitetsu
## @date        2021/01/31
## @copyright   Copyright (c) 2021 Keitetsu
## @par         License
##              This software is released under the MIT License.
##

import argparse
import threading
import sys
import time
import serial

class ArduinoDataReciever(threading.Thread):

    def __init__(self, port="/dev/ttyUSB0"):
        super(ArduinoDataReciever, self).__init__()
        self.port = port
        self.received_data = {}
        self.stop = False

        # シリアルポートをオープン
        try:
            self.ser = serial.Serial(port=self.port, baudrate=9600)
        except:
            print("No Arduino found", file=sys.stderr)
            raise

        return

    def run(self):
        while (not self.stop):
            # 1行受信する
            line = self.ser.readline()
            # 改行コードを削除し，文字列に変換する
            line_string = line.strip().decode("utf-8")
            # ":"で文字列を分割する
            line_elements = line_string.split(":")
            # 分割結果が2要素であれば，第1要素のピン名をキー，第2要素を値として
            # self.received_dataに保存する
            if (len(line_elements) == 2):
                self.received_data[line_elements[0]] = int(line_elements[1])

        # シリアルポートをクローズ
        self.ser.close()

        return

def get_level_bar(value):
    char_count = int(40 * (value / 1023))
    level_bar = " " * (40 - char_count) + "#" * char_count

    return level_bar

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Get A/D conversion value from Arduino"
    )
    parser.add_argument(
        "--port",
        "-p",
        type = str,
        default = "/dev/ttyUSB0",
        help = "Serial port (Arduino)"
    )
    args = parser.parse_args()

    # 引数を変数に格納
    port = args.port

    # A/D変換ピンのリスト
    adc_pins = ("A0",)

    # Arduinoからのデータを受信するスレッドを作成
    t = ArduinoDataReciever(port)

    # スレッドを実行
    t.start()

    try:
        print("Press Ctrl+C to quit")
        while True:
            for adc_pin in adc_pins:
                if (adc_pin in t.received_data):
                    # ピン名が一致する値が存在する場合は，その値とレベルバーを表示する
                    adc_value = t.received_data[adc_pin]
                    level_bar = get_level_bar(adc_value)
                    print("%s: %4d [%s]" % (adc_pin, adc_value, level_bar))
                else:
                    # ピン名が一致する値が存在しない場合は，"N/A"と表示する
                    print("%s:  N/A" % (adc_pin))
            # 表示行数分だけカーソルを上に移動する
            sys.stdout.write("\x1b[%dF" % (len(adc_pins)))
            time.sleep(0.2)
    except KeyboardInterrupt:
        # Ctrl+Cが押下された場合はスレッドを終了する
        t.stop = True

    # スレッドの終了まで待機
    t.join()    
