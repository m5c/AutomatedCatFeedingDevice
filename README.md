# Automated Cat Feeding Device

A Raspi project to ensure consistent dinner times for the cat when I am not home.

## About

My cat wants food at specific hours. This repository is the blueprint for an automated cat feeding device. You fill it with food, set a timer and it keeps the food until the programmed time is up.

## Hardware

The Automated Cat Feeding Device (ACFD) consists of four hardware modules:

 * [Raspberry Pi Zero, without WiFi](https://www.buyapi.ca/product/raspberry-pi-zero-w/)
 * [Time Display PCB](timepcb/pcb.md)  
![timepcb](figures/7seg.png)
   * 1x [12 Pin Common Cathod 7-Segment Display](https://www.amazon.ca/DOLITY-Segement-Displays-Common-Cathode/dp/B07GVKQWDX/ref=sr_1_3?dchild=1&keywords=common+cathode+7+set+4+digit&qid=1621708725&sr=8-3)
   * 7x 250Ω Resistor
   * 1x [Mini PCB](https://www.amazon.ca/Gikfun-Solder-able-Breadboard-Arduino-Electronic/dp/B077938SQF/ref=sr_1_1_sspa?dchild=1&keywords=pcb+gikfun&qid=1621708675&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUE5TURQWTNOUkQ3N0QmZW5jcnlwdGVkSWQ9QTA5Mjc2MTkzRFlJRlhDOUhPQkxCJmVuY3J5cHRlZEFkSWQ9QTAyMjc0MzgyWDBQSEpTMko2M05MJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==)
   * Wires
 * [4 Button Keypad](keypcb/pcb.md)
   * 4x [Tactile Push Button](https://www.amazon.ca/Ocr-10Value-Tactile-Momentary-Assortment/dp/B01NAJEVE3/ref=sr_1_15?dchild=1&keywords=taster+button&qid=1621708366&sr=8-15)
   * 1x 250Ω Resistor
   * 1x [Mini PCB](https://www.amazon.ca/Gikfun-Solder-able-Breadboard-Arduino-Electronic/dp/B077938SQF/ref=sr_1_1_sspa?dchild=1&keywords=pcb+gikfun&qid=1621708675&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUE5TURQWTNOUkQ3N0QmZW5jcnlwdGVkSWQ9QTA5Mjc2MTkzRFlJRlhDOUhPQkxCJmVuY3J5cHRlZEFkSWQ9QTAyMjc0MzgyWDBQSEpTMko2M05MJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==)
 * Lid Lifter
   * 1x [28byj Stepper Motor](https://www.amazon.ca/Titri-28BYJ-48-Stepper-Motor-5V/dp/B07PS2MJCX/ref=sr_1_10?dchild=1&keywords=28byj&qid=1621708600&sr=8-10)
   * 1x [ULN2003 Driver Controller Board](https://www.amazon.ca/ULN2003-Controller-Stepping-Electric-Control/dp/B07P5C2KWX/ref=pd_sbs_5/143-8326619-7922505?pd_rd_w=9C9KQ&pf_rd_p=4dc33e2e-16b5-4e12-aab9-e86d5748e0cb&pf_rd_r=ZP2TV2SNF7EJDQ68PBNA&pd_rd_r=a4128fd4-54f9-4180-9a7a-c8ab0560926e&pd_rd_wg=SAr8U&pd_rd_i=B07P5C2KWX&psc=1)

## Software 

...

## Contact / Pull Requests

 * Author: Maximilian Schiedermeier ![email](email.png)
 * Github: Kartoffelquadrat
 * Webpage: https://www.cs.mcgill.ca/~mschie3
 * License: [MIT](https://opensource.org/licenses/MIT)

