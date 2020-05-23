#include <Python.h>

/**
 * print_python_list - prints info about Python list object
 * @p: Pyobject list
 */
void print_python_list(PyObject *p)
{
	PyObject *item;
	Py_ssize_t list_size = PyList_Size(p);
	Py_ssize_t i;

	if (!p)
		return;

	printf("[*] Python list info\n");
	printf("[*] Size of the Python List = %lu\n", list_size);
	printf("[*] Allocated = %lu\n", ((PyListObject *)p)->allocated);

	for (i = 0; i < list_size; i++)
	{
		item = ((PyListObject *)(p))->ob_item[i];
		printf("Element %ld: %s\n", i, item->ob_type->tp_name);
	}
}

/**
 * print_python_bytes - prints info about Python bytes object
 * @p: PyObject list
 */
void print_python_bytes(PyObject *p)
{
	char *py_bytes_str;
	Py_ssize_t py_bytes_size;
	Py_ssize_t i;

	printf("[.] bytes object info\n");
	if (!PyBytes_Check(p))
	{
		printf("  [ERROR] Invalid Bytes Object\n");
		return;
	}
	py_bytes_size = (((PyVarObject *)(p))->ob_size);
	py_bytes_str = (((PyBytesObject *)(p))->ob_sval);

	printf("  size: %ld\n", py_bytes_size);
	printf("  trying string: %s\n", py_bytes_str);
	py_bytes_size = py_bytes_size > 9 ? 10 : py_bytes_size;
	printf("  first %ld bytes: \n", py_bytes_size);

	for (i = 0; i < py_bytes_size; i++)
		printf("%02hhx%c", py_bytes_str[i], i < py_bytes_size ? ' ' : '\n');
}
