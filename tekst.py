from bs4 import BeautifulSoup

from app.tekst.tekst import Divisie
from data import html_content


# html_content = """
# <h1>Title with a <em>bold</em> piece of text</h1>
# <p>Line 1</p>
# <p>Text with <em>important</em> parts</p>
# <ul>
#     <li><p>First un ordered list item</p></li>
#     <li><p><em>Second</em> un ordered list item</p></li>
# </ul>
# <p>We might have more!</p>
# <ol>
#     <li><p>First ordered list item</p></li>
#     <li><p><em>Second</em> ordered list item</p></li>
#     <li>
#         <ol>
#             <li><p>Deeper list item 1!</p></li>
#             <li><p>Deeper list item 2!</p></li>
#             <li><p>Deeper list item 3!</p></li>
#             <li><p>Deeper list item 4!</p></li>
#             <li><p>Deeper list item 5!</p></li>
#             <li>
#                 <ol>
#                     <li><p>Very deep list item 1!</p></li>
#                     <li><p>Very deep list item 2!</p></li>
#                     <li><p>Very deep list item 3!</p></li>
#                     <li><p>Very deep list item 4!</p></li>
#                     <li><p>Very deep list item 5!</p></li>
#                 </ol>
#             </li>
#         </ol>
#     </li>
# </ol>
# """

"""
@TODO:

- Empty p/Al should be removed

"""


soup = BeautifulSoup(html_content, "html.parser")

root_divisie = Divisie()
root_divisie.consume_children(soup.children)

soup = BeautifulSoup(features='xml')
xml = root_divisie.as_xml(soup)

a = True
