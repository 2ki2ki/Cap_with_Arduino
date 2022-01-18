
const int stim01 = 8;
const int stim02 = 9;
const int stim03= 10;
const int stim04 = 11;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(stim01, OUTPUT);
  pinMode(stim02, OUTPUT);
  pinMode(stim03, OUTPUT);
  pinMode(stim04, OUTPUT);
}


void loop() {
  // put your main code here, to run repeatedly:

  delay(1000);
  digitalWrite(stim01,HIGH);
  delay(1000);
  digitalWrite(stim01,LOW);
   delay(1000);
  digitalWrite(stim02,HIGH);
  delay(1000);
  digitalWrite(stim02,LOW);
  delay(1000);
  digitalWrite(stim03,HIGH);
  delay(1000);
  digitalWrite(stim03,LOW);  
  delay(1000);
  digitalWrite(stim04,HIGH);
  delay(1000);
  digitalWrite(stim04,LOW);
  
  

}
