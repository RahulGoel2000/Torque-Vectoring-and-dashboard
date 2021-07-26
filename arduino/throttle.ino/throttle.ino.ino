#include<Wire.h>
float rawThrottle = 0,preval = 0;
int send_count = 0 , MSB = 0,LSB=0;
void setup() {
  Wire.begin(0x07);
  Wire.onRequest(send);
  pinMode(A7 , INPUT_PULLUP);
  Serial.begin(9600);
  preval = analogRead(A7);
}
 
void loop() {
  //Serial.println(analogRead(A7));
}

void send()
{  
  send_count++;
  final(send_count);
}
/*void final(int sen_count)
{
  if(sen_count == 1)`
  {
    Wire.write(1);
    return ;
  }

  if(sen_count == 2)
  {
    Wire.write(MSB);
    
    return ;
  }
  if(sen_count == 3)
  {
    Wire.write(0);
    return ;
  }

  if(sen_count == 4)
  {
    Wire.write(LSB);
    send_count =0;
    return ;
  }
}*/
void final(int sen)
{
  if(sen ==1)
  {
    Wire.write(MSB & 0b01111111);
    return;
  }

   if(sen ==2)
  {
    Wire.write(LSB | 0b10000000);
    send_count = 0;
    msb_lsb_gen(analogRead(A7));
    return;
  }
}

float diff(float a, float b)
{
  if (a > b)
  {

    return a - b;
  }
  else {
    return b - a;
  }
}
void msb_lsb_gen(int val)
{
/*Serial.print("  ");
  if(diff(val , preval)>100)
  {
    val = preval;
  }
  preval = val;*/
  MSB = int(val/100.0);
  LSB = val - MSB*100;
  //Serial.println(val);
}
