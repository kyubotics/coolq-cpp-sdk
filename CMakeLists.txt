cmake_minimum_required(VERSION 3.9)
project(coolq-cpp-sdk)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "/utf-8 ${CMAKE_CXX_FLAGS}")  # use UTF-8 source files
set(CMAKE_CXX_FLAGS "/MP ${CMAKE_CXX_FLAGS}")  # build with object level parallelism

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/Modules/")

include(FindVcpkgIncludeDir)

if(CMAKE_BUILD_TYPE MATCHES "^Debug$")
    # fix Vcpkg debug library lookup bug, see https://github.com/Microsoft/vcpkg/issues/1626
    list(APPEND CMAKE_IGNORE_PATH ${_VCPKG_INSTALLED_DIR}/${VCPKG_TARGET_TRIPLET}/lib)
endif()

include_directories(${VCPKG_INCLUDE_DIR})
include_directories(src)

add_definitions(-DBOOST_CONFIG_SUPPRESS_OUTDATED_MESSAGE
                -D_WIN32_WINNT=0x0501
                -DWIN32_LEAN_AND_MEAN
				-DNOMINMAX)

find_package(Iconv REQUIRED)

include(FixLinkConflict)

file(GLOB_RECURSE SOURCE_FILES src/*.cpp)
set(LIB_NAME "com.example.demo")
add_library(${LIB_NAME} SHARED ${SOURCE_FILES})

target_link_libraries(${LIB_NAME} ${ICONV_AND_DEPS_LIBRARIES})

add_custom_command(TARGET ${LIB_NAME}
                   POST_BUILD
                   COMMAND
                   powershell -ExecutionPolicy Bypass -NoProfile -File "${PROJECT_SOURCE_DIR}/scripts/post_build.ps1" ${LIB_NAME} "$<TARGET_FILE_DIR:${LIB_NAME}>")
