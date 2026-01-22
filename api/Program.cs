using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using HighFreqTrader.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddSingleton<IWebSocketEngine, WebSocketEngine>();
builder.Services.AddControllers();

var app = builder.Build();

app.MapControllers();

app.Run();
