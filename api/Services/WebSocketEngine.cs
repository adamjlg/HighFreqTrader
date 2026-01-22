using System;
using System.Net.WebSockets;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using HighFreqTrader.Models;

namespace HighFreqTrader.Services
{
    public interface IWebSocketEngine
    {
        Task<bool> EnqueueOrderAsync(OrderDto order);
    }

    public class WebSocketEngine : IWebSocketEngine
    {
        private readonly Uri _serverUri = new Uri("ws://localhost:9000");

        public async Task<bool> EnqueueOrderAsync(OrderDto order)
        {
            using (var ws = new ClientWebSocket())
            {
                await ws.ConnectAsync(_serverUri, CancellationToken.None);

                string orderJson = JsonSerializer.Serialize(order);
                byte[] buffer = Encoding.UTF8.GetBytes(orderJson);

                await ws.SendAsync(new ArraySegment<byte>(buffer), WebSocketMessageType.Text, true, CancellationToken.None);

                var responseBuffer = new byte[256];
                var result = await ws.ReceiveAsync(new ArraySegment<byte>(responseBuffer), CancellationToken.None);
                string response = Encoding.UTF8.GetString(responseBuffer, 0, result.Count);

                return response == "success";
            }
        }
    }
}