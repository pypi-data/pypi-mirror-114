#include <pybind11/cast.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "MathEvaluator/include/evaluator.hpp"

namespace py = pybind11;

class py_Evaluator : public MathEvaluator{
public:
  py_Evaluator(bool accuracyOverEfficiency): MathEvaluator(accuracyOverEfficiency) {}

  void _appendVariable(const std::string name, const double value){
    double* heap_var = new double(value);
    appendVariable(name, *heap_var);
  }

  void _deleteVariable(const std::string name){
    delete getExternalVariables()[name];
    deleteVariable(name);
  }
};

PYBIND11_MODULE(InfixParser, m){

  // Construct Python Classes & Functions

  py::class_<me_RPN>(m, "mp_RPN")
    .def_readwrite("RPN", &me_RPN::RPN)
    .def_readwrite("RPN_values", &me_RPN::RPNValues);

  m.def("evaluate", &evaluate);

  py::class_<py_Evaluator>(m, "Evaluator")
    .def(py::init<bool>(), py::arg("accuracyOverEfficiency") = false)
    .def("append_variable", &py_Evaluator::_appendVariable)
    .def("delete_variable", &py_Evaluator::_deleteVariable)
    .def("variables", &py_Evaluator::getExternalVariables)
    .def("eval", &py_Evaluator::eval);
}
