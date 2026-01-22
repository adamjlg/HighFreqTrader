#include <boost/asio.hpp>
#include <boost/beast.hpp>
#include <boost/beast/websocket.hpp>
#include <iostream>
#include <nlohmann/json.hpp> 
#include <thread>
#include <functional>
#include <exception>

using json = nlohmann::json;
namespace beast = boost::beast;         
namespace http = beast::http;          
namespace websocket = beast::websocket; 
namespace net = boost::asio;           
using tcp = net::ip::tcp;              

class WebSocketServer {
public:
    WebSocketServer(net::io_context& ioc, tcp::endpoint endpoint)
        : acceptor_(ioc, endpoint) {}

    void run() {
        do_accept();
    }

private:
    tcp::acceptor acceptor_;

    void do_accept() {
        acceptor_.async_accept(
            [this](beast::error_code ec, tcp::socket socket) {
                if (!ec) {
                    std::make_shared<Session>(std::move(socket))->start();
                } else {
                    std::cerr << "Accept error: " << ec.message() << std::endl;
                }
                do_accept();
            });
    }

    class Session : public std::enable_shared_from_this<Session> {
    public:
        explicit Session(tcp::socket socket)
            : ws_(std::move(socket)) {}

        void start() {
            ws_.async_accept(
                [self = shared_from_this()](beast::error_code ec) {
                    if (!ec) {
                        self->do_read();
                    } else {
                        std::cerr << "WebSocket accept error: " << ec.message() << std::endl;
                    }
                });
        }

    private:
        websocket::stream<beast::tcp_stream> ws_;
        beast::flat_buffer buffer_;

        void do_read() {
            ws_.async_read(
                buffer_,
                [self = shared_from_this()](beast::error_code ec, std::size_t bytes_transferred) {
                    boost::ignore_unused(bytes_transferred);
                    if (!ec) {
                        self->on_message();
                    } else {
                        std::cerr << "Read error: " << ec.message() << std::endl;
                    }
                });
        }

        void on_message() {
            try {
                // Parse incoming message as JSON
                auto message = beast::buffers_to_string(buffer_.data());
                auto data = json::parse(message);
                std::cout << "Received order: " << data.dump() << std::endl;

                // Do something with the order
                bool success = true;

                // Send response to the client
                json response = {{"status", success ? "success" : "failure"}};
                do_write(response.dump());
            } catch (const std::exception& e) {
                std::cerr << "Message processing error: " << e.what() << std::endl;
            }
        }

        void do_write(const std::string& message) {
            ws_.async_write(
                net::buffer(message),
                [self = shared_from_this()](beast::error_code ec, std::size_t bytes_transferred) {
                    boost::ignore_unused(bytes_transferred);
                    if (!ec) {
                        self->buffer_.consume(self->buffer_.size()); // Clear buffer
                        self->do_read(); // Continue reading
                    } else {
                        std::cerr << "Write error: " << ec.message() << std::endl;
                    }
                });
        }
    };
};

int main() {
    try {
        net::io_context ioc;

        // Define endpoint port
        tcp::endpoint endpoint(tcp::v4(), 9000);

        WebSocketServer server(ioc, endpoint);
        server.run();

        // Run I/O context
        ioc.run();
    } catch (const std::exception& e) {
        std::cerr << "Fatal error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}