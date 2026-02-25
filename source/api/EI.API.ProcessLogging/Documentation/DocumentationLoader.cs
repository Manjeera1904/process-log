using System.Xml.XPath;

namespace EI.API.ProcessLogging.Documentation;

internal static class DocumentationLoader
{
    internal static XPathDocument? GetXmlDocs()
    {
        var assembly = typeof(DocumentationLoader).Assembly;
        var resourceNames = assembly.GetManifestResourceNames();
        var resourceName = resourceNames.Single(n => n.EndsWith("EI.API.ProcessLogging.xml"));

        using var stream = assembly.GetManifestResourceStream(resourceName);
        return stream == null ? null : new XPathDocument(stream);
    }
}
