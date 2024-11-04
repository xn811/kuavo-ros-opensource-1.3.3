#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "hpipm" for configuration "RelWithDebInfo"
set_property(TARGET hpipm APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(hpipm PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELWITHDEBINFO "blasfeo"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libhpipm.so"
  IMPORTED_SONAME_RELWITHDEBINFO "libhpipm.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS hpipm )
list(APPEND _IMPORT_CHECK_FILES_FOR_hpipm "${_IMPORT_PREFIX}/lib/libhpipm.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
