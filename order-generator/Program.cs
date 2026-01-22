// TODO: implement
using System.Net.Http.Json;
var client = new HttpClient();
var rnd = new Random();
for (int i = 1; i <= 1000; i++)
{
    var order = new
    {
        Id = i,
        Symbol = "AAPL",
        Price = 100 + rnd.NextDouble() * 10,
        Quantity = rnd.Next(1, 100),
        IsBuy = rnd.Next(0, 2) == 0
    };
    await client.PostAsJsonAsync("http://localhost:5183/trading/orders", order);
}