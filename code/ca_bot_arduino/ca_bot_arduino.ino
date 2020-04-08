#include "dofs.h"
#include "kinematics.h"

dof front_left_shoulder;
dof front_left_thigh;
dof front_left_leg;

dof front_right_shoulder;
dof front_right_thigh;
dof front_right_leg;

dof back_left_shoulder;
dof back_left_thigh;
dof back_left_leg;

dof back_right_shoulder;
dof back_right_thigh;
dof back_right_leg;

float L1 = 27;
float L2 = 77;
float L3 = 80.3;

float initX = L1;
float initY = L2;
float initZ = L3;

Servo tmp;
float x = 0;
float y = 0;
/* float z = 0; */
/* float y = -70; //-150 */
/* float z = 20; //30 */
float z = 30; //30


int directionX = -1;
int directionZ = -1;
int directionY = -1;

float t1, t2, t3;
float t12, t22, t32;
void setup() {
  Serial.begin(9600);
  initDof(&front_left_shoulder, 2, 90, 0, 180);
  initDof(&front_left_thigh, 3, 90, 0, 180);
  initDof(&front_left_leg, 4, 90, 60, 140);
  
  initDof(&front_right_shoulder, 5, 90, 0, 180);
  initDof(&front_right_thigh, 6, 90, 0, 180);
  initDof(&front_right_leg, 7, 90, 60, 140);
  
  initDof(&back_right_shoulder, 8, 90, 0, 180);
  initDof(&back_right_thigh, 9, 90, 0, 180);
  initDof(&back_right_leg, 10, 90, 60, 140);
  
  initDof(&back_left_shoulder, 11, 90, 0, 180);
  initDof(&back_left_thigh, 12, 90, 0, 180);
  initDof(&back_left_leg, 13, 90, 60, 140);
  
  /* enableDof(&front_left_shoulder); */
  /* enableDof(&front_left_thigh); */
  /* enableDof(&front_left_leg); */
  
  /* enableDof(&front_right_shoulder); */
  /* enableDof(&front_right_thigh); */
  /* enableDof(&front_right_leg); */
  
  /* enableDof(&back_right_shoulder); */
  /* enableDof(&back_right_thigh); */
  /* enableDof(&back_right_leg); */
  
  /* enableDof(&back_left_shoulder); */
  /* enableDof(&back_left_thigh); */
  /* enableDof(&back_left_leg); */

  /* tmp.attach(5); */
  /* tmp.write(90); */
  
  /* delay(1000); */
  /* tmp.detach(); */
}

void loop() 
{

  x += 0.3*directionX;
  if (x < -30 || x > 30){
    directionX = - directionX;
  }

  /* y += 0.2*directionY; */
  /* if (y < -30 || y >= 0){ */
  /*   directionY = - directionY; */
  /* } */
  
  /* z += 0.2*directionZ; */
  /* if (z > 30 || z <= 0){ */
  /*   directionZ = - directionZ; */
  /* } */

  
    
  
  ik(initX + x, initY + y, initZ + z, L1, L2, L3, &t1, &t2, &t3);
  ik(x - initX, y + initY, z + initZ, -L1, L2, L3, &t12, &t22, &t32);
  moveDof(&front_left_shoulder, t1);
  moveDof(&front_left_thigh, t2+(PI/2)-0.01);
  moveDof(&front_left_leg, (PI-t3+0.01));

  /* Serial.println((t12)*180/PI); */
  moveDof(&front_right_shoulder, t12+0.28); // validé
  moveDof(&front_right_thigh, (PI-t22)-(PI/2 - 0.28)-0.01);//validé
  moveDof(&front_right_leg, t32); // validé

  moveDof(&back_left_shoulder, (PI-t1)+0.1);
  moveDof(&back_left_thigh, t2+(PI/2)-0.01);
  moveDof(&back_left_leg, (PI-t3+0.01));
  
  moveDof(&back_right_shoulder, (PI-t12)-0.1);
  moveDof(&back_right_thigh, (PI-t22)-(PI/2 - 0.28));
  moveDof(&back_right_leg, t32);

  
  
  /* testDof(&front_left_shoulder); */
  /* testDof(&front_left_thigh); */
  /* testDof(&front_left_leg); */
  delay(1);
}
