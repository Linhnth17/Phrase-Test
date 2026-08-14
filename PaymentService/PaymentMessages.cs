using System.Globalization;
using System.Resources;

namespace PaymentService;

public static class PaymentMessages
{
    private static readonly ResourceManager Resources = new("PaymentService.Properties.Resources", typeof(PaymentMessages).Assembly);

    public static string PaymentSuccess => Resources.GetString("PaymentSuccess", CultureInfo.InvariantCulture)!;
    public static string PaymentFailed => Resources.GetString("PaymentFailed", CultureInfo.InvariantCulture)!;
}
