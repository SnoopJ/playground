%include "numpy.i"
%init %{
import_array();
%}

%rename(wrappedbar) Bar::bar;

%include "bar.hpp"
