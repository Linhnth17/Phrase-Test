// See https://aka.ms/new-console-template for more information
using System.Globalization;
using System.Resources;

var resources = new ResourceManager("Test_phrase.Properties.Resources", typeof(Program).Assembly);

Console.WriteLine(resources.GetString("Greeting", CultureInfo.InvariantCulture));
Console.WriteLine(resources.GetString("OrderConfirmation", CultureInfo.InvariantCulture));
Console.WriteLine(resources.GetString("WelcomeMessage", CultureInfo.InvariantCulture));
