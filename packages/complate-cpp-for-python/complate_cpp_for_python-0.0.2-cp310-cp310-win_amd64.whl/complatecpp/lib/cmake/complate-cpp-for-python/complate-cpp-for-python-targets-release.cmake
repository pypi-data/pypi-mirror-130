#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "complate-cpp-for-python::core" for configuration "Release"
set_property(TARGET complate-cpp-for-python::core APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(complate-cpp-for-python::core PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libcomplatecore.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS complate-cpp-for-python::core )
list(APPEND _IMPORT_CHECK_FILES_FOR_complate-cpp-for-python::core "${_IMPORT_PREFIX}/lib/libcomplatecore.a" )

# Import target "complate-cpp-for-python::quickjs" for configuration "Release"
set_property(TARGET complate-cpp-for-python::quickjs APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(complate-cpp-for-python::quickjs PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C;CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libcomplatequickjs.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS complate-cpp-for-python::quickjs )
list(APPEND _IMPORT_CHECK_FILES_FOR_complate-cpp-for-python::quickjs "${_IMPORT_PREFIX}/lib/libcomplatequickjs.a" )

# Import target "complate-cpp-for-python::v8" for configuration "Release"
set_property(TARGET complate-cpp-for-python::v8 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(complate-cpp-for-python::v8 PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libcomplatev8.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS complate-cpp-for-python::v8 )
list(APPEND _IMPORT_CHECK_FILES_FOR_complate-cpp-for-python::v8 "${_IMPORT_PREFIX}/lib/libcomplatev8.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
