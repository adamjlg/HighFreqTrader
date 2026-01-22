namespace HighFreqTrader.Models
{

    public class OrderDto
    {
        public int Id { get; set; }
        public string Symbol { get; set; }
        public double Price { get; set; }
        public int Quantity { get; set; }
        public bool IsBuy { get; set; }
    }
}