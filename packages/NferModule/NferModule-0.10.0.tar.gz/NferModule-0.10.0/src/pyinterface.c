#include <Python.h>
#include <unistd.h>

#include "types.h"
#include "log.h"
#include "pool.h"
#include "file.h"
#include "dsl.h"
#include "strings.h"
#include "dict.h"
#include "nfer.h"
#include "learn.h"

extern timestamp opt_window_size;
extern bool opt_full;

static PyObject *nfer_error;

static dictionary name_dict, key_dict, val_dict;
static nfer_specification spec;
static pool in_pool, out_pool;
static bool initialized = false;

PyDoc_STRVAR(init_method_doc, "Initialize the internal nfer data structures.");
static PyObject * python_init(PyObject *Py_UNUSED(self), PyObject *Py_UNUSED(args)) {
    if (initialized) {
        // clean up the old data first
        destroy_dictionary(&name_dict);
        destroy_dictionary(&key_dict);
        destroy_dictionary(&val_dict);
        destroy_specification(&spec);
        destroy_pool(&in_pool);
        destroy_pool(&out_pool);
    }

    // initialize the global data structures
    initialize_dictionary(&name_dict);
    initialize_dictionary(&key_dict);
    initialize_dictionary(&val_dict);
    initialize_specification(&spec, 0);
    initialize_pool(&in_pool);
    initialize_pool(&out_pool);
    initialized = true;

    Py_RETURN_NONE;
}


PyDoc_STRVAR(load_method_doc, "Load an nfer specification, replacing the current spec.");
static PyObject * python_load_spec(PyObject *Py_UNUSED(self), PyObject *args) {
    const char *filename;
    struct stat buffer;

    if (!PyArg_ParseTuple(args, "s", &filename)) {
        return NULL;
    }
    if (stat(filename, &buffer) != 0) {
        PyErr_SetString(nfer_error, "Spec file does not exist");
        return NULL;
    }

    // call the init_spec function before loading to initialize the globals
    python_init(NULL, args);

    // try to load the spec from the passed file
    if (!load_specification(filename, &spec, &name_dict, &key_dict, &val_dict)) {
        PyErr_SetString(nfer_error, "Error loading nfer specification");
        return NULL;
    }
    Py_RETURN_NONE;
}

PyDoc_STRVAR(scan_method_doc, "Scan an nfer specification and append the rules to the current spec.");
static PyObject * python_scan_spec(PyObject *Py_UNUSED(self), PyObject *args) {
    const char *code;

    if (!PyArg_ParseTuple(args, "s", &code)) {
        return NULL;
    }

    // call the init_spec function before loading to initialize the globals
    // this function is destructive, so only call it if it hasn't been called yet
    if (!initialized) {
    	python_init(NULL, args);
    }

    // try to load the spec from the passed file
    if (!scan_specification(code, &spec, &name_dict, &key_dict, &val_dict)) {
        PyErr_SetString(nfer_error, "Error loading nfer specification");
        return NULL;
    }
    Py_RETURN_NONE;
}

PyDoc_STRVAR(save_method_doc, "Save the current nfer specification.");
static PyObject * python_save_spec(PyObject *Py_UNUSED(self), PyObject *args) {
    const char *filename;
    struct stat buffer;

    if (!PyArg_ParseTuple(args, "s", &filename)) {
        return NULL;
    }
    if (stat(filename, &buffer) == 0) {
        PyErr_SetString(nfer_error, "Spec file already exists");
        return NULL;
    }

    /* todo: this is kind of ugly, since it would break other output to files.
     * One solution would be to add a way to get the current value so it can be restored. */

    // set logging to the file
    set_output_file(filename);
    // write the output
    output_specification(&spec, &name_dict, &key_dict, &val_dict);
    // close the file and return logging to the console
    stop_output();

    Py_RETURN_NONE;
}

static PyObject * map_to_pyobject(data_map *map) {
    map_iterator mit;
    map_key key;
    map_value value;
    PyObject *python_dict, *py_dict_value;

    // get a new dictionary
    python_dict = PyDict_New();

    // iterate over the map
    get_map_iterator(map, &mit);
    while (has_next_map_key(&mit)) {
        key = next_map_key(&mit);
        map_get(map, key, &value);

        switch(value.type) {
        case null_type:
        case pointer_type:
            // shouldn't happen!
            py_dict_value = NULL;
            break;
        case boolean_type:
            if (value.value.boolean) {
                py_dict_value = Py_True;
            } else {
                py_dict_value = Py_False;
            }
            break;
        case integer_type:
            py_dict_value = PyLong_FromUnsignedLongLong(value.value.integer);
            break;
        case real_type:
            py_dict_value = PyFloat_FromDouble(value.value.real);
            break;
        case string_type:
            py_dict_value = PyUnicode_FromString(get_word(&val_dict, value.value.string));
            break;
        }

        if (PyDict_SetItemString(python_dict, get_word(&key_dict, key), py_dict_value) == -1) {
            // an error occurred!
            PyErr_SetString(nfer_error, "Error parsing dictionary value");
            return NULL;
        }
    }

    return python_dict;
}

static PyObject * pool_to_pyobject(pool *p) {
    int index;
    interval *intout;
    pool_iterator pit;
    PyObject *python_list, *python_interval, *python_map;

    // create a new list
    python_list = PyList_New(p->size);
    // instantiate the index count
    index = 0;
    // loop over the contents of the pool
    get_pool_iterator(p, &pit);
    while (has_next_interval(&pit)) {
        intout = next_interval(&pit);
        // create the python object for the map
        python_map = map_to_pyobject(&intout->map);
        // create the python object for the interval
        python_interval = Py_BuildValue("sKKO", get_word(&name_dict, intout->name), intout->start, intout->end, python_map);
        // clean up the map reference
        Py_DECREF(python_map);
        // add it to the list, which steals the reference to the interval
        PyList_SetItem(python_list, index, python_interval);
        index++;
    }
    return python_list;
}

static bool pyobject_to_map(PyObject *py_dict, data_map *map) {
    const char *key_string, *string_value;
    map_key key;
    map_value value;
    label string_label;

    PyObject *py_dict_key, *py_dict_value;
    Py_ssize_t py_dict_pos;
    Py_ssize_t string_size;

    py_dict_pos = 0;
    while (PyDict_Next(py_dict, &py_dict_pos, &py_dict_key, &py_dict_value)) {
        // get the key string
        key_string = PyUnicode_AsUTF8AndSize(py_dict_key, &string_size);
        if (key_string == NULL) {
            // not a string?  just fail silently for now
            continue;
        }
        // get the key
        key = find_word(&key_dict, key_string);
        // if it isn't in the spec, move on
        if (key == WORD_NOT_FOUND) {
            continue;
        }
        // now we need to figure out the type of the value
        // this is tricky because we are going between two loosely typed languages
        // we have to check for bool first, because it also counts as a long!
        if (PyBool_Check(py_dict_value)) {
            value.value.boolean = (py_dict_value == Py_True);
            value.type = boolean_type;
        } else if (PyLong_Check(py_dict_value)) {
            value.value.integer = PyLong_AsUnsignedLongLong(py_dict_value);
            value.type = integer_type;
        } else if (PyFloat_Check(py_dict_value)) {
            value.value.real = PyFloat_AsDouble(py_dict_value);
            value.type = real_type;
        } else if (PyUnicode_Check(py_dict_value)) {
            string_value = PyUnicode_AsUTF8AndSize(py_dict_value, &string_size);
            if (string_value != NULL) {
                string_label = add_word(&val_dict, string_value);
                value.value.string = string_label;
                value.type = string_type;
            }
        } else {
            // A type we don't know how to parse.  Throw an error.
            PyErr_SetString(nfer_error, "Error parsing dictionary value");
            return false;
        }
        // set the map key to the value
        map_set(map, key, &value);
    }
    return true;
}

static interval * pyobject_to_interval(PyObject *py_interval, pool *p, bool filter) {
    const char *name_value;
    const uint64_t start_value;
    const uint64_t end_value;
    PyObject *map_dict;

    interval *intv;
    label name_label;

    if (!PyArg_ParseTuple(py_interval, "sKKO!", &name_value, &start_value, &end_value, &PyDict_Type, &map_dict)) {
        PyErr_SetString(nfer_error, "Couldn't parse interval");
        return NULL;
    }

    // get the label for the interval name
    name_label = find_word(&name_dict, name_value);
    // skip the interval if it doesn't appear in the spec
    if (name_label == WORD_NOT_FOUND) {
        if (filter) {
            // not an error!
            return NULL;
        } else {
            name_label = add_word(&name_dict, name_value);
        }
    }
    // allocate an interval in the input pool
    intv = allocate_interval(&in_pool);

    if (intv != NULL) {
        // populate the interval
        intv->name = name_label;
        intv->start = start_value;
        intv->end = end_value;
        intv->hidden = false;

        // swallow any errors, because we still have the basic data
        // not great, but we need to return the address of the interval anyway
        pyobject_to_map(map_dict, &intv->map);
    }
    return intv;
}

PyDoc_STRVAR(add_method_doc, "Add an interval to the model.");
static PyObject * python_add_interval(PyObject *Py_UNUSED(self), PyObject *args) {
    interval *intv;

    intv = pyobject_to_interval(args, &in_pool, true);

    if (intv != NULL) {
        // make sure the pool is empty
        clear_pool(&out_pool);
        run_nfer(&spec, &in_pool, &out_pool);
        // clear the input pool
        clear_pool(&in_pool);

        if (out_pool.size == 0) {
            // not an error!
            Py_RETURN_NONE;
        }

        return pool_to_pyobject(&out_pool);
    }

    Py_RETURN_NONE;
}



static bool pyobject_to_pool(PyObject *py_list, pool *p) {
    PyObject *py_interval;
    Py_ssize_t list_size, i;
    interval *intv;

    list_size = PyList_Size(py_list);

    for (i = 0; i < list_size; i++) {
        // interval should be a tuple
        py_interval = PyList_GetItem(py_list, i);

        if (py_interval == NULL) {
            PyErr_SetString(nfer_error, "Error getting an interval from the list");
            // if there was an error, return false
            return false;
        }

        intv = pyobject_to_interval(py_interval, p, false);
        if (intv == NULL) {
            // hopefully the error string is already set
            return false;
        }
    }
    // sort it before returning
    sort_pool(p);

    return true;
}

PyDoc_STRVAR(learn_method_doc, "Learn a specification from a list of intervals.");
static PyObject * python_learn_spec(PyObject *Py_UNUSED(self), PyObject *args) {
    PyObject *interval_list;

    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &interval_list)) {
        return NULL;
    }
    if (!initialized) {
        // initialize the global data structures
        initialize_dictionary(&name_dict);
        initialize_dictionary(&key_dict);
        initialize_dictionary(&val_dict);
        initialize_specification(&spec, 0);
        initialize_pool(&in_pool);
        initialize_pool(&out_pool);
        initialized = true;
    }

    if (pyobject_to_pool(interval_list, &in_pool)) {
        // run the learner
        run_learner_on_pool(&in_pool, 1, &name_dict, &key_dict, &val_dict, &spec, DEFAULT_CONFIDENCE, DEFAULT_SUPPORT);
    }
    // clean up
    clear_pool(&in_pool);

    Py_RETURN_NONE;
}

PyDoc_STRVAR(subscribes_method_doc, "Get intervals to which the current spec subscribes.");
static PyObject * python_get_subscribes(PyObject *Py_UNUSED(self), PyObject *Py_UNUSED(args)) {
    dictionary_iterator dit;
    word_id name;
    PyObject *python_list, *python_string;

    python_list = PyList_New(0);

    get_dictionary_iterator(&name_dict, &dit);
    while(has_next_word(&dit)) {
        name = next_word(&dit);

        if (is_subscribed(&spec, name)) {
            python_string = PyUnicode_FromString(get_word(&name_dict, name));
            if (PyList_Append(python_list, python_string) == -1) {
                // Error!  It sets an error message.
                return NULL;
            }
            // unlike PyList_SetItem, append does not steal the reference
            Py_DECREF(python_string);
        }
    }

    return python_list;
}

PyDoc_STRVAR(publishes_method_doc, "Get the intervals which the current spec publishes.");
static PyObject * python_get_publishes(PyObject *Py_UNUSED(self), PyObject *Py_UNUSED(args)) {
    dictionary_iterator dit;
    word_id name;
    PyObject *python_list, *python_string;

    python_list = PyList_New(0);

    get_dictionary_iterator(&name_dict, &dit);
    while(has_next_word(&dit)) {
        name = next_word(&dit);

        if (is_published(&spec, name)) {
            python_string = PyUnicode_FromString(get_word(&name_dict, name));
            if (PyList_Append(python_list, python_string) == -1) {
                // Error!  It sets an error message.
                return NULL;
            }
            // unlike PyList_SetItem, append does not steal the reference
            Py_DECREF(python_string);
        }
    }

    return python_list;
}

PyDoc_STRVAR(window_method_doc, "Set a window size (default 0).  0 disables the window optimization.");
static PyObject * python_window(PyObject *Py_UNUSED(self), PyObject *args) {
    timestamp window;

    if (!PyArg_ParseTuple(args, "K", &window)) {
        return NULL;
    }
    opt_window_size = window;

    Py_RETURN_NONE;
}

PyDoc_STRVAR(minimal_method_doc, "Set minimality check on (True) (default) or off (False).");
static PyObject * python_minimal(PyObject *Py_UNUSED(self), PyObject *args) {
    int minimal;

    if (!PyArg_ParseTuple(args, "p", &minimal)) {
        return NULL;
    }
    opt_full = !minimal;

    Py_RETURN_NONE;
}

static PyMethodDef nfer_methods[] = {
    {"init",       python_init, METH_NOARGS, init_method_doc},
    {"load",       python_load_spec, METH_VARARGS, load_method_doc},
    {"scan",       python_scan_spec, METH_VARARGS, scan_method_doc},
    {"save",       python_save_spec, METH_VARARGS, save_method_doc},
    {"add",        python_add_interval, METH_VARARGS, add_method_doc},
    {"learn",      python_learn_spec, METH_VARARGS, learn_method_doc},
    {"subscribes", python_get_subscribes, METH_NOARGS, subscribes_method_doc},
    {"publishes",  python_get_publishes, METH_NOARGS, publishes_method_doc},
    {"window",     python_window, METH_VARARGS, window_method_doc},
    {"minimal",    python_minimal, METH_VARARGS, minimal_method_doc},

    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyDoc_STRVAR(nfer_module_doc,
       "The nfer module adds support to Python for the nfer language and system "
       "for abstracting event streams.  The API takes named intervals as inputs "
       "and returns named intervals.  The nfer DSL is flexible, and supports "
       "arbitrary data items and nested rules.  See http://nfer.io/ for more "
       "information.");

static struct PyModuleDef nfer_module = {
   PyModuleDef_HEAD_INIT,
   "_nfer",            /* name of module */
   nfer_module_doc,   /* module documentation, may be NULL */
   -1,                /* size of per-interpreter state of the module,
                         or -1 if the module keeps state in global variables. */
   nfer_methods,
   NULL,              /* single phase initialization, so m_slots is null */
   NULL,              /* m_traverse is not needed */
   NULL,              /* m_clear is not needed */
   NULL               /* m_free is not needed */
};

PyDoc_STRVAR(nfer_error_doc, "Reports an error that occurred in the nfer module.");
PyMODINIT_FUNC PyInit__nfer(void) {
    PyObject *module;

    module = PyModule_Create(&nfer_module);
    if (module == NULL) {
        return NULL;
    }

    nfer_error = PyErr_NewExceptionWithDoc("nfer.error", nfer_error_doc, NULL, NULL);
    Py_INCREF(nfer_error);
    PyModule_AddObject(module, "error", nfer_error);
    return module;
}


