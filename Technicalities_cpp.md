# Technicalities

Page 257.

A **declaration** defines how something can be used; it defines the interface of a function, variable or a class.

A **declaration** that (also) fully specifies the entity declared is called a **definition**.

A **header file** contains definitions of terms, such as cout, that we use in our program.

The declaration/definition distinction reflects the fundamental distinction between what we need to use something (an interface) and what we need for that something to do what it is supposed to (an implementation). For a variable, a declaration supplies the type but only the definition supplies the object (the memory). For a function, a declaration again provides the type (argument types plus return type) but only the definition supplies the function body (the executable statements). 

"Forward declaration": when we declare the function before defining it

**Default Initialization**: for strings and vectors, we don't need to necessarily initiliaze, it creats empty arrays and strings. However, we can not do the same thing for built-in types.

The key to managing declarations of facilities defined 'elsewhere' in C++ is the header. Basically, a header is a collection of declarations, typically defined in a file, so a header is also called a **header file**. Such headers are then included in our source files. 

## Scopes

1. The *global scope*: the area of text outside any other scope
2. A *namespace scope*: a named scope nested in the global scope or in another namespace
3. A *class scope*: the area of text within a class
4. A *local scope*: between {} braces of a block or in a **function argument list**
5. A *statement scope*: e.g. in a **for**-statement

## Classes

1. **Functions within class**: member functions 

```c++
class C {
  public: 
  		void f();
  		void g() //a member function can be defined within its class
      {
        ///.
      }
};

void C::f() //a member function definition can be outside its class
{
  //...
}
```



2. **Classes within classes**: member classes

   ```c++
   class C{
     public: 
     		struct M{
           //...
         };
     		//...
   };
   ```

   

*3. **Classes within functions**: local classes

```c++
void f()
{
			class L {
						//...
			};
};
```



4. **Functions within functions**: local functions (also called nested functions) - THIS IS NOT LEGAL IN C++
5. **Blocks with functions and other blocks**: nested blocks



### Class Interfaces

**Use :: after a class name (or a namespace name) and . (dot) after an object name

How do we design a good interface? 

- Keep interfaces complete
- Keep interfaces minimal
- Provide constructors
- Support copying (or prohibit it)
- Use types to provide good arguments checking 
- Identify nonmodifying member functions
- Free all resources in the destructor



## Declaring arguments and return type

A function declaration consists of a return type followed by the name of the function followed by a list fo formal arguments in parentheses. 

```c++
double fct(int a, double d); //declaration of fct ( no body)
double fct(int a, double d) { return a•d; } //definition of fct
```

If you don't want to return a value from a function, give **void** as its return type. 

## Passing by 

1. **Pass-by-value**: to give the function a copy of the value you use as the argument. 

2. **Pass-by-const-reference**. There has to be a way for us to pass a variable to a function without copying it. We need a way of giving out **print()** function "the address" of the **vector** to **print()** rather than a copy of the vector. The **&** means "reference" and the **const** is there to stop **print()** modifying its argument by accicent. It's like before but the only difference is that instead of operating on a copy, **print()** now refers back to the argument through the reference. 

   ```c++
   void print(const vector<double>& v)
   ```

3. **Pass-by-reference**: What if we did want a function to modify its arguments? Sometimes, that's a perfectly reasonable thing to wish for. For example, we might want an **init()** function that assigned values to vector to vector elements: 

   ```c++
   void init(vector<double>& v) //pass-by-reference
   {
     for(int i=0; i<v.size(); ++i) v[i]=i;
   }
   
   void g(int x)
   {
     vector<double> vd1(10); //small vector
     vector<double> vd2(1000000); //large vector
     vector<double> vd3(x); //vector of some unknown size
     
     init(vd1); //here we wanted init() to mdify the argument vector, so we did not copy
     init(vd2);
     init(vd3);
   }
   ```

   Let us consider references from a more technical point of view. A reference is a construct that allows a user to declare a new name for an object. For example, **int&** is a reference to an **int**, so we can write 

   ```c++
   int i = 7;
   int& r = i; //r is a reference to i
   r = 9; //i becomes 9
   i = 10;
   cout << r << '' << i << '\n'; //write 10 10 
   ```

## Function call implementation

The language implementation sets aside a data structure containing a copy of all its paraeters and local variables. The "implementation stuff" varies from implementation to implementation, but it's basically the information that the function needs to return to its caller and to return a value to its caller. Such a data structure is called a *function activation record*, and each function has its own detailed layout of its activation record. The stack, also called the *call stack*, is a data structure that grows and shrinks at one end according to the rule: first in, first out (probably LIFO).



### Namespaces

What we lack so far is something to organize classes, functions, data and types into an identifiable and named part of a program without defining a type. The language mechanism for such grouping of declaraions is a *namespace*. 

**A fully qualified name** is a name composed of a namespace name or a class name) and a memeber name combined by ::. Sometimes it's pretty tedious, so we would like to use short-hand notation: 

```c++
//instead of 
#include<string> 
#include<iostream>

//we can use 
using std::string; //string means std::string
using std::cout; //cout means std::cout

//even stronger "shorthand" for the use of names from a namespace
using namespace std;
#include"std_lib_facilities.h"
```



## Technicalities of classes

The parts used to define the class are called *members*. 

```c++
class X {
  public: 
  		int m; //data member
  		int mf(int v) {int old = m; m=v; return old; } //function member
}

//We access members using the object.member notation

X var; //var is a variable of type X
var.m = 7; //assign to var's data member m
int x = var.mf(9); //call var's member function mf()

```

### Interface and implementation 

Usually, we think of a class as having an interface plus an implementation. The **interface** is the part of the class's declaration that its users access directly. The implementation is that part of the class's declaration that its users access only indirectly through the interface. 

```c++
class X { //this class's name is X
	public: 
  			//public members:
  			// - the interface to users (accessible by all)
  			//functions
  			//types
  			//data (often best kept private)
  private: 
  			//private members:
  			//  the implementation details (used by embers of this class only
  			// functions
  			//types
  			//data
};
```

Class membders are **private by default**. A user cannot directly refer to a private member. Instead, we have to go through a public function that can use it. 

```c++
class X {
  		int m;
  		int mf(int);
  public:
  		int f(int i) { m=i; return mf(i); }
};

X x; 
int y = x.f(2);
```



### Member functions

**Member functions** guarantee initialization with constructor - when a member function with the same name as its class. It is called a **constructor** and will be used for initiliazation("construction") of objects of the class.

----

In order to mitigate the threat of editing the data, it can be included in the private except through the public member functions that we supply. 

```c++
//simple Date (control access)
class Date{
  	int y,m,d;
public: 
  	Date(int y, int m, int d);
  	void add_day(int n);
  	int month() {return m;}
  	int day() {return d;}
  	int year() {return y;}
};


Date birthday(1970,12,30);
birthday.m = 14; //error date::m is private
cout << birthday.month() << endl;
```

We try to design our types so that values are guaranteed to be valid; that is, we hide the representarion, provide a constructor that creates only valid objects, and design all member functions to expect valid values and leave only valid values behind when they return. The value of an object is often called its **state**, so the idea of a valid value is often referred to as a *valid state* of an object. A rule for what constitutes a valid value is called an *invariant*. 

Data members can be initialized by using an initializer list in the constructor (a base and member initializer list). Members will be initialized in the order in which they are declared in the class. The **:y(yy), m(mm), d(dd)** notation is how we initialize members. 

```c++
Date::Date(int yy, int mm, int dd)
  :y(yy), m(mm), d(dd)
  {
    
  }
```

Writing the definition of a member function within the class definition has two effects:

+ The function will be *inlined*; that is, the compiled will tryu to generate code for a call to the inline function without using a function call to get to that code.This can be a significant performance afvantage for functions.
+ All uses of the class will have to be recompiled whenever we make a change to the body of an inlined function. If the function body is out of the class declaration, recompilation of users is needed only when the class declaration. is itself changed. Not recompiling when the body is changed can be a huge advantage in large programs. 

**Enumerations**: *enum* is a very simple user-defined type, specifying its set of values (its enumerators) as symbloic constants. 

```c++
enum Month {
  jan=1, fed, mar, apr, may,jun, jul, aug, sep, oct, nov, dec
};
```



### Operator Overloading 

You can define almost all C++ operators for class or enumeration operands. That's often called operator overloading. We use it when we want to provide cnventional notation for a type we design. 

```c++
enum Month {
  Jan=1,FebMar,Apr,May, Jun,Jul, Aug,Sep, Oct, Nov, Dec
};

Month operator++(Month& m) //prefix increment operator
{
  m = (m==Dec) ? Jan : Month(m+1); //'wrap around'
  return m;
}

//Now can be used like this 
Month m = sep;
++m; //m becomes Oct
```

Use :: after a class name(or a namespace name) and .(dot) after an object name.

### Pointers and references

Clock/Spiral Rule - https://stackoverflow.com/questions/1143262/what-is-the-difference-between-const-int-const-int-const-and-int-const

You can think of a reference as an automatically dereferences immutable pointer or as an alternative name for an object. Pointers and references differ in these ways:

+ Assignment to a pointer changes the pointer's value (not the pointer-to value)
+ To get a pointer you generally need to use **new** or **&**
+ To access an object pointer to by a pointer yu use ***** or **[]**
+ Assignment to a reference changed what reference refers to (not the reference itself)
+ You cannot make a reference refer to a different object after initialization
+ Assignment of references does deep copy (assigns to the referred-to object); assignment of pointers does not (assigns to the pointer object itself)
+ Beware of null pointers

**Facts**: 

**Null pointers** are implicitly converted into boolean false while non-null pointers are converted into true.



### Different use of address-of operator (&) in contest of expressions and declarations

The meaning of symbol `&` is different in an expression and in a declaration. When it is used in an expression, `&` denotes the address-of operator, which returns the address of a variable, e.g., if `number` is an `int` variable, `&number` returns the address of the variable `number` (this has been described in the above section).

Howeve, when `&` is used in a *declaration* (including *function formal parameters*), it is part of the type identifier and is used to declare a *reference variable* (or *reference* or *alias* or *alternate name*). It is used to provide *another name*, or *another reference*, or *alias* to an existing variable.

9.4.4 - 309