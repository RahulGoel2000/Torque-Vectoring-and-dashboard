#include<Wire.h>
float num = 1000 , ir_sum = 0 , il_sum  = 0 , il = 0 , ir = 0  ;
int c_r =0 , c_l = 0;
volatile int send_count = 0 ;
void setup()
{
  Serial.begin(9600);
  Wire.begin(0x09);
  Wire.onRequest(send);
  pinMode(A0 , OUTPUT);
  pinMode(A1 , OUTPUT);
  pinMode(A6 , INPUT);

  pinMode(A5 , INPUT);
  pinMode(A7 , INPUT);
  
   Wire.begin(0x09);
  Wire.onRequest(send);
}
void loop()
{
 
  
  for( int i =0 ; i< num ; i++)
  {
    il_sum += analogRead(A7);
    ir_sum += analogRead(A6);
  }
  il = abs(il_sum/num);
  ir = abs(ir_sum / num);
  il_sum = 0;
  ir_sum  = 0;
  Serial.print(c_r );

  Serial.print("  ");
  Serial.print(c_l);
  Serial.print("  ");
  
  if(abs(ir-534)/33.3 > 0.19)
  {
    Serial.print((abs(ir-534)/17.3) );
    c_r = abs((ir-534)/17.3)*10;
  }
  else
  {
    Serial.print((abs(ir-534)/33.3) );
    c_r = abs((ir-534)/33.3)*10;
  }
  Serial.print("  ");
  Serial.println(abs(il -534)/15.3);
  c_l = abs((il -534)/15.3)*10;
}
void send()
{
   send_count++;
   final(send_count);
}
void final(int sen)
{
  if(sen ==1)
  {
    Wire.write(((abs(c_l)) | 0b10000000));
    return;
  }
  if(sen == 2)
  {
    Wire.write((abs((c_r)) & 0b01111111));
    send_count = 0;
    return;
  } 
}
