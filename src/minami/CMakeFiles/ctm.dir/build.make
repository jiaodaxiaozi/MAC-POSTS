# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.2

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/weima/MINAMI/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/weima/MINAMI/src

# Include any dependencies generated for this target.
include minami/CMakeFiles/ctm.dir/depend.make

# Include the progress variables for this target.
include minami/CMakeFiles/ctm.dir/progress.make

# Include the compile flags for this target's objects.
include minami/CMakeFiles/ctm.dir/flags.make

minami/CMakeFiles/ctm.dir/test_ctm.cpp.o: minami/CMakeFiles/ctm.dir/flags.make
minami/CMakeFiles/ctm.dir/test_ctm.cpp.o: minami/test_ctm.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/weima/MINAMI/src/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object minami/CMakeFiles/ctm.dir/test_ctm.cpp.o"
	cd /home/weima/MINAMI/src/minami && g++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/ctm.dir/test_ctm.cpp.o -c /home/weima/MINAMI/src/minami/test_ctm.cpp

minami/CMakeFiles/ctm.dir/test_ctm.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ctm.dir/test_ctm.cpp.i"
	cd /home/weima/MINAMI/src/minami && g++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/weima/MINAMI/src/minami/test_ctm.cpp > CMakeFiles/ctm.dir/test_ctm.cpp.i

minami/CMakeFiles/ctm.dir/test_ctm.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ctm.dir/test_ctm.cpp.s"
	cd /home/weima/MINAMI/src/minami && g++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/weima/MINAMI/src/minami/test_ctm.cpp -o CMakeFiles/ctm.dir/test_ctm.cpp.s

minami/CMakeFiles/ctm.dir/test_ctm.cpp.o.requires:
.PHONY : minami/CMakeFiles/ctm.dir/test_ctm.cpp.o.requires

minami/CMakeFiles/ctm.dir/test_ctm.cpp.o.provides: minami/CMakeFiles/ctm.dir/test_ctm.cpp.o.requires
	$(MAKE) -f minami/CMakeFiles/ctm.dir/build.make minami/CMakeFiles/ctm.dir/test_ctm.cpp.o.provides.build
.PHONY : minami/CMakeFiles/ctm.dir/test_ctm.cpp.o.provides

minami/CMakeFiles/ctm.dir/test_ctm.cpp.o.provides.build: minami/CMakeFiles/ctm.dir/test_ctm.cpp.o

minami/CMakeFiles/ctm.dir/dlink.cpp.o: minami/CMakeFiles/ctm.dir/flags.make
minami/CMakeFiles/ctm.dir/dlink.cpp.o: minami/dlink.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/weima/MINAMI/src/CMakeFiles $(CMAKE_PROGRESS_2)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object minami/CMakeFiles/ctm.dir/dlink.cpp.o"
	cd /home/weima/MINAMI/src/minami && g++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/ctm.dir/dlink.cpp.o -c /home/weima/MINAMI/src/minami/dlink.cpp

minami/CMakeFiles/ctm.dir/dlink.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ctm.dir/dlink.cpp.i"
	cd /home/weima/MINAMI/src/minami && g++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/weima/MINAMI/src/minami/dlink.cpp > CMakeFiles/ctm.dir/dlink.cpp.i

minami/CMakeFiles/ctm.dir/dlink.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ctm.dir/dlink.cpp.s"
	cd /home/weima/MINAMI/src/minami && g++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/weima/MINAMI/src/minami/dlink.cpp -o CMakeFiles/ctm.dir/dlink.cpp.s

minami/CMakeFiles/ctm.dir/dlink.cpp.o.requires:
.PHONY : minami/CMakeFiles/ctm.dir/dlink.cpp.o.requires

minami/CMakeFiles/ctm.dir/dlink.cpp.o.provides: minami/CMakeFiles/ctm.dir/dlink.cpp.o.requires
	$(MAKE) -f minami/CMakeFiles/ctm.dir/build.make minami/CMakeFiles/ctm.dir/dlink.cpp.o.provides.build
.PHONY : minami/CMakeFiles/ctm.dir/dlink.cpp.o.provides

minami/CMakeFiles/ctm.dir/dlink.cpp.o.provides.build: minami/CMakeFiles/ctm.dir/dlink.cpp.o

# Object files for target ctm
ctm_OBJECTS = \
"CMakeFiles/ctm.dir/test_ctm.cpp.o" \
"CMakeFiles/ctm.dir/dlink.cpp.o"

# External object files for target ctm
ctm_EXTERNAL_OBJECTS =

minami/ctm: minami/CMakeFiles/ctm.dir/test_ctm.cpp.o
minami/ctm: minami/CMakeFiles/ctm.dir/dlink.cpp.o
minami/ctm: minami/CMakeFiles/ctm.dir/build.make
minami/ctm: 3rdparty/g3log/libg3log.a
minami/ctm: minami/libminami.so
minami/ctm: snap-core/libSnap.so
minami/ctm: glib-core/libGlib.so
minami/ctm: 3rdparty/g3log/libg3log.a
minami/ctm: minami/CMakeFiles/ctm.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX executable ctm"
	cd /home/weima/MINAMI/src/minami && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/ctm.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
minami/CMakeFiles/ctm.dir/build: minami/ctm
.PHONY : minami/CMakeFiles/ctm.dir/build

minami/CMakeFiles/ctm.dir/requires: minami/CMakeFiles/ctm.dir/test_ctm.cpp.o.requires
minami/CMakeFiles/ctm.dir/requires: minami/CMakeFiles/ctm.dir/dlink.cpp.o.requires
.PHONY : minami/CMakeFiles/ctm.dir/requires

minami/CMakeFiles/ctm.dir/clean:
	cd /home/weima/MINAMI/src/minami && $(CMAKE_COMMAND) -P CMakeFiles/ctm.dir/cmake_clean.cmake
.PHONY : minami/CMakeFiles/ctm.dir/clean

minami/CMakeFiles/ctm.dir/depend:
	cd /home/weima/MINAMI/src && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/weima/MINAMI/src /home/weima/MINAMI/src/minami /home/weima/MINAMI/src /home/weima/MINAMI/src/minami /home/weima/MINAMI/src/minami/CMakeFiles/ctm.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : minami/CMakeFiles/ctm.dir/depend

