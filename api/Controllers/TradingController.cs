using System;
using Microsoft.AspNetCore.Mvc;
using System.Net.WebSockets;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using HighFreqTrader.Models;
using HighFreqTrader.Services;
namespace HighFreqTrader.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TradingController : ControllerBase
    {
        private readonly IWebSocketEngine _engine;

        public TradingController(IWebSocketEngine engine)
        {
            _engine = engine;
        }

        [HttpPost("orders")]
        public async Task<IActionResult> SubmitOrder([FromBody] OrderDto order)
        {
            bool success = await _engine.EnqueueOrderAsync(order);
            return success ? Ok() : StatusCode(500, "Queue full");
        }
    }

}
