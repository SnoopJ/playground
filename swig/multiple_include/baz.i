%include "numpy.i"
%init %{
import_array();
%}

%rename(wrappedbar) Baz::bar;

%include "baz.hpp"
