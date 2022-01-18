
const int stim01 = 8;
const int stim02 = 9;
const int stim03= 10;
const int stim04 = 11;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(stim01, INPUT);
  pinMode(stim02, INPUT);
  pinMode(stim03, INPUT);
  pinMode(stim04, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int stim_num = 0;
  if (digitalRead(stim01) == HIGH){
    stim_num = 1;
  }else if (digitalRead(stim02) ==HIGH){
    stim_num = 2;
  }else if (digitalRead(stim03) == HIGH){
      stim_num = 3;
  }else if (digitalRead(stim04) == HIGH){
    stim_num = 4;
  }else{
    stim_num = 0;
  }

  Serial.println(stim_num);
  delay(1);
}
