
struct MCintegrate {
	Int ndim,nfun,n; //number of dimensions, functions and points sampled
	VecDoub ff,fferr; //Answers: the integrals and their standard errors
	VecDoub xlo,xhi,x,xx,fn,sf,sferr; //xlo - lower limits of the coordinates of the box to be sampled , sf is a sum function, sferr is the error function of our f
	Doub vol;

	VecDoub (*funcsp)(const VecDoub &); //The declaration of the pointer to the function that takes the reference of type const Vecdoub and returnds VecDoub
	VecDoub (*xmapp)(const VecDoub &); 
	Bool (*inregionp)(const VecDoub &);
	Ran ran; 

	MCintegrate(const VecDoub &xlow, const VecDoub &xhigh, //Member function with the same name as its class guarantees initialization upon construction ()
	VecDoub funcs(const VecDoub &), Bool inregion(const VecDoub &), //declaration of the reference to the &xhigh
	VecDoub xmap(const VecDoub &), Int ranseed);

	void step(Int nstep);

	void calcanswers(); //Void return type, the function does not return a value
};
MCintegrate::MCintegrate(const VecDoub &xlow, const VecDoub &xhigh,
	VecDoub funcs(const VecDoub &), Bool inregion(const VecDoub &),
	VecDoub xmap(const VecDoub &), Int ranseed)
	: ndim(xlow.size()), n(0), xlo(xlow), xhi(xhigh), x(ndim), xx(ndim), //initializer list is used to directly initialize the data members of a class
	funcsp(funcs), xmapp(xmap), inregionp(inregion), vol(1.), ran(ranseed) {
	if (xmapp) {
		nfun = funcs(xmapp(xlo)).size();
	} //if xmapp is NULL (the null pointer) is implicitly converted into boolean false while non-null pointers are converted into true
	else {
		nfun = funcs(xlo).size();
		ff.resize(nfun);
		fferr.resize(nfun);
		fn.resize(nfun);
		sf.assign(nfun,0.);
		sferr.assign(nfun,0.);
	}
	for (Int j=0;j<ndim;j++) { //gives a volume of the rectangular box 
		vol *= abs(xhi[j]-xlo[j]);
	}
}

void MCintegrate::step(Int nstep) { //Sample an additional nstep points, accumulating the various sums
	Int i,j;
	for (i=0;i<nstep;i++) { //for one point at a time
		for (j=0;j<ndim;j++) //for one dimension at a time
			x[j] = xlo[j]+(xhi[j]-xlo[j])*ran.doub(); //we are interested in the points between our boundaries for this dimension
		if (xmapp) xx = (*xmapp)(x);
		else xx = x; //we got our point
		if ((*inregionp)(xx)) { //want to check if this point is inside the region
			fn = (*funcsp)(xx);
			for (j=0;j<nfun;j++) {
				sf[j] += fn[j];
				sferr[j] += SQR(fn[j]);
			}
		}
	}
	n += nstep;
}

void MCintegrate::calcanswers(){ //Member function updates the vectors ff and ffer which contains respectively the estimated MC integrals of the functions and the rrors of these estimates
	for (Int j=0;j<nfun;j++) {
		ff[j] = vol*sf[j]/n;
		fferr[j] = vol*sqrt((sferr[j]/n-SQR(sf[j]/n))/n);
	}
}

//To use the MCintegrate object we first write functions that describe the integrans nd the region of integration W iside the box V
VecDoub torusfuncs(const VecDoub &x) { //pass the value by reference (changes made to the parameter affect the passed argument). Instead of actual values, the reference of the var is passed to function parameters
	Doub den = 1.; 						//Local parameters are reference to the storage locations of the argument passed in and thus can be altered inside!
	VecDoub f(4); //number of integrals
	f[0] = den; 
	for (Int i=1;i<4;i++) f[i] = x[i-1]*den;
	return f;
}
//Returns the inequality 
Bool torusregion(const VecDoub &x) {
	return SQR(x[2])+SQR(sqrt(SQR(x[0])+SQR(x[1]))-3.) <= 1.;
}
VecDoub torusmap(const VecDoub &s) {
	VecDoub xx(s);
	xx[2] = 0.2*log(5.*s[2]);
	return xx;
}