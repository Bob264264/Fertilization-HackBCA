/******************************************************************************/
/*macro definitions of Rotary angle sensor*/
#define xROTARY_ANGLE_SENSOR A0
#define yROTARY_ANGLE_SENSOR A1
#define ADC_REF 5//reference voltage of ADC is 5v
#define GROVE_VCC 5//VCC of the grove interface is normally 5v
#define FULL_ANGLE 265//full value of the rotary angle is 300 degrees
void setup() 
{
    Serial.begin(9600);
    pinsInit();
}

void loop() 
{
    int xDegrees = map(getDegree(xROTARY_ANGLE_SENSOR),0,FULL_ANGLE,-FULL_ANGLE/20,FULL_ANGLE/20);
    int yDegrees = map(getDegree(yROTARY_ANGLE_SENSOR),0,FULL_ANGLE,FULL_ANGLE/20,-FULL_ANGLE/20);
    String out =  String(xDegrees) + " " + String(yDegrees);
    Serial.println(out);
    
//    Serial.print(xDegrees);
//    Serial.print(" ");
//    Serial.println(yDegrees);
    delay(100);
}
void pinsInit()
{
    pinMode(xROTARY_ANGLE_SENSOR, INPUT);
    pinMode(yROTARY_ANGLE_SENSOR, INPUT);
}

/*Function: Get the angle between the mark and the starting position    */
/*Parameter:-int, the pin number */
/*Return:   -int,the range of degrees is 0 to 300 */
int getDegree(int pin)
{
    int sensor_value = analogRead(pin);
    float voltage;
    voltage = (float)sensor_value*ADC_REF/1023;
    float degrees = (voltage*FULL_ANGLE)/GROVE_VCC;
    return degrees;
}
