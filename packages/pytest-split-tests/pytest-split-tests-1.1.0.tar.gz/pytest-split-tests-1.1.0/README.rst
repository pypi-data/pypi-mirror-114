Welcome to pytest-split-tests!
==============================

pytest-split-tests allows you to split your test runs into groups of a specific
size to make it easier to split up your test runs.


Usage
---------------------

::

    # Install pytest-split-tests
    pip install pytest-split-tests

    # Split the tests into 10 groups and run the second group
    py.test --test-group-count 10 --test-group=2
    
    # Assign tests pseudo-randomly into 10 groups, and run the second group
    py.test --test-group-count 10 --test-group=2 --test-group-random-seed=12345


Why would I use this?
------------------------------------------------------------------

Sometimes you may have some long running test jobs that take a
while to complete. This can be a major headache when trying to
run tests quickly. pytest-split-tests allows you to easily say
"split my tests into groups of 10 tests and run the second group".
This is primarily useful in the context of CI builds.
