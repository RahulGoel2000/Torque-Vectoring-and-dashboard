#include<Wire.h>
volatile boolean first;
volatile boolean triggered;
volatile unsigned long overflowCount;
volatile unsigned long startTime=0;
volatile unsigned long finishTime=0;
unsigned long elapsedTime;
volatile float freq = 0 , f_pre = 0;
volatile int send_count = 1 , counterd=0  ;

volatile byte  MSB = 0 , LSB = 0 ;

// here on rising edge
void msb_lsb_gen()
{
  int temp = int(freq);
  MSB = int(freq/10.0);
  LSB = temp - MSB*10;
   
 
}

void final(int sen)
{
  
  if(sen ==1)
  {
    Wire.write(MSB | 0b10000000);
    return;
  }
  if(sen == 2)
  {
    Wire.write(LSB & 0b00111111);
    send_count = 0;
    return;
  }
 
}
void send()
{ 
   send_count++;
   final(send_count);
   
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
void isr () 
{
  
  unsigned int counter = TCNT1;  // quickly save it
  
  
  if (first)
    {
     // counterd++;
      
    startTime = (overflowCount << 16) + counter;
    first = false;
    return;  
    }
  
  finishTime = (overflowCount << 16) + counter;
  elapsedTime = finishTime - startTime;
  
  //Serial.print(String(elapsedTime) + " ");
  freq = F_CPU*2.5/elapsedTime;
  if( abs(f_pre - freq) > 60)
  {
    freq = f_pre;
  }
  f_pre = freq;
  msb_lsb_gen();
  /*if(diff(freq ,freq_pre) >40)
{
  freq = freq_pre;
}
  //freq = (freq - freq_pre)*1 + freq_pre;
  freq_pre = freq;*/
 // triggered = true;
  
  float a  = freq;
  Serial.println(a);
  /*Serial.print("  ");
  Serial.print(MSB);
  Serial.print("  ");
  Serial.print (LSB); 
  Serial.print("  ");
   Serial.print(counterd);
  Serial.print("  ");
  Serial.print(MSB_counter);
  Serial.print("  ");
  Serial.println (LSB_counter); */
  
  detachInterrupt(0);  
  prepareForInterrupts ();    
}  // end of isr

// timer overflows (every 65536 counts)
ISR (TIMER1_OVF_vect) 
{
  overflowCount++;
}  // end of TIMER1_OVF_vect


void prepareForInterrupts ()
  {
  // get ready for next time
  EIFR = bit (INTF0);  // clear flag for interrupt 0
  first = true;
  //triggered = false;  // re-arm for next time
  attachInterrupt(0, isr, RISING);     
  }  // end of prepareForInterrupts
  

void setup () 
  {
  Serial.begin(9600);       
  Wire.begin(0x06);
  Wire.onRequest(send);
  
  // reset Timer 1
  TCCR1A = 0;
  TCCR1B = 0;
  // Timer 1 - interrupt on overflow
  TIMSK1 = bit (TOIE1);   // enable Timer1 Interrupt
  // zero it
  TCNT1 = 0;  
  overflowCount = 0;  
  // start Timer 1
  TCCR1B =  bit (CS10);  //  no prescaling

  // set up for interrupts
  //attachInterrupt(0 , isr , RISING);
  prepareForInterrupts ();   
  
  } // end of setup

void loop () 
  {
    
     
}  
