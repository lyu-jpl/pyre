// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
// 

#if !defined(gsl_extension_blas_h)
#define gsl_extension_blas_h


// place everything in my private namespace
namespace gsl {
    namespace blas {

        extern const char * const ddot__name__;
        extern const char * const ddot__doc__;
        PyObject * ddot(PyObject *, PyObject *);

        extern const char * const dnrm2__name__;
        extern const char * const dnrm2__doc__;
        PyObject * dnrm2(PyObject *, PyObject *);

        extern const char * const dasum__name__;
        extern const char * const dasum__doc__;
        PyObject * dasum(PyObject *, PyObject *);

        extern const char * const daxpy__name__;
        extern const char * const daxpy__doc__;
        PyObject * daxpy(PyObject *, PyObject *);

    } // of namespace blas
} // of namespace gsl

#endif

// end of file