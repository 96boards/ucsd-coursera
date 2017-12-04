//Sets the pins for sensors.
const int buttonPin = 7;	//D7
const int potPin = 0;		//A0

void setup()
{
	Serial.begin(9600);			//Begin serial communication.
	pinMode(buttonPin, INPUT);	//Sets button pin to receive input.
}

void loop()
{
	int pot = analogRead(potPin);			//Read amount turned from rotary sensor.
	int button = digitalRead(buttonPin);	//Read button state.

	//Send button and potetiometer states to clock.py through serial communication.
	Serial.print("button = ");
	Serial.print(button);
	Serial.print(", pot = ");
	Serial.println(pot);

}


