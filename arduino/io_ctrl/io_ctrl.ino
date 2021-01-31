/**
 * @file        io_ctrl.ino
 * @brief       Arduino I/O Controller
 * @author      Keitetsu
 * @date        2021/01/31
 * @copyright   Copyright (c) 2021 Keitetsu
 * @par         License
 *              This software is released under the MIT License.
 */

#define ADC_NUM 1         /**< A/D変換ピンの数 */
#define BUF_SIZE 8        /**< シリアル通信の送信バッファのサイズ */
#define INTERVAL_TIME 500 /**< 周期実行の間隔 */

/**
 * @brief       A/D変換ピンのリスト
 */
uint8_t adc_pins[ADC_NUM] = {0};
unsigned long prev_time;     /**< 周期実行の前回実行時刻 */
unsigned long interval_time; /**< 周期実行の間隔 */

/**
 * @brief       入出力値のシリアル送信
 */
void sendData()
{
    uint8_t i;
    int adc_value;
    char buf[BUF_SIZE];

    // A/D変換ピンの値を取得して，送信する
    for (i = 0; i < ADC_NUM; i++) {
        adc_value = analogRead(adc_pins[i]);
        sprintf(buf, "A%u:%u", adc_pins[i], adc_value);
        Serial.println(buf);
    }
}

/**
 * @brief       セットアップ関数
 */
void setup()
{
    Serial.begin(9600);

    prev_time = 0;
    interval_time = INTERVAL_TIME;
}

/**
 * @brief       ループ関数
 */
void loop()
{
    unsigned long curr_time;

    // 現在時刻を取得する
    curr_time = millis();

    // 周期実行
    if ((curr_time - prev_time) >= interval_time) {
        prev_time += interval_time;
        sendData();
    }
}
