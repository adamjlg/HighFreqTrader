using Xunit;
using HighFreqTrader.Controllers;
using HighFreqTrader.Services;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;
using HighFreqTrader.Models;

// basic unit test for now
// TODO: add integration tests
public class TradingControllerTests
{
    [Fact]
    public async Task SubmitOrder_ReturnsOk_WhenOrderIsSuccessful()
    {
        var mockEngine = new WebSocketEngineStub(); 
        var controller = new TradingController(mockEngine);

        var order = new OrderDto
        {
            Id = 1,
            Symbol = "AAPL",
            Price = 150.0,
            Quantity = 10,
            IsBuy = true
        };

        var result = await controller.SubmitOrder(order);

        Assert.IsType<OkResult>(result);
    }
}

public class WebSocketEngineStub : IWebSocketEngine
{
    public Task<bool> EnqueueOrderAsync(OrderDto order)
    {
        return Task.FromResult(true); // Always succeed
    }
}