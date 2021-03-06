# A sample Makefile for building Google Test and using it in user
# tests.  Please tweak it to suit your environment and project.  You
# may want to move it to your project's root directory.
#
# SYNOPSIS:
#
#   make [all]  - makes everything.
#   make TARGET - makes the given target.
#   make clean  - removes all files generated by make.

# Please tweak the following variable definitions as needed by your
# project, except GTEST_HEADERS, which you can use in your own targets
# but shouldn't modify.

# Points to the root of Google Test, relative to where this file is.
# Remember to tweak this if you move this file.
GTEST_DIR =gtest

# Where to find user code.
USER_DIR = .

# Flags passed to the preprocessor.
# Set Google Test's header directory as a system directory, such that
# the compiler doesn't generate warnings in Google Test headers.
CPPFLAGS += --std=c++11 -isystem $(GTEST_DIR)/include

# Flags passed to the C++ compiler.
CXXFLAGS += -g -Wall -Wextra -pthread

# All tests produced by this Makefile.  Remember to add new tests you
# created to the list.
TESTS = test_iforest

# All Google Test headers.  Usually you shouldn't change this
# definition.
GTEST_HEADERS = $(GTEST_DIR)/include/gtest/*.h \
                $(GTEST_DIR)/include/gtest/internal/*.h

# House-keeping build targets.

all : $(TESTS)
fresh:
	make clean
	make
clean :
	rm -f $(TESTS) gtest.a gtest_main.a *.o
	rm -rf ../C/*.o*
	rm -rf ../C/*.exe
# Builds gtest.a and gtest_main.a.

# Usually you shouldn't tweak such internal variables, indicated by a
# trailing _.
GTEST_SRCS_ = $(GTEST_DIR)/src/*.cc $(GTEST_DIR)/src/*.h $(GTEST_HEADERS)

# For simplicity and to avoid depending on Google Test's
# implementation details, the dependencies specified below are
# conservative and not optimized.  This is fine as Google Test
# compiles fast and for ordinary users its source rarely changes.
gtest-all.o : $(GTEST_SRCS_)
	$(CXX) $(CPPFLAGS) -I$(GTEST_DIR) $(CXXFLAGS) -c \
$(GTEST_DIR)/src/gtest-all.cc

gtest_main.o : $(GTEST_SRCS_)
	$(CXX) $(CPPFLAGS) -I$(GTEST_DIR) $(CXXFLAGS) -c \
            $(GTEST_DIR)/src/gtest_main.cc

gtest.a : gtest-all.o
	$(AR) $(ARFLAGS) $@ $^

gtest_main.a : gtest-all.o gtest_main.o
	$(AR) $(ARFLAGS) $@ $^

# Builds a sample test.  A test should link with either gtest.a or
# gtest_main.a, depending on whether it defines its own main()
# function.

CC=g++
CFLAGS=--std=c99 -D_GNU_SOURCE -Wall -Werror -g
PP=g++
INCLUDES=../Eigen/ 
PFLAGS=--std=c++11 -Wall -Werror -g
#../C/%.o: ../C/%.c ../C/%.h
#	$(CC) $(CFLAGS) -c $< -o $@

#cincl.o: ../C/common.o ../C/object.o ../C/strfun.o ../C/readwrite.o ../C/argparse.o ../C/argparse_iforest.o ../C/frames.o
#	ld -r ../C/common.o ../C/object.o ../C/strfun.o ../C/readwrite.o ../C/argparse.o ../C/argparse_iforest.o ../C/frames.o -o cincl.o

%.o: ../%.cpp ../%.hpp ../json/json.hpp 
	$(PP) $(PFLAGS) -I $(INCLUDES) -c $< -o $@

%.o:%.cpp %.hpp $(GTEST_HEADERS) ../%.hpp
	$(PP) $(PFLAGS)$(CXXFLAGS)  -I $(INCLUDES) -c $< -o $@

test_iforest: utility.o Tree.o Forest.o IsolationForest.o test_tree.o test_utility.o FacadeForest.o test_FacadeForest.o test_Forest.o gtest_main.a
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -L$(INCLUDES) -lpthread $^ -o $@
