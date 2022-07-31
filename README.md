# 贪吃蛇

---

## 硬件

st7735 1.44寸 128*128

4个按压式开关

---

## 电路连接

pin13 -- 开关负级 (用来控制角色的上移)

pin12 -- 开关负级 (用来控制角色的下移)

pin14 -- 开关负级 (用来控制角色的左移)

pin27 -- 开关负级 (用来控制角色的右移)

pin18 -- 开关正级

3.3v -- 屏幕VCC

GND -- 屏幕DNG

pin15 -- 屏幕SCL

pin0 -- 屏幕SDA

pin4 -- 屏幕RES

pin16 -- 屏幕DC

pin17 -- 屏幕CS

pin5 -- 屏幕BLK

![00C230A2F2B895E5D52C336E1EBAE6CC](https://user-images.githubusercontent.com/57019607/182031238-6b5ce19c-b90c-48d7-bebc-51c2c7853733.jpg)

---

## 文件

st7735.py    大佬写的 st7735驱动 (不知道是谁)

tools.py	工具库

game.py	简单的游戏框架

main.py	主程序
