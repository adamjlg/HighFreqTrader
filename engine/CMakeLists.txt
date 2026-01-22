cmake_minimum_required(VERSION 3.21)

project(HighFreqTraderEngine LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Engine library
add_library(HighFreqTraderEngine STATIC
    SPSCQueue.h
    OrderBook.cpp
    Engine.cpp
)

find_package(Boost REQUIRED COMPONENTS system beast)
find_package(nlohmann_json CONFIG REQUIRED)


add_executable(WebSocketServer
    src/WebSocketServer.cpp
)

target_link_libraries(WebSocketServer PRIVATE
    HighFreqTraderEngine
    Boost::system
    Boost::beast
    nlohmann_json::nlohmann_json
)

if (MSVC)
    target_compile_options(WebSocketServer PRIVATE /W4 /permissive-)
endif()