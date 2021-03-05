
#include <iostream>
#include "/Users/user/Desktop/UCL_CS_Masters/cpp_learn/code/include/nr3.h"
#include "/Users/user/Desktop/UCL_CS_Masters/cpp_learn/code/include/ran.h"
#include "/Users/user/Desktop/UCL_CS_Masters/cpp_learn/code/include/mcintegrate.h"


int main() {
    VecDoub xlo(3), xhi(3);
    xlo[0] = 1.; xhi[0] = 4.;
    xlo[1] = -3.; xhi[1] = 4.;
    xlo[2] = -1.; xhi[2] = 1.;
    MCintegrate mymc(xlo,xhi,torusfuncs,torusregion,NULL,10201);
    mymc.step(1000000);
    mymc.calcanswers();
    std::cout << mymc.ff[0]; 
}