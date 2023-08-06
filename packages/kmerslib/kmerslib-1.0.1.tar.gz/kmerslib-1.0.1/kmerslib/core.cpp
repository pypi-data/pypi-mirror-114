#include "Python.h"
#include "kmerslib.h"

static PyObject* kmerslib_core_makeFFPS(PyObject *self, PyObject *args){
	std::string dir;
    int startk;
    int endk;
    int ndevice;
		if (!PyArg_ParseTuple(args, "siii",&dir,&startk,&endk, &ndevice))return NULL;
		return Py_BuildValue("i", kmerslib::makeFFPS(dir,startk, endk, ndevice) );
	}


static PyMethodDef kmerslib_core_methods[] = {
	{"makeFFPS",(PyCFunction)kmerslib_core_makeFFPS,METH_VARARGS, "Calculate Frequency File Profile"},
	{NULL,}
};


static struct PyModuleDef module_def = {
	PyModuleDef_HEAD_INIT,
	"kmerslib.core",
	"An example project showing how to build a pip-installable Python package that invokes custom CUDA/C++ code.",
	-1,
	kmerslib_core_methods
};

PyMODINIT_FUNC PyInit_core(){
	return PyModule_Create(&module_def);
}