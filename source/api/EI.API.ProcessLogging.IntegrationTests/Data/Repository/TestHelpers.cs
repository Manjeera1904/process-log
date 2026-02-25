namespace EI.API.ProcessLogging.IntegrationTests.Data.Repository;

public static class TestHelpers
{
    public static string GetRandom(int maxLength)
    {
        var random = new byte[100];

        var data = string.Empty;
        while (data.Length < maxLength)
        {
            Random.Shared.NextBytes(random);
            data += Convert.ToBase64String(random);
        }

        return data[..maxLength];
    }
}
