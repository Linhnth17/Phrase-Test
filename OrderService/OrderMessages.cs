using System.Globalization;
using System.Resources;

namespace OrderService;

public static class OrderMessages
{
    private static readonly ResourceManager Resources = new("OrderService.Properties.Resources", typeof(OrderMessages).Assembly);

    public static string OrderPlaced => Resources.GetString("OrderPlaced", CultureInfo.InvariantCulture)!;
    public static string OrderCancelled => Resources.GetString("OrderCancelled", CultureInfo.InvariantCulture)!;
}
