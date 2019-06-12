#include "python.h"
#include <stdio.h>
#include <string.h>

static PyObject *

spam_strlen(PyObject *self, PyObject *args)
{
	char* str = NULL;
	char* str2 = NULL;
	char* str3 = NULL;

	if (!PyArg_ParseTuple(args,"ss", &str, &str2)) // �Ű����� ���� �м��ϰ� ���������� �Ҵ� ��ŵ�ϴ�.
		return NULL;

	strcat(str, str2);

	return Py_BuildValue("s", str);
}



static PyMethodDef SpamMethods[] = {
	{ "strlen", spam_strlen, METH_VARARGS,
	"count a string length." },
	{ NULL, NULL, 0, NULL } // �迭�� ���� ��Ÿ���ϴ�.
};


static struct PyModuleDef spammodule = {
	PyModuleDef_HEAD_INIT,
	"spam",            // ��� �̸�
	"It is test module.", // ��� ������ ���� �κ�, ����� __doc__�� ����˴ϴ�.
	-1,SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
	return PyModule_Create(&spammodule);
}