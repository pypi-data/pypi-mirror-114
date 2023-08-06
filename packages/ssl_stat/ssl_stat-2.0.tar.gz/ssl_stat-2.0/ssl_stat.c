#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <curl/curl.h>
#include <string.h>

char *get_second_part(char *str) {
    char * token = strtok(str, ":");
    token = strtok(NULL, ":");
    return token;
}

char *get_datetime(char *str) {
    char * retstr = (char *) malloc(30);
    char * token = strtok(str, ":");
    strcpy(retstr, "");
    int ignore_first = 1;
    while( token != NULL ) {
        if (ignore_first) {
            ignore_first = 0;
            token = strtok(NULL, " ");
            continue;
        }
        strcat(retstr, token);
        strcat(retstr, " ");
        token = strtok(NULL, " ");
    }
    return retstr;
}

static size_t wrfu(void *ptr,  size_t  size,  size_t  nmemb,  void *stream) {
    (void)stream;
    (void)ptr;
    return size * nmemb;
}

static PyObject *PySSLStatError;

static PyObject *
ssl_stat_check(PyObject *self, PyObject *args) {
    char *url_to_check;;

    if (!PyArg_ParseTuple(args, "s", &url_to_check)) {
        PyErr_SetString(PySSLStatError, "expected 1 arguments, got 0");
        return NULL;
    }

    CURL *curl;
    CURLcode res;

    curl_global_init(CURL_GLOBAL_DEFAULT);

    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url_to_check);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, wrfu);
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
        curl_easy_setopt(curl, CURLOPT_VERBOSE, 0L);
        curl_easy_setopt(curl, CURLOPT_CERTINFO, 1L);

        res = curl_easy_perform(curl);

        if(!res) {
            struct curl_certinfo *certinfo;
            int need_break = 0;
            char *serial_number, *expire_date, *start_date;

            res = curl_easy_getinfo(curl, CURLINFO_CERTINFO, &certinfo);

            if(!res && certinfo) {
                int i;

                for(i = 0; i < certinfo->num_of_certs; i++) {
                    struct curl_slist *slist;

                    for(slist = certinfo->certinfo[i]; slist; slist = slist->next) {
                        if (strstr(slist->data, "Serial Number:") != NULL) {
                            serial_number = get_second_part(slist->data);
                        }

                        if(strstr(slist->data, "Start date:") != NULL) {
                            start_date = get_datetime(slist->data);
                        } 

                        if(strstr(slist->data, "Expire date:") != NULL) {
                            expire_date = get_datetime(slist->data);
                        } 
                        if(strstr(slist->data, "Subject Alternative Name") != NULL) {
                            need_break = 1;
                        }
                    }

                    if (need_break) {
                        curl_easy_cleanup(curl);
                        curl_global_cleanup();
                        return Py_BuildValue("{s:s,s:s,s:s}", "serial_number", serial_number, "start_date", start_date, "expire_date", expire_date);
                    }

                }
            }

        }

        curl_easy_cleanup(curl);
    }

    curl_global_cleanup();

    return Py_BuildValue("{}");
}

static PyMethodDef PySSLStatMethods[] = {
    {"check",  ssl_stat_check, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef ssl_stat = {
    PyModuleDef_HEAD_INIT,
    "ssl_stat",
    NULL,
    -1,
    PySSLStatMethods
};

PyMODINIT_FUNC
PyInit_ssl_stat(void){
    PyObject *m;
    m = PyModule_Create(&ssl_stat);
    if (m == NULL)
        return NULL;

    PySSLStatError = PyErr_NewException("ssl_stat.Error", NULL, NULL);
    Py_XINCREF(PySSLStatError);

    if (PyModule_AddObject(m, "Error", PySSLStatError) < 0) {
        Py_XDECREF(PySSLStatError);
        Py_CLEAR(PySSLStatError);
        Py_DECREF(m);
        return NULL;
    }

    return m;

}