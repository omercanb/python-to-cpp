#define PY_MAJOR_VERSION 3
#undef ENABLE_PYTHON_MODULE
#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/builtins/None.hpp>
#include <pythonic/include/builtins/assert.hpp>
#include <pythonic/include/builtins/list.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/eq.hpp>
#include <pythonic/include/operator_/iadd.hpp>
#include <pythonic/builtins/None.hpp>
#include <pythonic/builtins/assert.hpp>
#include <pythonic/builtins/list.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/eq.hpp>
#include <pythonic/operator_/iadd.hpp>
namespace 
{
  namespace __pythran_input
  {
    struct multiple_assignment
    {
      typedef void callable;
      typedef void pure;
      struct type
      {
        typedef pythonic::types::none_type __type0;
        typedef typename pythonic::returnable<__type0>::type __type1;
        typedef __type1 result_type;
      }  ;
      inline
      typename type::result_type operator()() const;
      ;
    }  ;
    inline
    typename multiple_assignment::type::result_type multiple_assignment::operator()() const
    {
      typedef long __type0;
      typedef pythonic::types::make_tuple_t<__type0, __type0> __type1;
      typedef std::tuple_element_t<0, std::remove_reference_t<__type1>> __type2;
      typedef typename pythonic::assignable<__type1>::type __type3;
      typedef decltype(pythonic::types::as_const(std::declval<__type3>())) __type4;
      typedef std::tuple_element_t<0, std::remove_reference_t<__type4>> __type5;
      typedef typename pythonic::assignable<__type5>::type __type6;
      typedef typename __combined<__type0,__type2,__type5,__type6>::type __type7;
      typedef std::tuple_element_t<1, std::remove_reference_t<__type1>> __type8;
      typedef std::tuple_element_t<1, std::remove_reference_t<__type4>> __type9;
      typedef typename __combined<__type8,__type9>::type __type10;
      typedef typename pythonic::lazy<__type10>::type __type11;
      typedef typename __combined<__type0,__type8,__type9,__type11>::type __type12;
      typedef typename pythonic::assignable<__type7>::type __type13;
      typedef typename pythonic::lazy<__type12>::type __type14;
      typedef pythonic::types::list<std::remove_reference_t<__type0>> __type15;
      typedef typename pythonic::assignable<__type15>::type __type16;
      typedef std::integral_constant<__type0, 0> __type17;
      typedef decltype(pythonic::types::as_const(std::declval<__type15>())) __type18;
      typedef std::tuple_element_t<1, std::remove_reference_t<__type18>> __type19;
      typedef std::tuple_element_t<0, std::remove_reference_t<__type18>> __type20;
      typedef pythonic::types::make_tuple_t<__type19, __type20> __type21;
      typedef typename pythonic::assignable<__type21>::type __type22;
      typedef decltype(pythonic::types::as_const(std::declval<__type22>())) __type23;
      typedef std::tuple_element_t<0, std::remove_reference_t<__type23>> __type24;
      typedef indexable_container<__type17, std::remove_reference_t<__type24>> __type25;
      typedef indexable<__type0> __type26;
      typedef std::integral_constant<__type0, 1> __type27;
      typedef std::tuple_element_t<1, std::remove_reference_t<__type23>> __type28;
      typedef indexable_container<__type27, std::remove_reference_t<__type28>> __type29;
      typedef typename __combined<__type15,__type25,__type26,__type29>::type __type30;
      typedef typename pythonic::assignable<__type30>::type __type31;
      typedef decltype(pythonic::types::as_const(std::declval<__type30>())) __type32;
      typedef std::tuple_element_t<0, std::remove_reference_t<__type32>> __type33;
      typedef typename pythonic::lazy<__type33>::type __type34;
      typedef decltype(pythonic::operator_::add(std::declval<__type7>(), std::declval<__type34>())) __type35;
      typedef decltype(pythonic::operator_::add(std::declval<__type0>(), std::declval<__type35>())) __type36;
      typedef typename __combined<__type0,__type36>::type __type37;
      typedef typename pythonic::assignable<__type37>::type __type38;
      __type13 x = 0L;
      __type14 y = 1L;
      __type31 a = __type16({static_cast<typename __type16::value_type>(2L), static_cast<typename __type16::value_type>(3L)});
      __type38 n = 0L;
      {
        long  __target1 = 1000000L;
        for (long  i=0L; i < __target1; i += 1L)
        {
          typename pythonic::assignable_noescape<decltype(pythonic::types::make_tuple(y, x))>::type __tuple0 = pythonic::types::make_tuple(y, x);
          x = std::get<0>(pythonic::types::as_const(__tuple0));
          y = std::get<1>(pythonic::types::as_const(__tuple0));
          typename pythonic::assignable_noescape<decltype(pythonic::types::make_tuple(std::get<1>(pythonic::types::as_const(a)), std::get<0>(pythonic::types::as_const(a))))>::type __tuple1 = pythonic::types::make_tuple(std::get<1>(pythonic::types::as_const(a)), std::get<0>(pythonic::types::as_const(a)));
          std::get<0>(a) = std::get<0>(pythonic::types::as_const(__tuple1));
          std::get<1>(a) = std::get<1>(pythonic::types::as_const(__tuple1));
          typename pythonic::lazy<decltype(std::get<0>(pythonic::types::as_const(a)))>::type xx = std::get<0>(pythonic::types::as_const(a));
          typename pythonic::lazy<decltype(std::get<1>(pythonic::types::as_const(a)))>::type yy = std::get<1>(pythonic::types::as_const(a));
          n += pythonic::operator_::add(x, xx);
        }
      }
      pythonic::pythran_assert(pythonic::operator_::eq(n, 3000000L), n);
      return pythonic::builtins::None;
    }
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE

static PyMethodDef Methods[] = {

    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef moduledef = {
  PyModuleDef_HEAD_INIT,
  "input",            /* m_name */
  "",         /* m_doc */
  -1,                  /* m_size */
  Methods,             /* m_methods */
  NULL,                /* m_reload */
  NULL,                /* m_traverse */
  NULL,                /* m_clear */
  NULL,                /* m_free */
};
PyMODINIT_FUNC
PyInit_input(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
#if defined(GNUC) && !defined(__clang__)
__attribute__ ((externally_visible))
#endif
#endif
;
PyMODINIT_FUNC
PyInit_input(void) {
    import_array();

    PyObject* theModule = PyModule_Create(&moduledef);
    if(! theModule)
        return theModule;

                #ifdef Py_GIL_DISABLED
                    PyUnstable_Module_SetGIL(theModule, Py_MOD_GIL_NOT_USED);
                #endif
    PyObject * theDoc = Py_BuildValue("(ss)",
                                      "0.18.1",
                                      "de7a134288782151cf6fd86a52acca6e15c4c0f7ce7fe75f25305c8e75325ffd");
    if(! theDoc)
        return theModule;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    return theModule;
}

#endif