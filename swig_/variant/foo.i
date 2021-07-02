%module foo

%include "std_string.i"
%include "stdint.i"
%include "std_unordered_map.i"

%{
#include <iostream>
#include <string>
#include <unordered_map>
#include <variant>
#include "foo.hpp"
%}

// declaring %immutable will not generate a setter for the unordered_map that
// contains the move-only class, which prevents SWIG from trying to use the 
// deleted copy operations
%immutable Bar::m_map;

// unfortunately, I believe we must also explicitly ignore any method that returns
// the offending type, or the same copying code will be generated
%ignorewarn("ignoring Bar::baz()") Bar::baz;

%template(UMapStringCopyableMember) std::unordered_map<std::string, int>;

// N.B. if we instantiated the template here, we would codegen the bad copy
//%template(UMapStringMoveOnlyFoo) std::unordered_map<std::string, MoveOnlyFoo>;


// This typemap unpacks the variant of interest to a suitable wrapper for the value present
%typemap(out)
    (std::variant<CopyableMemberMap, MoveOnlyMemberMap>*)
{
    //std::cout << "variant index() = " << ($1)->index() << std::endl;
    //std::cout << "m_map is CopyableMemberMap: " << std::holds_alternative<CopyableMemberMap>(*$1) << std::endl;
    //std::cout << "m_map is MoveOnlyMemberMap: " << std::holds_alternative<MoveOnlyMemberMap>(*$1) << std::endl;

    if (std::holds_alternative<CopyableMemberMap>(*$1))
    {
        CopyableMemberMap* p = &std::get<CopyableMemberMap>(*$1);
        // All we needed to do was unpack the variant, we let SWIG do the rest
        // of the work with the type descriptor it already knows
        $result = SWIG_NewPointerObj(p, $descriptor(CopyableMemberMap *), 0);
    } else if (std::holds_alternative<MoveOnlyMemberMap>(*$1))
    {
        MoveOnlyMemberMap* p = &std::get<MoveOnlyMemberMap>(*$1);
        $result = SWIG_NewPointerObj(p, $descriptor(MoveOnlyMemberMap *), 0);
    } else {
        std::cout << "Unknown variant alternative, goodbye cruel world! (got type " << typeid($1).name() << ")" << std::endl;
        SWIG_fail;
    }
}

// NOTE:20201117:jgerity:I think the unpacking of the variant could be generic
// instead of the very explicit spelling above, the below is a partial
// (nonworking) sketch
/*
auto T = std::variant_alternative<($1)->index(), $1>;
T* p = &std::get<T>(*$1);
$result = SWIG_NewPointerObj(p, $descriptor(T*), 0);
*/

%include foo.hpp
