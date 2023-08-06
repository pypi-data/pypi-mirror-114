#define _GNU_SOURCE
#include <stdlib.h>
#include <errno.h>
#include <sys/uio.h>
#define PY_SSIZE_T_CLEAN
#include <Python.h>

/*
process_vm_readv
*/
PyObject * method_process_vm_readv(PyObject *self, PyObject *args) {
	int pid;
	void* addr;
    char *buf;
	size_t BUFSIZE;
    ssize_t nread;
	struct iovec local[1];
    struct iovec remote[1];
	PyObject *result;

	if(!PyArg_ParseTuple(args, "inn", &pid,&addr,&BUFSIZE)) {
	    return NULL;
	}

	buf = (char *) PyMem_Malloc(BUFSIZE); /* for I/O */

	if (buf == NULL){
		return PyErr_NoMemory();
	}

    local[0].iov_base = buf;
    local[0].iov_len = BUFSIZE;
    remote[0].iov_base = addr;
    remote[0].iov_len = BUFSIZE;

    nread = process_vm_readv(pid, local, 1, remote, 1, 0);

    if (nread == -1) {
    	PyMem_Free(buf);
        return PyErr_SetFromErrno(PyExc_IOError);
    }

	result = Py_BuildValue("y#", buf, BUFSIZE);//PyBytes_FromStringAndSize(buf, buf_size);
	PyMem_Free(buf); /* allocated with PyMem_Malloc */
	return result;
}

/*
process_vm_writev
*/
PyObject * method_process_vm_writev(PyObject *self, PyObject *args) {
	int pid;
	void* addr;
    Py_buffer bytes;
    ssize_t nread;
	struct iovec local[1];
    struct iovec remote[1];
	//PyObject *result;

	if(!PyArg_ParseTuple(args, "iny*", &pid,&addr,&bytes)) {
	    return NULL;
	}
	
    local[0].iov_base = bytes.buf;
    local[0].iov_len = bytes.len;
    remote[0].iov_base = addr;
    remote[0].iov_len = bytes.len;

    nread = process_vm_writev(pid, local, 1, remote, 1, 0);

    if (nread == -1) {
        return PyErr_SetFromErrno(PyExc_IOError);
    }

	return Py_BuildValue("l", nread);
}

/*
DOCS
*/
char method_process_vm_readvfunc_docs[] = "process_vm_readv\n";
char method_process_vm_writevfunc_docs[] = "process_vm_readv\n";

PyMethodDef rwpm_funcs[] = {
	{	"process_vm_readv",
		(PyCFunction)method_process_vm_readv,
		METH_VARARGS,
		PyDoc_STR(method_process_vm_readvfunc_docs)},
	{	"process_vm_writev",
		(PyCFunction)method_process_vm_writev,
		METH_VARARGS,
		PyDoc_STR(method_process_vm_writevfunc_docs)},
	{	NULL}
};

char rwpmmod_docs[] = "Extension provides wrapper functions to Linux system calls: process_vm_readv & process_vm_writev.\n";

PyModuleDef rwpm_mod = {
	PyModuleDef_HEAD_INIT,
	"rwpm",
	PyDoc_STR(rwpmmod_docs),
	-1,
	rwpm_funcs,
	NULL,
	NULL,
	NULL,
	NULL
};

PyMODINIT_FUNC PyInit_rwpm(void) {
	return PyModule_Create(&rwpm_mod);
}