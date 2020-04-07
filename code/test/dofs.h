#include <Servo.h>


#define MOVE 1

typedef struct dof{
  int pin;
  Servo servo;
  int initPos;
  int limits[2];
  int angle;
  int currentDirection = 1;
  bool enable = false;
} dof;

void enableDof(dof* d){
  if (MOVE){
    d->enable = 1;
    d->servo.attach(d->pin);
    d->servo.write(d->angle);
  }
}

void disableDof(dof* d){
  d->enable = 0;
}

void initDof(dof* d, int pin, int initPos, int limit_1, int limit_2){
  
  d->pin = pin;
  
  if (initPos >= limit_1 && initPos <= limit_2)
    d->initPos = initPos;
  else
    d->initPos = limit_1;
    
  d->angle = initPos;
  
  d->limits[0] = limit_1;
  d->limits[1] = limit_2;  
}

void moveDof(dof*d, float newAngleRad){

  float newAngleDeg = newAngleRad*180/PI;
  
  if (MOVE){
    if (newAngleDeg < d->limits[0] || newAngleDeg > d->limits[1]){
      if (newAngleDeg < d->limits[0])
	newAngleDeg = d->limits[0];
      else
	newAngleDeg = d->limits[1];
    }

    d->angle = newAngleDeg;
    if (d->enable)
      d->servo.write(d->angle);
  }

}

// scan between limits
void testDof(dof* d){
  if (d->angle+d->currentDirection >= d->limits[0] && d->angle+d->currentDirection <= d->limits[1])
    moveDof(d, d->angle+d->currentDirection);
  else
    d->currentDirection = - d->currentDirection;
}

