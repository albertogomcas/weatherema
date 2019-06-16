# weatherema
Control warema awning based on weather conditions

# requirements
The RF control needs aircontrol https://github.com/rfkd/aircontrol

The web interface is developed in bottle https://bottlepy.org

The weather information is retrieved using pyowm https://github.com/csparpa/pyowm

# sniffing RF codes
Build aircontrol in a raspberry pi/2/zero. Connect a RF receiver to it.
Beware typically the VCC is 5V but the pi GPIOs expect 3.3V, use a voltage divider or a logic-level translator between 
the DATA pin of the receiver and the raspberry.

execute 
aircontrol -g GPIO_PIN -s 1000 > button_1.scn
and at the same time press the button in the remote

Open the .scn in a text editor and interpret the code. Warema uses Manchester encoding. Look for the first long 
"high" (S) and start from there. The codes where in my case

Move __UP: S01100001111111 S001011110 S011100011 S

Move DOWN: S01100001111110 S001011110 S011100011 S

If you get UP working you may try just flipping the 1-0 of the first part and skip the decoding.
