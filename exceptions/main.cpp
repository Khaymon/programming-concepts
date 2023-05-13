#include <any>

#include <iostream>
#include <setjmp.h>
#include <stack>
#include <string>
#include <cassert>

class Object;

std::stack<Object*> objectsStack;

class Object {
public:
	Object() {
        objectsStack.push(this);
    }

	virtual ~Object() {
        assert(!objectsStack.empty() && this == objectsStack.top());
        objectsStack.pop();
        std::cout << "Destruct Object" << std::endl;
    }
};

int currentObjectsStackSize;
bool isClearingStack = false;

std::any currentException;
std::stack<jmp_buf*> environmentsStack;


#define TRY \
{\
    jmp_buf env; \
    int isException = setjmp(env); \
    bool isEnvInStack = true; \
    currentObjectsStackSize = objectsStack.size();\
    if(!isException) { \
        environmentsStack.push(&env); \

#define THROW(e) \
    if (isClearingStack) \
        std::terminate(); \
    currentException = e; \
    isClearingStack = true; \
    while(objectsStack.size() != currentObjectsStackSize) { \
        Object *currentObject = objectsStack.top(); \
        currentObject->~Object(); \
    } \
    isClearingStack = false; \
    if (!environmentsStack.empty()) \
        longjmp(*environmentsStack.top(), 1); \
    else \
        std::terminate();

#define CATCH(userExceptionType, userExceptionValue) \
    } else \
        if (userExceptionType *p = std::any_cast<userExceptionType>(&currentException)) {\
            userExceptionType userExceptionValue = *p; \
            environmentsStack.pop(); \
            isEnvInStack = false;

#define FINALIZE \
    } else { \
        if (isEnvInStack) {\
            environmentsStack.pop(); \
            isEnvInStack = false; \
        } \
        THROW(currentException); \
    } \
}


class Doggo : public Object {
public:
	Doggo() {
		std::cout << "Doggo woof" << std::endl;
	}
	~Doggo() {
		std::cout << "Doggo woofn't" << std::endl;
	}
	void big_question() {
		std::cout << "42" << std::endl;
		THROW(42)
	}
	void small_question() {
		std::cout << "Ça va" << std::endl;
		big_question();
	}
};

class Bober : public Object {
public:
	Bober() {
		std::cout << "Bober is" << std::endl;
	}
	~Bober() {
		std::cout << "Bober isn't" << std::endl;
	}

	void greeting() {
		std::cout << "Bober hi" << std::endl;
		Doggo doggo;
		doggo.small_question();
	}

	void farewell() {
		std::cout << "Bober bye" << std::endl;
		greeting();
	}
};

class Catto : public Object {
public:
	Catto() {
		std::cout << "Catto meow" << std::endl;
	}
	Catto(const Catto& _c) {
		std::cout << "Catto purr" << std::endl;
	}
	~Catto() {
		std::cout << "Catto meown't" << std::endl;
	}
	void bark() {
		std::cout << "woof" << std::endl;
		THROW("woof");
	}
};

class Hampter : public Object {
public:
	Hampter() {
		std::cout << "Hampter in" << std::endl;
	}
	~Hampter() {
		std::cout << "Hampter out" << std::endl;
		THROW(2.5)
	}
	void crunch(Catto cotto) {
		std::cout << "Humpter crunch-crunch" << std::endl;
		cotto.bark();
	}
};

int main() {
    std::cout << "\n##################### TEST 1 #####################\n\n";
	TRY {
		std::cout << "There is no exception" << std::endl;
		TRY{
			std::cout << "New try, here throws exception" << std::endl;
			THROW(5.2f)
		}
		CATCH(char, e) {
			std::cout << "Here is char!" << std::endl;
		}
		FINALIZE
	}
	CATCH(int, e) {
		std::cout << "Here is int!" << std::endl;
	}
	CATCH(float, e) {
		std::cout << "Here is float!" << std::endl;
	}
	FINALIZE

	std::cout << "\n##################### TEST 2 #####################\n\n";

	TRY {
		Bober bober;
		bober.farewell();
	}
	CATCH(int, e) {
		std::cout << "CATCH it!" << std::endl;
	}
	FINALIZE

    std::cout << "\n##################### TEST 3 #####################\n\n";

	TRY {
		Hampter hampter;
		Catto catto;
		hampter.crunch(Catto(catto));
	}
	CATCH(char, e) {
		std::cout << "CATCH again!" << std::endl;
	}
	FINALIZE
    
	return 0;
}