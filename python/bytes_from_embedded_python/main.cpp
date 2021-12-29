#include <iomanip>
#include <iostream>

#include "Python.h"

int
main(int argc, char** argv)
{
	int err;
	Py_buffer buf;

	if (argc < 2)
	{
		std::cout << "usage: " << argv[0] << " \"quoted python expression\"\n";
		return 1;
	}

	// initialize Python
	Py_SetProgramName(L"TestProgram");  /* optional but recommended */
	Py_Initialize();

	// Get the globals/locals for __main__, creating it if it doesn't exist
	PyObject *m, *d, *v;
	m = PyImport_AddModule("__main__");
	if (m == NULL)
	{
		goto error;
	}
	d = PyModule_GetDict(m);

	// Evaluate the given expression (roughly equivalent to eval())
	v = PyRun_String(argv[1], Py_eval_input, d, d);
	if (v == NULL) {
		PyErr_Print();
		goto error;
	}

	// retrieve the associated buffer
	err = PyObject_GetBuffer(v, &buf, 0);
	if (err != 0)
	{
		std::cout << "Bad buffer! (error " << err << ")\n";
		goto error;
	}

	// output the buffer elements
	std::cout << "Buffer at " << buf.buf << "\n";
	for (int i=0; i<buf.len; i++)
	{
		std::cout << "#" << i << "\t" << ((std::uint8_t*)buf.buf)[i] << "\n";
	}

	// buffer views hold a reference to the object that created them, release it
	PyBuffer_Release(&buf);
	// don't forget the reference we own from calling PyRun_String() !
	Py_DECREF(v);
	return 0;

error:
	return -1;
}
