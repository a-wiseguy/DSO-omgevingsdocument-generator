from lxml import etree
from bs4 import BeautifulSoup


# Your input HTML content
html_content = """
<h2>Inleiding</h2>

<h3>Leeswijzer</h3>

<p>
	De Zuid‐Hollandse leefomgeving verbeteren, elke dag, dat is waar de
	provincie aan werkt. Zeven vernieuwingsambities laten zien waar
	Zuid‐Holland naartoe wil. Noem het gerust uitdagingen. Met de zeven
	ambities maakt de provincie ruimte voor belangrijke ontwikkelingen rond
	participatie, bereikbaarheid, energie, economie, natuur, woningbouw en
	gezondheid en veiligheid. Wie vooral benieuwd is naar de vergezichten en
	kansen gaat direct naar hoofdstuk 4 waar de ambities op een rij staan. Dat
	hoofdstuk is de kern van dit document. Welke kaders en uitgangspunten bij
	het werken aan die ambities gelden, staat beschreven in hoofdstuk 5.
	Hoofdstuk 3 laat zien waar de provincie Zuid‐Holland nu staat. De
	sturingsfilosofie die de provincie gebruikt om, samen met partners, te
	groeien van waar Zuid‐Holland nu staat naar waar de provincie naartoe
	wil, is het onderwerp van hoofdstuk 2. De wijze waarop ons beleid tot stand
	komt staat beschreven in Hoofdstuk 6. De hoofdstukken 7 tot en met 8 ten
	slotte maken het beeld compleet met een integraal overzicht van alle
	beleidsdoelen, beleidskeuzes en de kaarten die op hoofdlijnen . Dit
	hoofdstuk is ook (actueel) te raadplegen via <a href="https://omgevingsbeleid.pzh.nl">
		https://omgevingsbeleid.zuid‐holland.nl</a>
</p>

<h3>Doel en opzet</h3>
<p>De Omgevingsvisie van Zuid‐Holland biedt een strategische blik op de
	lange(re) termijn voor de gehele fysieke leefomgeving en bevat de hoofdzaken
	van het te voeren integrale beleid van de provincie Zuid‐Holland. De
	Omgevingsvisie vormt samen met de Omgevingsverordening en het
	Omgevingsprogramma het provinciale Omgevingsbeleid van de provincie
	Zuid‐Holland. Het Omgevingsbeleid beschrijft hoe de provincie werkt
	aan een goede leefomgeving, welke plannen daarvoor zijn, welke regels
	daarbij gelden en welke inspanningen de provincie daarvoor levert.</p>
<p>Dit document is een provinciale Omgevingsvisie die functioneert in het
	huidige en toekomstige (juridische) stelsel voor de fysieke leefomgeving. De
	Omgevingsvisie is een instrument dat uiteindelijk moet gaan functioneren
	zoals bedoeld in de Omgevingswet. Vooruitlopend op die Omgevingswet moet de
	provincie vanuit de huidige wet‐ en regeling beschikken over een
	aantal visies en plannen. De Omgevingsvisie omvat de volgende wettelijk
	verplichte plannen:</p>
<p>‐ de provinciale ruimtelijke structuurvisie, artikel 2.2 van de Wet
	ruimtelijke ordening (Wro);</p>
<p>‐ het milieubeleidsplan, artikel 4.9 van de Wet milieubeheer (Wm);</p>
<p>‐ (delen van) het regionale waterplan, artikel 4.4 van de Waterwet
	(Ww)<sup>1</sup> ;</p>
<p>‐ het verkeers‐ en vervoersplan, artikel 5 van de Planwet
	verkeer en vervoer;</p>
<p>‐ de natuurvisie, artikel 1.7 van de Wet natuurbescherming (Wnb)</p>
<p>Zodra de Omgevingswet in werking is getreden zal deze Omgevingsvisie via het
	overgangsrecht <sup>2</sup> gelden als een omgevingsvisie, zoals in de
	nieuwe wet is bedoeld.</p>
<p>(1) Het waterbeleid met een ruimtelijke component is opgenomen in de
	Omgevingsvisie, het beleid voor waterkwaliteit staat in de Voortgangsnota
	Europese Kaderrichtlijn Water 2016‐2021. Voor een klein aantal
	onderdelen blijft het provinciale waterplan 2010‐2015 ongewijzigd van
	kracht. Deze delen zullen onder de Omgevingswet deel gaan uitmaken van het
	Regionale Waterprogramma.</p>
<p>(2) Op basis artikel 4.10, tweede lid, van de Invoeringswet Omgevingswet
	geldt een provinciale omgevingsvisie die van kracht is voor of direct na
	inwerkingtreding van artikel 3.1, tweede lid, van de Omgevingswet, en
	voldoet aan de artikelen 3.2 en 3.3, als een provinciale omgevingsvisie als
	bedoeld in artikel 3.1, tweede lid, van de Omgevingswet.</p>
"""

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Create the root element of the XML structure
root = etree.Element("Root")  # Assuming the root element is named "Root"

# Initialize the current division and divisietekst
current_division = None
current_divisietekst = None

# Iterate over each element in the body of the HTML
for tag in soup.find_all(['h2', 'h3', 'p']):
    if tag.name == 'h2':
        # Create a new division element
        current_division = etree.SubElement(root, "Divisie")
        # Reset current divisietekst
        current_divisietekst = None
    elif tag.name == 'h3':
        # Close the previous divisietekst if any
        current_divisietekst = None
        # Start a new Divisietekst within the current division
        if current_division is not None:
            current_divisietekst = etree.SubElement(current_division, "Divisietekst")
            kop = etree.SubElement(current_divisietekst, "Kop")
            etree.SubElement(kop, "Opschrift").text = tag.text.strip()
    elif tag.name == 'p':
        # Only add paragraphs if there is a current divisietekst
        if current_divisietekst is not None:
            inhoud = etree.SubElement(current_divisietekst, "Al")
            # Handle external references if they exist
            if tag.find('a'):
                for a in tag.find_all('a'):
                    ext_ref = etree.SubElement(inhoud, "ExtRef", ref=a['href'])
                    ext_ref.text = a.text
                    # remove the anchor from the tag
                    a.replace_with(a.text)
            inhoud.text = (tag.text or '').strip()

# Convert the XML to a string
xmlstr = etree.tostring(root, pretty_print=True, encoding='unicode')

# Print the formatted XML
print(xmlstr)
