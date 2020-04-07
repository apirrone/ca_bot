#import <math.h>

void ik(float x, float y, float z, float L1, float L2, float L3, float *t1, float *t2, float *t3){

  float n = sqrt(z*z + x*x);
  float h = sqrt(n*n - L1*L1);

  float delta2 = acos((-(h*h) + n*n + L1*L1)/(2*n*L1));
  float gamma2 = asin(x/n);
  *t1 = gamma2 + delta2;

  float m = sqrt(y*y + h*h);
  float delta = acos((-(L3*L3) + m*m + L2*L2)/(2*m*L2));
  float gamma = asin(y/m);

  *t2 = gamma + delta;

  *t3 = acos((-(m*m) + L2*L2 + L3*L3)/(2*L2*L3));
}
