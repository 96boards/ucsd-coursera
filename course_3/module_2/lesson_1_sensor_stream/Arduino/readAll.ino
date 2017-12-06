#include <math.h>

const int B = 4275;               // B value of the thermistor
const int R0 = 100000;            // R0 = 100k
const int pinTempSensor = A0;     // Grove - Temperature Sensor connect to A5
const int lightPin = A1;
const int soundPin = A2;

void setup()
{
	Serial.begin(9600);
}

void loop()
{
//Temperature Reading
	int a = analogRead(pinTempSensor);

	float R = 1023.0/a-1.0;
	R = R0*R;

	float temperature = 1.0/(log(R/R0)/B+1/298.15)-273.15; // convert to temperature via datasheet

//Light Reading
	int light_level = analogRead(lightPin);

//Sound Reading
	int sound_level = analogRead(soundPin);

	Serial.print("temperature = ");
	Serial.print(temperature);
	Serial.print(", light = ");
	Serial.print(light_level);
	Serial.print(", sound = ");
	Serial.println(sound_level);

	delay(500);
}


