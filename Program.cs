// See https://aka.ms/new-console-template for more information
using System.Globalization;
using System.Resources;

var resources = new ResourceManager("Test_phrase.Resources.Resources", typeof(Program).Assembly);

Console.WriteLine(resources.GetString("Greeting", CultureInfo.InvariantCulture));
Console.WriteLine(resources.GetString("Farewell", CultureInfo.InvariantCulture));
