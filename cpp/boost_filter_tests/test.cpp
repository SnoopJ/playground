#include <algorithm>
#include <iostream>
#include <vector>

#define BOOST_TEST_MODULE tests_with_preconditions
#include <boost/test/included/unit_test.hpp>

namespace tt = boost::test_tools;
// see Boost doc:
// https://www.boost.org/doc/libs/1_80_0/libs/test/doc/html/boost_test/tests_organization/enabling.html#boost_test.tests_organization.enabling.runtime_run_status
using precondition = boost::unit_test::precondition;

const std::string supportedNet = "f29ba21e-73a7-45c5-8dc6-4b7321ddb591";
const std::string unsupportedNet = "5398054a-9c0a-46ad-a097-97f8a1ebbb6d";
const std::vector<std::string> SUPPORTED_NETWORKS{supportedNet};

/*
 * Indicates if the given UUID is compatible with the current build
 *
 * Corresponds to functionality from $employerProduct
 */
bool isSupported(std::string uuid)
{
    auto result = std::find(std::begin(SUPPORTED_NETWORKS), std::end(SUPPORTED_NETWORKS), uuid);

    return (result != std::end(SUPPORTED_NETWORKS));
}

#define REQUIRES(uuid) *boost::unit_test::precondition(networkSupported(uuid))

// Boost wants something with an operator() to use with precondition
struct networkSupported
{
  std::string uuid;
  networkSupported(std::string uuid_)
    : uuid(uuid_) {}

  tt::assertion_result operator()(boost::unit_test::test_unit_id)
  {
    return isSupported(uuid);
  }
};

BOOST_AUTO_TEST_CASE(should_run, REQUIRES(supportedNet))
{
  BOOST_TEST(true);
}

BOOST_AUTO_TEST_CASE(should_not_run, REQUIRES(unsupportedNet))
{
  // This test would fail, but won't be run
  BOOST_TEST(false);
}
